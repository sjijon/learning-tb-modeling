# tb_toy_model

Python implementation of the SELT(R) compartmental TB model. See `tb_overview/modeling_tb.pdf` for the full mathematical specification and parameter sources.

---

## The model: SELT(R)

The core model is a deterministic compartmental ODE model that captures the key features of TB dynamics that distinguish it from a generic SEIR:

- **Two-speed latency** -- newly infected individuals split into fast progressors (~10%) who develop active TB within months, and slow progressors (~90%) who carry a low long-term reactivation risk.
- **Self-cure** -- a fraction of infectious cases resolve without treatment and enter a recovered state from which reactivation is possible.
- **Treatment and relapse** -- treated individuals can relapse back to infectious.
- **TB-specific mortality** -- active TB carries excess mortality beyond the background death rate.

Compartments:

```
S  -- Susceptible
Lf -- Early latent (fast progressors)
Ls -- Late latent (slow progressors)
I  -- Infectious (active TB)
T  -- Treated
R  -- Recovered (self-cured)
```

Flow:

```
S  --[infection]--> Lf  --[fast progression]--> I
S  --[infection]--> Ls  --[slow reactivation]--> I
I  --[treatment]-->  T  --[relapse]--> I
I  --[self-cure]-->  R  --[reactivation]--> I
I  --[TB death]-->   D
```

The basic reproduction number R0 is computed analytically via the next-generation matrix approach.

---

## Structure

```
tb_toy_model/
  src/
    __init__.py
    model.py        # ODE system, solver wrapper, R0 calculation
    parameters.py   # ModelParameters dataclass with literature-sourced defaults
    plotting.py     # time series, incidence curve, and tornado plot helpers
  notebooks/
    01_tb_model.ipynb             # baseline simulation, R0, treatment scenarios
    02_sensitivity_analysis.ipynb # parameter sweeps, tornado diagrams
```

---

## Notebooks

### `notebooks/01_tb_model.ipynb`

Runs the baseline SELT(R) simulation (100 years, 1M population) and produces:
- Time series of all compartments
- Incidence curve
- Printed R0 value
- Scenario comparison: baseline vs doubled treatment rate

### `notebooks/02_sensitivity_analysis.ipynb`

One-at-a-time sensitivity analysis varying each parameter ±20%:
- Tornado plot of effect on R0
- Tornado plot of effect on cumulative 100-year incidence

---

## Setup

Install dependencies from the project root (Python 3.9+):

```bash
pip install -r ../requirements.txt
```

Launch notebooks from the project root so that the `src/` package is on the path:

```bash
cd ..
jupyter notebook
```

---

## Design decisions

- **SELT(R) rather than plain SEIR** -- the fast/slow latency split and the reactivation pathway are the features that make TB modeling distinct. Implementing them explicitly demonstrates that understanding.
- **Deterministic ODE model first** -- the standard baseline for TB modeling work. Stochastic extensions and agent-based models are natural follow-ups once the deterministic foundation is solid.
- **`src/` separates reusable code from notebooks** -- keeps the ODE system and parameter definitions independent of the notebook narrative.
- **Python only to start** -- `scipy` + `matplotlib` is the dominant stack in this field. R is a natural extension.
