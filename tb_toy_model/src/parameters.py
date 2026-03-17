from dataclasses import dataclass


@dataclass
class ModelParameters:
    n_agents: int = 50_000
    # Monthly time steps — small enough that competing-risk approximation is accurate
    time_step_years: float = 1.0 / 12.0
    birth_rate: float = 1.0 / 70.0
    natural_death_rate: float = 1.0 / 70.0
    transmission_rate: float = 12.0
    fast_progressor_fraction: float = 0.10
    fast_progression_rate: float = 2.0
    slow_reactivation_rate: float = 0.001
    treatment_rate: float = 1.0
    self_cure_rate: float = 0.2
    tb_mortality_rate: float = 0.2
    relapse_rate_treated: float = 0.02
    relapse_rate_recovered: float = 0.01
