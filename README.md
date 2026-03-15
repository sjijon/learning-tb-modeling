# Learning about tuberculosis (TB) modeling approaches

This is a self-directed learning project to build skills in TB epidemiology, modeling approaches and using AI agents to achieve those goals. This project was designed as both a learning artifact and a portfolio piece for infectious disease research scientist positions focusing in TB modeling.

---

## Goals

1. Learn the epidemiology and natural history of tuberculosis.
2. Research the TB programs, funding landscape, modeling groups, and key stakeholders to understand the field context for research scientist positions.
3. Survey the different mathematical modeling approaches used in TB research.
4. Build a working TB-specific toy model in Python.
5. Develop project architecture skills using AI agents, structuring a new technical subject into organized, layered deliverables from scratch, documenting the tools, prompts, and workflows used throughout.

---

## Project structure

```
2026 TB/
  tb_overview/
    modeling_tb.tex                 # TB epidemiology, natural history, modeling approaches (LaTeX)
    modeling_tb.pdf                 # compiled PDF
    references.bib                  # BibTeX citations
    tb_programs_stakeholders.tex    # TB programs, funding, modeling groups, stakeholders
  tb_toy_model/
    README.md                       # model description, setup, design decisions
    src/
      model.py                      # ODE system and solver wrapper
      parameters.py                 # parameter dataclass with literature-sourced defaults
      plotting.py                   # time series, incidence, and tornado plot helpers
    notebooks/
      01_tb_model.ipynb             # model spec, baseline simulation, R0, treatment scenarios
      02_sensitivity_analysis.ipynb # parameter sweeps, tornado plots
  ai_approach/
    ai_approach.tex                 # documentation of AI agent use, skills, and prompts
    ai_approach.pdf                 # compiled PDF
```

---

## TB transmission model

In [`tb_toy_model/`](tb_toy_model/), I build my very first TB model. I start with a very simple deterministic approach, that I plan to develop further to account for treatment, prevention and policy and economic evaluations. 

This is a deterministic SELT(R) compartmental ODE system (Susceptible, Early Latent, Late Latent, Infectious, Treated, Recovered). It captures TB-specific dynamics -- two-speed latency, self-cure, treatment, relapse, and TB-specific mortality -- that a generic SEIR does not represent. R0 is computed analytically via the next-generation matrix.

- Biological rationale and modeling approach: [`tb_overview/modeling_tb.pdf`](tb_overview/modeling_tb.pdf)
- ODE equations, parameter table, and simulation results: [`tb_toy_model/notebooks/01_tb_model.ipynb`](tb_toy_model/notebooks/01_tb_model.ipynb)
- Code and setup: [`tb_toy_model/`](tb_toy_model/README.md)
- Documentation of how I used AI agents to build the model: [`ai_approach/ai_approach.pdf`](ai_approach/ai_approach.pdf), Section 5 (Prompts by project component)

---

## TB programs, stakeholders, and elimination

In [`tb_overview/`](tb_overview/), [`tb_programs_stakeholders.tex`](tb_overview/tb_programs_stakeholders.tex) covers the field context relevant to research scientist positions: the major institutions (WHO, Stop TB Partnership, Global Fund, USAID/PEPFAR, CDC), ongoing prevention programs (BCG, TPT regimens, case-finding), current and pipeline treatments, the WHO End TB Strategy and elimination targets, and the main academic groups that use mathematical models for TB.

---

## AI approach

This project was built using Cursor AI agents (Plan mode + Agent mode) and custom skills. The full account --prompts used, agents involved, organizational decisions, and observations-- is documented in [`ai_approach/ai_approach.pdf`](ai_approach/ai_approach.pdf).

