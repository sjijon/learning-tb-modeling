# Context: TB Toy Model (SELT(R))

This file captures all context needed to work on the `tb_toy_model/` component of the project.

---

## Purpose

A deterministic compartmental ODE model of TB transmission, built as a concrete implementation of one TB modeling approach. It is a learning and portfolio artifact, not calibrated to any specific country. Epidemiological background and modeling rationale are in `tb_overview/modeling_tb.pdf`.

---

## Project location

```
tb_toy_model/
  README.md
  src/
    __init__.py
    model.py        # ODE system, solver wrapper, R0 calculation
    parameters.py   # ModelParameters dataclass, InitialState dataclass
    plotting.py     # time series, incidence curve, tornado plot helpers
  notebooks/
    01_tb_model.ipynb             # model spec, baseline simulation, R0, scenarios
    02_sensitivity_analysis.ipynb # one-at-a-time parameter sweeps, tornado plots
```

---

## Model: SELT(R)

Seven compartments: Susceptible (S), Early Latent / fast progressors (Lf), Late Latent / slow progressors (Ls), Subclinical Infectious (Isub), Clinical Infectious (Iclin), Treated (T), Recovered / self-cured (R).

### Why not plain SEIR

- TB latency is heterogeneous: ~10% of new infections progress to active disease within months (fast), ~90% carry a low long-term reactivation risk (slow).
- Self-cure is common (~50% of untreated cases over 3 years); recovered individuals can reactivate.
- Active TB passes through a subclinical stage (Isub) before becoming symptomatic (Iclin): subclinical cases transmit at reduced intensity and escape passive symptom-based case finding (Zwerling et al. 2015, Richards 2023, Kendall 2021).
- Treatment is not instantaneous: the diagnostic cascade (care-seeking → testing → linkage) determines effective detection rate κσφ.
- TB carries excess mortality beyond the background death rate (clinical stage only).

### Compartment flows

```
S   --[infection]--> Lf   --[fast progression]--> Isub
S   --[infection]--> Ls   --[slow reactivation]--> Isub
Isub --[ω]---------> Iclin --[κσφ]-----------> T  --[relapse ρ_T]--> Isub
Isub --[self-cure γ]-> R
Iclin --[self-cure γ]-> R   --[reactivation ρ_R]--> Isub
Iclin --[TB death δ]--> D
```

### ODE system

Force of infection: λ = β · (ε · Isub + Iclin) / N, where N = S + Lf + Ls + Isub + Iclin + T + R.
ε = subclinical_relative_infectiousness (default 0.15).

```
dS/dt     = b·N − λ·S − μ·S
dLf/dt    = f·λ·S − ν_fast·Lf − μ·Lf
dLs/dt    = (1−f)·λ·S − ν_slow·Ls − μ·Ls
dIsub/dt  = ν_fast·Lf + ν_slow·Ls + ρ_T·T + ρ_R·R − (ω + γ + μ)·Isub
dIclin/dt = ω·Isub − (κσφ + γ + δ + μ)·Iclin
dT/dt     = κσφ·Iclin − ρ_T·T − μ·T
dR/dt     = γ·(Isub + Iclin) − ρ_R·R − μ·R
```

### R0 (next-generation matrix)

Let d_sub = ω + γ + μ, d_clin = κσφ + γ + δ + μ.

```
R0 = p_I · β · (ε · d_clin + ω) / (d_sub · d_clin)
p_I = f · ν_fast/(ν_fast + μ) + (1−f) · ν_slow/(ν_slow + μ)
```

Improving σ or φ increases d_clin → reduces R0 (shorter clinical infectious period). Reducing ε (early detection) reduces subclinical transmission contribution.

---

## Default parameters (`src/parameters.py`)

| Symbol | Field name | Default value | Units | Source / note |
|---|---|---|---|---|
| N | `n_agents` | 50,000 | persons | laptop-scale default |
| b | `birth_rate` | 1/70 | 1/year | ~70-year life expectancy |
| μ | `natural_death_rate` | 1/70 | 1/year | ~70-year life expectancy |
| β | `transmission_rate` | 20.0 | 1/year | yields R0 ≈ 2.2, consistent with high-burden TB settings |
| f | `fast_progressor_fraction` | 0.10 | — | 5–10% early progression (Vynnycky & Fine 1997) |
| ν_fast | `fast_progression_rate` | 2.0 | 1/year | months to active TB (Vynnycky & Fine 1997) |
| ν_slow | `slow_reactivation_rate` | 0.001 | 1/year | long-term reactivation (Vynnycky & Fine 1997) |
| ω | `subclinical_progression_rate` | 1.0 | 1/year | ~1-year subclinical phase (Richards 2023, Kendall 2021) |
| ε | `subclinical_relative_infectiousness` | 0.15 | — | ~15% of clinical; indirect household-contact estimates |
| κ | `care_seeking_rate` | 2.0 | 1/year | twice-yearly presentation; patient-delay literature |
| σ | `test_sensitivity` | 0.65 | — | smear microscopy pooled sensitivity (Steingart et al.) |
| φ | `linkage_to_treatment_prob` | 0.80 | — | WHO diagnostic cascade estimates |
| γ | `self_cure_rate` | 0.2 | 1/year | ~5-year mean self-cure (Tiemersma et al. 2011) |
| δ | `tb_mortality_rate` | 0.2 | 1/year | ~50% 3-year fatality (Tiemersma et al. 2011) |
| ρ_T | `relapse_rate_treated` | 0.02 | 1/year | toy value |
| ρ_R | `relapse_rate_recovered` | 0.01 | 1/year | toy value |

Effective detection rate: κ · σ · φ = 2.0 × 0.65 × 0.80 = 1.04/year ≈ old single treatment_rate = 1.0/year.

### Default initial conditions (`create_initial_states`)

- `infectious_clin` (ICLIN) = 10 (scaled from 10 per million)
- `latent_slow` = 50 (scaled from 1,000 per million)
- all other compartments = 0 or S (remainder)

---

## Source module API (`src/`)

### `parameters.py`

```python
@dataclass
class ModelParameters:
    population_size, birth_rate, natural_death_rate,
    transmission_rate, fast_progressor_fraction,
    fast_progression_rate, slow_reactivation_rate,
    treatment_rate, self_cure_rate, tb_mortality_rate,
    relapse_rate_treated, relapse_rate_recovered

@dataclass
class InitialState:
    susceptible, latent_fast, latent_slow, infectious, treated, recovered

def create_default_initial_state(parameters: ModelParameters) -> InitialState
```

### `model.py`

State integer encoding: S=0, LFAST=1, LSLOW=2, ISUB=3, ICLIN=4, T=5, R=6, DEAD=7.

```python
def compute_basic_reproduction_number(parameters: ModelParameters) -> float
    # Analytical R0 via next-generation matrix:
    # R0 = p_I · β · (ε·d_clin + ω) / (d_sub · d_clin)

def run_simulation(parameters, time_horizon_years, seed) -> dict
    # Returns results dict with keys:
    #   time_years, susceptible, latent_fast, latent_slow,
    #   infectious_sub, infectious_clin,
    #   treated, recovered, total_population, prevalence_infectious,
    #   incident_active_tb, new_infections, parameters

def run_replications(parameters, n_replications, time_horizon_years, base_seed) -> list[dict]
```

### `plotting.py`

```python
def plot_compartment_timeseries(results, compartment_names=None, figure_size=(10,6))
    # Line plot of selected compartments over time.

def plot_incident_active_tb(results, figure_size=(10,4))
    # Line plot of incident_active_tb over time.

def plot_tornado(parameter_names, low_values, high_values, baseline_value, x_label, figure_size=(10,6))
    # Horizontal bar tornado chart for sensitivity analysis.
```

---

## Notebooks

### `01_tb_model.ipynb`

Cells in order:
1. Title + framing (subclinical stage + diagnostic cascade extensions)
2. Model structure: 7 compartments, transition table, ODE system with new force of infection
3. R0 formula: two-stage next-generation matrix derivation
4. Parameter table (includes ω, ε, κ, σ, φ; removes old τ)
5. Imports
6. Instantiate `ModelParameters`, compute and print R0 (~1.3)
7. Run 50-year baseline, plot compartments (`infectious_sub`, `infectious_clin`, etc.) and incidence
8. 20 replications — `compartment="infectious_clin"`
9. Stochastic extinction demo — checks `r["infectious_clin"][-1] == 0`

### `02_sensitivity_analysis.ipynb`

Cells in order:
1. Title + cross-reference
2. Imports
3. Run baseline; compute baseline R0 and cumulative incidence (`np.trapz`)
4. One-at-a-time loop: vary parameters ±20%, collect R0 and cumulative incidence for low/high
5. Tornado plot for R0
6. Tornado plot for cumulative incidence

Parameters to sweep (update from old `treatment_rate` to new diagnostic cascade params):
`transmission_rate`, `fast_progressor_fraction`, `subclinical_progression_rate`, `subclinical_relative_infectiousness`, `care_seeking_rate`, `test_sensitivity`, `linkage_to_treatment_prob`, `self_cure_rate`, `tb_mortality_rate`.

---

## Design decisions

- **`ModelParameters` is a dataclass** -- easy to override individual fields for scenarios (`ModelParameters(treatment_rate=2.0)`).
- **`run_simulation` returns a plain dict** -- keys match compartment names; easy to index in notebooks without additional abstractions.
- **`incident_active_tb` computed inside `run_simulation`** -- saves repeating the formula in every notebook.
- **No global state** -- all functions take explicit parameters; nothing depends on module-level variables.
- **Notebooks run from project root** -- `sys.path.append(str(Path.cwd().parent))` in the imports cell keeps `src/` importable without installing the package.

---

## Setup

```bash
pip install -r requirements.txt   # numpy, scipy, matplotlib, jupyter, ipywidgets
cd tb_toy_model
jupyter notebook
```

Python 3.9+. No project install needed; `src/` is imported via `sys.path` in each notebook.

---

## Related files

| File | Role |
|---|---|
| `tb_overview/modeling_tb.pdf` | TB epidemiology background and biological rationale for model structure |
| `tb_overview/modeling_tb.tex` | Source for the above |
| `tb_overview/references.bib` | BibTeX citations (Vynnycky & Fine 1997, Tiemersma et al. 2011, etc.) |
| `ai_approach/ai_approach.pdf` | Documents prompts and decisions used to build this model |
