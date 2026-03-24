from dataclasses import dataclass


@dataclass
class ModelParameters:
    n_agents: int = 50_000
    # Monthly time steps — small enough that competing-risk approximation is accurate
    time_step_years: float = 1.0 / 12.0
    birth_rate: float = 1.0 / 70.0
    natural_death_rate: float = 1.0 / 70.0
    transmission_rate: float = 20.0
    fast_progressor_fraction: float = 0.10
    fast_progression_rate: float = 2.0
    slow_reactivation_rate: float = 0.001
    # Subclinical infectious stage
    subclinical_progression_rate: float = 1.0       # ω: rate I_sub → I_clin (1/year, ~1-year subclinical phase)
    subclinical_relative_infectiousness: float = 0.15  # ε: infectiousness of I_sub relative to I_clin
    # Diagnostic cascade (replaces single treatment_rate)
    care_seeking_rate: float = 2.0                  # κ: rate of presenting to health facility (1/year)
    test_sensitivity: float = 0.65                  # σ: probability of correct TB+ result given presentation
    linkage_to_treatment_prob: float = 0.80         # φ: probability of starting treatment given positive test
    self_cure_rate: float = 0.2
    tb_mortality_rate: float = 0.2
    relapse_rate_treated: float = 0.02
    relapse_rate_recovered: float = 0.01
