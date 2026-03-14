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

Six compartments: Susceptible (S), Early Latent / fast progressors (Lf), Late Latent / slow progressors (Ls), Infectious (I), Treated (T), Recovered / self-cured (R).

### Why not plain SEIR

- TB latency is heterogeneous: ~10% of new infections progress to active disease within months (fast), ~90% carry a low long-term reactivation risk (slow).
- Self-cure is common (~50% of untreated cases over 3 years); recovered individuals can reactivate.
- Treatment modifies the infectious duration; treated individuals can relapse.
- TB carries excess mortality beyond the background death rate.

### Compartment flows

```
S  --[infection]--> Lf  --[fast progression]--> I
S  --[infection]--> Ls  --[slow reactivation]--> I
I  --[treatment]-->  T  --[relapse]--> I
I  --[self-cure]-->  R  --[reactivation]--> I
I  --[TB death]-->   D  (removed from population)
```

### ODE system

Force of infection: λ = β · I / N, where N = S + Lf + Ls + I + T + R.

```
dS/dt   = b·N − λ·S − μ·S
dLf/dt  = f·λ·S − ν_fast·Lf − μ·Lf
dLs/dt  = (1−f)·λ·S − ν_slow·Ls − μ·Ls
dI/dt   = ν_fast·Lf + ν_slow·Ls + ρ_T·T + ρ_R·R − (τ + γ + δ + μ)·I
dT/dt   = τ·I − ρ_T·T − μ·T
dR/dt   = γ·I − ρ_R·R − μ·R
```

### R0 (next-generation matrix approximation)

```
R0 = β · [1 / (τ + γ + δ + μ)] · [f · ν_fast/(ν_fast + μ) + (1−f) · ν_slow/(ν_slow + μ)]
```

Three factors: transmission rate × mean infectious duration × probability of ever reaching I (weighted over fast and slow progressors).

---

## Default parameters (`src/parameters.py`)

| Symbol | Field name | Default value | Units | Source / note |
|---|---|---|---|---|
| N | `population_size` | 1,000,000 | persons | project default |
| b | `birth_rate` | 1/70 | 1/year | ~70-year life expectancy |
| μ | `natural_death_rate` | 1/70 | 1/year | ~70-year life expectancy |
| β | `transmission_rate` | 12.0 | 1/year | yields plausible R0 |
| f | `fast_progressor_fraction` | 0.10 | — | 5–10% early progression (Vynnycky & Fine 1997) |
| ν_fast | `fast_progression_rate` | 2.0 | 1/year | months to active TB (Vynnycky & Fine 1997) |
| ν_slow | `slow_reactivation_rate` | 0.001 | 1/year | long-term reactivation (Vynnycky & Fine 1997) |
| τ | `treatment_rate` | 1.0 | 1/year | mean 1-year delay to treatment |
| γ | `self_cure_rate` | 0.2 | 1/year | ~5-year mean self-cure (Tiemersma et al. 2011) |
| δ | `tb_mortality_rate` | 0.2 | 1/year | ~50% 3-year fatality (Tiemersma et al. 2011) |
| ρ_T | `relapse_rate_treated` | 0.02 | 1/year | toy value |
| ρ_R | `relapse_rate_recovered` | 0.01 | 1/year | toy value |

### Default initial conditions (`create_default_initial_state`)

- `infectious` = 10
- `latent_slow` = 1,000
- `latent_fast` = 0
- `treated` = 0
- `recovered` = 0
- `susceptible` = N − all above

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

```python
def tuberculosis_ode_system(time_point, state_vector, parameters) -> np.ndarray
    # Right-hand side of the ODE system. Passed directly to solve_ivp.

def compute_basic_reproduction_number(parameters: ModelParameters) -> float
    # Analytical R0 via next-generation matrix approximation.

def run_simulation(parameters, initial_state, time_span_years, evaluation_times) -> dict
    # Runs solve_ivp and returns results dict with keys:
    #   time_years, susceptible, latent_fast, latent_slow, infectious,
    #   treated, recovered, total_population, prevalence_infectious,
    #   incident_active_tb, parameters
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
1. Title + cross-reference to `tb_overview/modeling_tb.pdf`
2. ODE system (markdown with MathJax)
3. R0 formula and interpretation (markdown)
4. Parameter table (markdown)
5. Imports (adds `tb_toy_model/` parent to `sys.path`, imports from `src/`)
6. Instantiate `ModelParameters`, compute and print R0
7. Run 100-year baseline simulation (`np.linspace(0, 100, 1001)`)
8. Plot compartment time series and incidence curve
9. Treatment scenario: baseline vs `treatment_rate=2.0`

### `02_sensitivity_analysis.ipynb`

Cells in order:
1. Title + cross-reference
2. Imports
3. Run baseline; compute baseline R0 and cumulative incidence (`np.trapz`)
4. One-at-a-time loop: vary 8 parameters ±20%, collect R0 and cumulative incidence for low/high
5. Tornado plot for R0
6. Tornado plot for cumulative incidence

Parameters swept: `transmission_rate`, `fast_progressor_fraction`, `fast_progression_rate`, `slow_reactivation_rate`, `treatment_rate`, `self_cure_rate`, `tb_mortality_rate`, `relapse_rate_treated`.

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
