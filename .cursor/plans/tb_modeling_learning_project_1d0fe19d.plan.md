---
name: TB Modeling Learning Project
overview: A structured learning project that builds from TB epidemiology fundamentals through mathematical modeling theory to a working compartmental model in Python, designed both as a skill-building exercise and a portfolio piece for infectious disease modeling positions.
todos:
  - id: phase1-tex
    content: "Phase 1: Write LaTeX document (tex/tb_background.tex) covering TB epidemiology, natural history, key parameters, modeling approaches, and literature references"
    status: completed
  - id: phase2-src
    content: "Phase 2: Build src/ package -- model.py (ODE system + solver), parameters.py (literature-sourced defaults), plotting.py (visualization helpers)"
    status: completed
  - id: phase3-notebook
    content: "Phase 3a: Create toy model notebook (notebooks/01_toy_model.ipynb) -- baseline simulation, R0 calculation, treatment scenarios"
    status: completed
  - id: phase4-sensitivity
    content: "Phase 3b: Create sensitivity analysis notebook (notebooks/02_sensitivity_analysis.ipynb) -- parameter sweeps, tornado diagram, scenario comparisons"
    status: completed
  - id: phase5-polish
    content: "Phase 4: Polish -- ensure notebooks run end-to-end, check epidemiological plausibility of outputs, set up requirements.txt"
    status: completed
isProject: false
---

# TB Infectious Disease Modeling Project

## Why this structure

Research scientist positions in TB modeling expect familiarity with: (a) TB natural history and its quirks vs other infectious diseases, (b) compartmental ODE models and their assumptions, and (c) practical implementation including parameter estimation and sensitivity analysis. This project walks through all three, producing a working model and annotated notebooks that double as a portfolio.

---

## Phases 1-2: LaTeX Background Document

Write a single LaTeX document ([tex/tb_background.tex](tex/tb_background.tex)) that serves as both a learning artifact and a literature review. Compile with standard `pdflatex` + `bibtex`. Sections:

### Section 1: TB Epidemiology and Natural History

- **Etiology and transmission**: *M. tuberculosis*, airborne spread, prolonged close contact, not equally infectious across disease stages
- **Latent vs Active TB**: ~90% of infected remain latent; ~5-10% progress to active disease within 2 years ("fast progressors"), remainder reactivate decades later ("slow progressors" at ~0.1%/year)
- **Disease spectrum**: recent literature (Dowdy et al., Kendall et al.) shows TB is not binary latent/active but a continuum -- subclinical (infectious but asymptomatic) disease matters
- **Natural history without treatment**: ~50% mortality over 3 years for active TB, ~50% self-cure; mean infectious duration ~3 years
- **Treatment**: 6-month standard regimen (DOTS), drug-resistant TB (MDR/XDR)
- **Global burden**: WHO estimates, high-burden countries, HIV co-infection
- **Key epidemiological parameters**: R0 ~ 1.5-3.5, incubation highly variable, case fatality rates
- Include a TikZ or included figure of the TB natural history flow diagram

### Section 2: Mathematical Modeling Approaches for TB

- **Compartmental ODE models**: SIR, SEIR, and TB-specific extensions (SEILTR, SVEITRS)
- **Why TB needs more than SIR**: long latency, fast/slow progression, reactivation, treatment compartment
- **The math**: system of ODEs, basic reproduction number (R0) via next-generation matrix, disease-free and endemic equilibria
- **Stochastic vs deterministic models**: when each matters, brief overview
- **Agent-based models**: brief overview, when used for TB (household transmission, heterogeneous contact)
- **Parameter estimation**: least squares, MLE, Bayesian approaches
- **Sensitivity analysis**: one-at-a-time, PRCC, tornado diagrams

### Section 3: Model Description (the SELT(R) model built in Phase 3)

- Full mathematical specification of the ODE system
- Parameter table with values, ranges, units, and literature sources
- R0 derivation
- This section bridges the LaTeX document to the computational notebooks

### References

BibTeX file ([tex/references.bib](tex/references.bib)) with key citations:

- Vynnycky & Fine (1997) -- classic TB transmission model
- WHO Global Tuberculosis Report 2025
- Dowdy et al. -- subclinical TB
- Houben & Dodd (2016) -- global latent TB burden
- Tiemersma et al. (2011) -- natural history parameters
- Kendall et al. (2021) -- disease spectrum synthesis
- Diekmann et al. (1990) -- next-generation matrix for R0

Deliverable: `tex/tb_background.tex` + `tex/references.bib`, compilable to PDF.

---

## Phase 3: Build a Toy Compartmental Model in Python

This is the core technical deliverable. Build a TB-specific compartmental model step by step.

### Model: SELT(R) -- Susceptible, Early Latent, Late Latent, Infectious (Treated/Recovered)

This captures the key TB-specific dynamics that distinguish it from a generic SEIR:

```
S --[infection]--> E_fast --[fast progression]--> I
                   E_slow --[slow reactivation]--> I
I --[treatment]--> T (Recovered/Treated)
I --[self-cure]--> R (can reactivate)
I --[TB death]--> D
T --[relapse]--> I
```

### Implementation plan

`**src/model.py**` -- Core model module:

- ODE system function defining dS/dt, dE_fast/dt, dE_slow/dt, dI/dt, dT/dt, dR/dt
- Parameter dataclass or dictionary with default values from literature
- Solver wrapper using `scipy.integrate.solve_ivp`
- R0 calculation function (next-generation matrix approach)

`**src/parameters.py**` -- Parameter definitions:

- Default parameter set with literature sources cited in comments
- Key parameters: beta (transmission rate), p (fraction fast progressors ~0.05-0.15), v_fast (fast progression rate ~2/year), v_slow (slow reactivation rate ~0.001/year), gamma (recovery/self-cure rate), mu_tb (TB mortality rate), tau (treatment rate), relapse_rate
- Demographic parameters: birth/death rate, total population

`**src/plotting.py**` -- Visualization helpers:

- Time series of compartment populations
- Phase portraits
- Tornado/sensitivity plots

`**notebooks/01_toy_model.ipynb**` -- Main model notebook:

1. Import from `src/`, run baseline simulation (e.g., 100 years, population of 1M, single introduction)
2. Visualize epidemic dynamics: incidence curve, prevalence, latent reservoir size
3. Calculate and interpret R0
4. Explore scenarios: what happens when you introduce treatment? Vary treatment coverage?
5. Brief markdown cells for context, but full mathematical exposition lives in the LaTeX document

`**notebooks/02_sensitivity_analysis.ipynb**` -- Parameter exploration:

1. One-at-a-time sensitivity analysis: vary each parameter +/- 20%, plot effect on R0 and cumulative incidence
2. Tornado diagram showing which parameters matter most
3. Scenario comparison: high-burden vs low-burden settings (different beta, treatment rates)

### Dependencies

`**requirements.txt**`:

- numpy
- scipy
- matplotlib
- jupyter
- ipywidgets (optional, for interactive sliders)

---

## Phase 4: Wrap-Up and Portfolio Polish

- Ensure all notebooks run end-to-end
- Add a brief project-level `__init__.py` for the `src/` package
- Review model outputs for epidemiological plausibility (endemic equilibrium prevalence ~100-500 per 100k for high-burden, R0 in expected range)

---

## Project Structure

```
2026 TB/
  requirements.txt
  tex/
    tb_background.tex
    references.bib
  notebooks/
    01_toy_model.ipynb
    02_sensitivity_analysis.ipynb
  src/
    __init__.py
    model.py
    parameters.py
    plotting.py
```

---

## Key design decisions

- **Python only** (not R) to start -- scipy + matplotlib is the standard stack for this work, and most TB modeling groups use Python. R version could be a follow-up.
- **Deterministic ODE model** first -- this is the expected baseline skill. Stochastic/ABM extensions are natural follow-ups.
- **LaTeX for background/theory, notebooks for computation, `src/` for reusable code** -- this three-layer separation shows both scientific writing and software engineering maturity.
- **SELT(R) rather than plain SEIR** -- demonstrates understanding that TB has unique dynamics (latency bifurcation, reactivation). This is the kind of detail interviewers look for.

