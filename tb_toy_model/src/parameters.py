from dataclasses import dataclass


@dataclass
class ModelParameters:
    population_size: float = 1_000_000.0
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


@dataclass
class InitialState:
    susceptible: float
    latent_fast: float
    latent_slow: float
    infectious: float
    treated: float
    recovered: float


def create_default_initial_state(parameters: ModelParameters) -> InitialState:
    infectious_initial = 10.0
    latent_fast_initial = 0.0
    latent_slow_initial = 1_000.0
    treated_initial = 0.0
    recovered_initial = 0.0
    susceptible_initial = (
        parameters.population_size
        - infectious_initial
        - latent_fast_initial
        - latent_slow_initial
        - treated_initial
        - recovered_initial
    )

    return InitialState(
        susceptible=susceptible_initial,
        latent_fast=latent_fast_initial,
        latent_slow=latent_slow_initial,
        infectious=infectious_initial,
        treated=treated_initial,
        recovered=recovered_initial,
    )
