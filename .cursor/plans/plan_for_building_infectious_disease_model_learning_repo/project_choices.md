# Project choices

Fill in the fields below before running any plan. Every plan in this folder reads this file (via `@project_choices.md`) to know what disease, language, and modeling approach to use.

## Required

| Field | Your choice | Example (TB project) |
|---|---|---|
| **Disease** | ______________________ | Tuberculosis (TB) |
| **Language** | Python / R / both | Python |
| **Modeling approach** | deterministic ODE / stochastic ODE / agent-based | deterministic ODE |

## Optional (the agent will propose defaults if left blank)

| Field | Your choice | Example (TB project) |
|---|---|---|
| **Compartmental structure** | let the agent propose / specify one (e.g., SEIR, SIR+vector) | SELT(R) -- agent proposed, user accepted |
| **Simulation time horizon** | ______ years | 100 years |
| **Population size** | ______ | 50,000 |
| **Include stakeholder document?** | yes / no | yes |
| **Include AI approach documentation?** | yes / no | yes |

## How these choices affect the plans

- **Disease** replaces `[DISEASE]` in every plan's todos and prompts.
- **Language** determines the code package and notebook format:
  - Python → `scipy.integrate.solve_ivp`, `matplotlib`, `numpy`; notebooks in `.ipynb`
  - R → `deSolve::ode`, `ggplot2`; analysis in `.Rmd` files instead of `.ipynb`
  - Both → Python `src/` + R `R/` side by side
- **Modeling approach** determines what the agent builds:
  - Deterministic ODE → `solve_ivp` / `deSolve`, analytical R0 via next-generation matrix
  - Stochastic ODE → Gillespie algorithm or tau-leaping, replicated runs, extinction probability
  - Agent-based → individual-level simulation, contact networks, longer compute time
- **Compartmental structure** can be left for the agent to propose (recommended if you're new to the disease). See the disease adaptation table in the guide for starting points.
