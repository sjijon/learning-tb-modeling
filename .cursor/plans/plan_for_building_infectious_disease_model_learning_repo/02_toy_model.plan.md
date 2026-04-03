---
name: "Step 2: Toy model"
overview: Build the compartmental model code package and two notebooks -- a baseline simulation with R0 and intervention scenarios, and a sensitivity analysis with tornado diagrams. Read @project_choices.md for the disease, language, modeling approach, and simulation parameters.
todos:
  - id: write-parameters
    content: "Create the parameters module ([disease]_toy_model/src/parameters.py or R/parameters.R). Define a dataclass (Python) or named list (R) with literature-sourced default values for all model parameters. Include units and source citations as comments. Use the compartmental structure proposed during planning."
    status: pending
  - id: write-model
    content: "Create the model module ([disease]_toy_model/src/model.py or R/model.R). Implement: (1) the ODE system function, (2) a solver wrapper using solve_ivp (Python) or deSolve::ode (R), (3) an R0 calculation function using the next-generation matrix approach. If stochastic: implement Gillespie or tau-leaping instead of deterministic ODE."
    status: pending
  - id: write-plotting
    content: "Create the plotting module ([disease]_toy_model/src/plotting.py or R/plotting.R). Implement: (1) compartment time series plot, (2) incidence curve plot, (3) tornado/sensitivity bar chart. Use matplotlib (Python) or ggplot2 (R)."
    status: pending
  - id: write-init
    content: "If Python: create [disease]_toy_model/src/__init__.py so the package is importable."
    status: pending
  - id: write-notebook-baseline
    content: "Create the baseline simulation notebook ([disease]_toy_model/notebooks/01_[disease]_model.ipynb or .Rmd). Contents: (1) title cell with cross-reference to the literature review PDF, (2) full ODE system in markdown/MathJax, (3) R0 formula with derivation notes, (4) parameter table with values/units/sources, (5) import from src/ and run baseline simulation, (6) plot compartment dynamics and incidence, (7) compute and print R0, (8) intervention scenario comparison (e.g., vary treatment rate)."
    status: pending
  - id: write-notebook-sensitivity
    content: "Create the sensitivity analysis notebook ([disease]_toy_model/notebooks/02_sensitivity_analysis.ipynb or .Rmd). Contents: (1) title cell, (2) imports and baseline run, (3) one-at-a-time parameter sweep (+/- 20%), (4) tornado diagram for R0, (5) tornado diagram for cumulative incidence."
    status: pending
  - id: write-requirements
    content: "Create requirements.txt (Python) or DESCRIPTION/renv.lock (R) at the project root with all dependencies and their versions."
    status: pending
isProject: false
---

# Step 2: Toy model

## What this plan does

Builds the computational core of the project: a compartmental model in `src/` (or `R/`), a baseline simulation notebook, and a sensitivity analysis notebook.

## Prerequisites

- `01_literature_review.plan.md` completed (the literature review exists and informs the model structure).
- `@project_choices.md` filled in with disease, language, modeling approach, time horizon, and population size.

## What the agent reads

Attach `@project_choices.md` when clicking Build. The agent should also read the literature review `.tex` file to ensure the model structure matches the biological rationale described there.

## Model structure

The compartmental structure should have been proposed by the agent during planning (Step 0/1) and accepted by the user. The agent should use that structure here. Common examples:

| Disease | Typical structure |
|---|---|
| TB | SELT(R) -- two-speed latency, self-cure, treatment, relapse |
| Malaria | SEIR + vector population, seasonality |
| HIV | SI with CD4 stages, ART compartments |
| Cholera | SIR + environmental reservoir |
| Dengue | Multi-strain SEIR, cross-immunity |
| COVID-19 | SEIR with presymptomatic stage |

## After this plan completes

Verify:
- `[disease]_toy_model/src/` (or `R/`) has 3 code files + `__init__.py` if Python.
- Both notebooks exist and are populated with markdown and code cells.
- Run the notebooks yourself in Jupyter (or knit the .Rmd). Paste any errors back into the chat.
- R0 is in the expected range for the disease.
- `requirements.txt` (or equivalent) exists at the project root.

Then proceed to `03_documentation.plan.md`.
