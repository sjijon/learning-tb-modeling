from dataclasses import asdict
from typing import Dict, List, Optional

import numpy as np

from .parameters import ModelParameters

# Integer encoding for agent states
S, LFAST, LSLOW, ISUB, ICLIN, T, R, DEAD = 0, 1, 2, 3, 4, 5, 6, 7

STATE_NAMES = (
    "susceptible",
    "latent_fast",
    "latent_slow",
    "infectious_sub",   # subclinical: lower infectiousness, not passively detectable
    "infectious_clin",  # clinical: full infectiousness, detectable
    "treated",
    "recovered",
)


def _prob(rate: float, dt: float) -> float:
    """Exact probability of at least one event in interval dt for an exponential waiting time."""
    return 1.0 - np.exp(-rate * dt)


def create_initial_states(parameters: ModelParameters) -> np.ndarray:
    """Returns (n_agents,) int8 array with initial state assignments.

    Scales from the ODE defaults (10 clinical-infectious + 1000 latent_slow per million).
    Initial infectious agents start in ICLIN (already symptomatic seeds).
    """
    states = np.zeros(parameters.n_agents, dtype=np.int8)
    scale = parameters.n_agents / 1_000_000
    n_infectious = max(1, round(10 * scale))
    n_latent_slow = max(1, round(1_000 * scale))
    states[:n_infectious] = ICLIN
    states[n_infectious : n_infectious + n_latent_slow] = LSLOW
    # remaining agents start as S
    return states


def _count_states(states: np.ndarray) -> np.ndarray:
    """Returns integer counts for states S through R (indices 0..6)."""
    return np.array([(states == k).sum() for k in range(7)], dtype=np.int32)


def _step(
    states: np.ndarray,
    parameters: ModelParameters,
    rng: np.random.Generator,
) -> tuple:
    """Advance all agents by one time step.

    Returns (new_states, n_new_infections, n_incident_active_tb) where:
      n_new_infections     = agents transitioning S -> Lfast or Lslow
      n_incident_active_tb = agents entering ISUB from any source (onset of active TB)
    """
    dt = parameters.time_step_years
    n_total = len(states)
    n_alive = int((states != DEAD).sum())
    n_isub = int((states == ISUB).sum())
    n_iclin = int((states == ICLIN).sum())

    # Subclinical cases contribute ε times the infectiousness of clinical cases
    effective_infectious = (
        parameters.subclinical_relative_infectiousness * n_isub + n_iclin
    )
    lambda_ = (
        parameters.transmission_rate * effective_infectious / n_alive
        if n_alive > 0
        else 0.0
    )

    new_states = states.copy()
    # Single uniform draw per agent — sequential competing risks
    u = rng.random(n_total)

    p_nat_death = _prob(parameters.natural_death_rate, dt)

    # --- S: infection (-> Lfast or Lslow) or natural death ---
    s_mask = states == S
    p_infect = _prob(lambda_, dt)
    infected = s_mask & (u < p_infect)
    fast_infected = infected & (rng.random(n_total) < parameters.fast_progressor_fraction)
    new_states[fast_infected] = LFAST
    new_states[infected & ~fast_infected] = LSLOW
    new_states[s_mask & ~infected & (u < p_infect + p_nat_death)] = DEAD
    n_new_infections = int(infected.sum())

    # --- LFAST: fast progression to ISUB or natural death ---
    lf_mask = states == LFAST
    p_prog_fast = _prob(parameters.fast_progression_rate, dt)
    progressed_lf = lf_mask & (u < p_prog_fast)
    new_states[progressed_lf] = ISUB
    new_states[lf_mask & ~progressed_lf & (u < p_prog_fast + p_nat_death)] = DEAD

    # --- LSLOW: slow reactivation to ISUB or natural death ---
    ls_mask = states == LSLOW
    p_react = _prob(parameters.slow_reactivation_rate, dt)
    reactivated_ls = ls_mask & (u < p_react)
    new_states[reactivated_ls] = ISUB
    new_states[ls_mask & ~reactivated_ls & (u < p_react + p_nat_death)] = DEAD

    # --- ISUB: competing exits: progress to ICLIN, self-cure, natural death ---
    # No TB-specific mortality and no passive detection at the subclinical stage
    isub_mask = states == ISUB
    p_progress_sub = _prob(parameters.subclinical_progression_rate, dt)
    p_cure_sub = _prob(parameters.self_cure_rate, dt)
    progressed_to_clin = isub_mask & (u < p_progress_sub)
    self_cured_sub = isub_mask & ~progressed_to_clin & (u < p_progress_sub + p_cure_sub)
    nat_died_sub = (
        isub_mask
        & ~progressed_to_clin
        & ~self_cured_sub
        & (u < p_progress_sub + p_cure_sub + p_nat_death)
    )
    new_states[progressed_to_clin] = ICLIN
    new_states[self_cured_sub] = R
    new_states[nat_died_sub] = DEAD

    # --- ICLIN: competing exits: detection/treatment, self-cure, TB death, natural death ---
    # Effective detection rate = κ · σ · φ
    iclin_mask = states == ICLIN
    p_detect = _prob(
        parameters.care_seeking_rate
        * parameters.test_sensitivity
        * parameters.linkage_to_treatment_prob,
        dt,
    )
    p_cure_clin = _prob(parameters.self_cure_rate, dt)
    p_tb_death = _prob(parameters.tb_mortality_rate, dt)
    detected_now = iclin_mask & (u < p_detect)
    self_cured_clin = iclin_mask & ~detected_now & (u < p_detect + p_cure_clin)
    tb_died = iclin_mask & ~detected_now & ~self_cured_clin & (u < p_detect + p_cure_clin + p_tb_death)
    nat_died_clin = (
        iclin_mask
        & ~detected_now
        & ~self_cured_clin
        & ~tb_died
        & (u < p_detect + p_cure_clin + p_tb_death + p_nat_death)
    )
    new_states[detected_now] = T
    new_states[self_cured_clin] = R
    new_states[tb_died] = DEAD
    new_states[nat_died_clin] = DEAD

    # --- T: relapse to ISUB or natural death ---
    t_mask = states == T
    p_relapse_t = _prob(parameters.relapse_rate_treated, dt)
    relapsed_t = t_mask & (u < p_relapse_t)
    new_states[relapsed_t] = ISUB
    new_states[t_mask & ~relapsed_t & (u < p_relapse_t + p_nat_death)] = DEAD

    # --- R: reactivation to ISUB or natural death ---
    r_mask = states == R
    p_relapse_r = _prob(parameters.relapse_rate_recovered, dt)
    relapsed_r = r_mask & (u < p_relapse_r)
    new_states[relapsed_r] = ISUB
    new_states[r_mask & ~relapsed_r & (u < p_relapse_r + p_nat_death)] = DEAD

    # --- Births: replace dead slots with new susceptibles ---
    n_births = int(rng.poisson(parameters.birth_rate * n_alive * dt))
    dead_indices = np.where(new_states == DEAD)[0]
    if len(dead_indices) > 0 and n_births > 0:
        n_to_fill = min(n_births, len(dead_indices))
        birth_slots = rng.choice(dead_indices, size=n_to_fill, replace=False)
        new_states[birth_slots] = S

    # All entries into ISUB constitute new incident active TB episodes
    n_incident_active_tb = int(
        progressed_lf.sum() + reactivated_ls.sum() + relapsed_t.sum() + relapsed_r.sum()
    )

    return new_states, n_new_infections, n_incident_active_tb


def compute_basic_reproduction_number(parameters: ModelParameters) -> float:
    """Analytical R0 from next-generation matrix.

    With subclinical and clinical infectious stages:
      R0 = prob_reach_I · β · (ε · d_clin + ω) / (d_sub · d_clin)

    where:
      d_sub  = ω + γ + μ          (total exit rate from I_sub)
      d_clin = κσφ + γ + δ + μ    (total exit rate from I_clin)
      ω      = subclinical_progression_rate
      ε      = subclinical_relative_infectiousness
      κσφ    = care_seeking_rate · test_sensitivity · linkage_to_treatment_prob
    """
    mu = parameters.natural_death_rate
    omega = parameters.subclinical_progression_rate
    epsilon = parameters.subclinical_relative_infectiousness
    gamma = parameters.self_cure_rate
    delta = parameters.tb_mortality_rate
    kappa_sigma_phi = (
        parameters.care_seeking_rate
        * parameters.test_sensitivity
        * parameters.linkage_to_treatment_prob
    )

    d_sub = omega + gamma + mu
    d_clin = kappa_sigma_phi + gamma + delta + mu

    fast_progression_probability = parameters.fast_progression_rate / (
        parameters.fast_progression_rate + mu
    )
    slow_progression_probability = parameters.slow_reactivation_rate / (
        parameters.slow_reactivation_rate + mu
    )
    prob_reach_i = (
        parameters.fast_progressor_fraction * fast_progression_probability
        + (1.0 - parameters.fast_progressor_fraction) * slow_progression_probability
    )

    return parameters.transmission_rate * prob_reach_i * (epsilon * d_clin + omega) / (d_sub * d_clin)


def run_simulation(
    parameters: ModelParameters,
    time_horizon_years: float = 50.0,
    seed: Optional[int] = None,
) -> Dict[str, np.ndarray]:
    """Run a single stochastic microsimulation.

    Returns a results dict with time series arrays (one value per time step):
      time_years, susceptible, latent_fast, latent_slow,
      infectious_sub, infectious_clin,
      treated, recovered,
      total_population, prevalence_infectious,
      incident_active_tb, new_infections
    """
    rng = np.random.default_rng(seed)
    states = create_initial_states(parameters)

    n_steps = round(time_horizon_years / parameters.time_step_years)
    counts = np.zeros((n_steps + 1, 7), dtype=np.int32)
    incident_active_tb = np.zeros(n_steps + 1, dtype=np.int32)
    new_infections = np.zeros(n_steps + 1, dtype=np.int32)

    counts[0] = _count_states(states)

    for step in range(n_steps):
        states, n_inf, n_inc = _step(states, parameters, rng)
        counts[step + 1] = _count_states(states)
        new_infections[step + 1] = n_inf
        incident_active_tb[step + 1] = n_inc

    time_years = np.linspace(0.0, time_horizon_years, n_steps + 1)
    total_population = counts.sum(axis=1)

    results = {name: counts[:, k] for k, name in enumerate(STATE_NAMES)}
    results["time_years"] = time_years
    results["total_population"] = total_population
    # prevalence_infectious = total active TB (subclinical + clinical) as a fraction
    total_infectious = counts[:, ISUB] + counts[:, ICLIN]
    results["prevalence_infectious"] = total_infectious / np.maximum(total_population, 1)
    results["incident_active_tb"] = incident_active_tb
    results["new_infections"] = new_infections
    results["parameters"] = asdict(parameters)

    return results


def run_replications(
    parameters: ModelParameters,
    n_replications: int = 10,
    time_horizon_years: float = 50.0,
    base_seed: int = 0,
) -> List[Dict]:
    """Run multiple independent replications with different seeds."""
    return [
        run_simulation(parameters, time_horizon_years, seed=base_seed + rep)
        for rep in range(n_replications)
    ]
