from dataclasses import asdict
from typing import Dict, Tuple

import numpy as np
from scipy.integrate import solve_ivp

from .parameters import InitialState, ModelParameters

STATE_VARIABLE_NAMES = (
    "susceptible",
    "latent_fast",
    "latent_slow",
    "infectious",
    "treated",
    "recovered",
)


def _build_state_vector(initial_state: InitialState) -> np.ndarray:
    return np.array(
        [
            initial_state.susceptible,
            initial_state.latent_fast,
            initial_state.latent_slow,
            initial_state.infectious,
            initial_state.treated,
            initial_state.recovered,
        ],
        dtype=float,
    )


def _force_of_infection(
    transmission_rate: float, infectious: float, total_population: float
) -> float:
    return transmission_rate * infectious / total_population


def tuberculosis_ode_system(
    time_point: float, state_vector: np.ndarray, parameters: ModelParameters
) -> np.ndarray:
    susceptible, latent_fast, latent_slow, infectious, treated, recovered = state_vector
    total_population = (
        susceptible + latent_fast + latent_slow + infectious + treated + recovered
    )
    force_of_infection = _force_of_infection(
        parameters.transmission_rate, infectious, total_population
    )

    new_infections_fast = parameters.fast_progressor_fraction * force_of_infection * susceptible
    new_infections_slow = (
        (1.0 - parameters.fast_progressor_fraction)
        * force_of_infection
        * susceptible
    )

    d_susceptible = (
        parameters.birth_rate * total_population
        - new_infections_fast
        - new_infections_slow
        - parameters.natural_death_rate * susceptible
    )
    d_latent_fast = (
        new_infections_fast
        - parameters.fast_progression_rate * latent_fast
        - parameters.natural_death_rate * latent_fast
    )
    d_latent_slow = (
        new_infections_slow
        - parameters.slow_reactivation_rate * latent_slow
        - parameters.natural_death_rate * latent_slow
    )
    d_infectious = (
        parameters.fast_progression_rate * latent_fast
        + parameters.slow_reactivation_rate * latent_slow
        + parameters.relapse_rate_treated * treated
        + parameters.relapse_rate_recovered * recovered
        - (
            parameters.treatment_rate
            + parameters.self_cure_rate
            + parameters.tb_mortality_rate
            + parameters.natural_death_rate
        )
        * infectious
    )
    d_treated = (
        parameters.treatment_rate * infectious
        - parameters.relapse_rate_treated * treated
        - parameters.natural_death_rate * treated
    )
    d_recovered = (
        parameters.self_cure_rate * infectious
        - parameters.relapse_rate_recovered * recovered
        - parameters.natural_death_rate * recovered
    )

    return np.array(
        [
            d_susceptible,
            d_latent_fast,
            d_latent_slow,
            d_infectious,
            d_treated,
            d_recovered,
        ],
        dtype=float,
    )


def compute_basic_reproduction_number(parameters: ModelParameters) -> float:
    infectious_outflow_rate = (
        parameters.treatment_rate
        + parameters.self_cure_rate
        + parameters.tb_mortality_rate
        + parameters.natural_death_rate
    )
    infectious_duration = 1.0 / infectious_outflow_rate
    fast_progression_probability = parameters.fast_progression_rate / (
        parameters.fast_progression_rate + parameters.natural_death_rate
    )
    slow_progression_probability = parameters.slow_reactivation_rate / (
        parameters.slow_reactivation_rate + parameters.natural_death_rate
    )
    progression_probability = (
        parameters.fast_progressor_fraction * fast_progression_probability
        + (1.0 - parameters.fast_progressor_fraction) * slow_progression_probability
    )

    return parameters.transmission_rate * infectious_duration * progression_probability


def run_simulation(
    parameters: ModelParameters,
    initial_state: InitialState,
    time_span_years: Tuple[float, float],
    evaluation_times: np.ndarray,
) -> Dict[str, np.ndarray]:
    initial_state_vector = _build_state_vector(initial_state)

    solution = solve_ivp(
        tuberculosis_ode_system,
        time_span_years,
        initial_state_vector,
        t_eval=evaluation_times,
        args=(parameters,),
    )

    results = {name: solution.y[index] for index, name in enumerate(STATE_VARIABLE_NAMES)}
    results["time_years"] = solution.t

    total_population = (
        results["susceptible"]
        + results["latent_fast"]
        + results["latent_slow"]
        + results["infectious"]
        + results["treated"]
        + results["recovered"]
    )
    results["total_population"] = total_population
    results["prevalence_infectious"] = results["infectious"] / total_population

    results["incident_active_tb"] = (
        parameters.fast_progression_rate * results["latent_fast"]
        + parameters.slow_reactivation_rate * results["latent_slow"]
        + parameters.relapse_rate_treated * results["treated"]
        + parameters.relapse_rate_recovered * results["recovered"]
    )

    results["parameters"] = asdict(parameters)

    return results
