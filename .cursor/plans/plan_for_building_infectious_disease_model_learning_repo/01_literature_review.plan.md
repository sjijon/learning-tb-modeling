---
name: "Step 1: Literature review"
overview: Write a LaTeX literature review covering [DISEASE] epidemiology, natural history, global burden, modeling approaches, and the model specification used in this project. Produces a .tex file, references.bib, and compiled PDF. Read @project_choices.md for the disease and language.
todos:
  - id: research-disease
    content: "Search the literature for [DISEASE] epidemiology: etiology, transmission route, natural history, latent vs active stages, global burden, key epidemiological parameters (R0, incubation period, case fatality). Use WebSearch to find current data and verify all claims."
    status: pending
  - id: write-bib
    content: "Create references.bib in the [disease]_overview/ folder. For each key paper, use the add-references skill: search for the DOI, fetch metadata, and write a complete BibTeX entry. Include at least 6-8 foundational references covering natural history, modeling approaches, and global burden data."
    status: pending
  - id: write-tex
    content: "Write [disease]_overview/modeling_[disease].tex covering: (1) epidemiology and natural history, (2) mathematical modeling approaches used for [DISEASE], (3) the specific model used in this project (biological rationale only -- equations go in the notebook). Include a TikZ flow diagram of the disease natural history. Use natbib + plainnat for citations, MidnightBlue for all links via hyperref."
    status: pending
  - id: compile-pdf
    content: Compile the .tex file to PDF using latexmk. Fix any compilation errors.
    status: pending
  - id: content-split-check
    content: Verify the literature review contains biological rationale but NOT the full ODE system, R0 formula, or parameter table -- those belong in the first notebook (Step 2). If equations are present, move them out and add a cross-reference to the notebook instead.
    status: pending
isProject: false
---

# Step 1: Literature review

## What this plan does

Produces a LaTeX document that serves as both a learning artifact and a literature review for [DISEASE]. This is the scientific foundation that the toy model (Step 2) builds on.

## Prerequisites

- `00_project_setup.plan.md` completed (folder skeleton, skills, and rules exist).
- `@project_choices.md` filled in with your disease.

## What the agent reads

Attach `@project_choices.md` when clicking Build so the agent knows which disease to research.

## Content structure

The document should have these sections:

1. **[DISEASE] epidemiology and natural history** -- transmission, disease stages, global burden, key parameters.
2. **Mathematical modeling approaches for [DISEASE]** -- compartmental ODE models, stochastic models, agent-based models, parameter estimation, sensitivity analysis. Focus on approaches actually used in the [DISEASE] literature.
3. **The model used in this project** -- biological rationale for the compartmental structure chosen in the plan. Cross-reference the notebook for the full ODE system and parameter table.

## After this plan completes

Verify:

- `[disease]_overview/modeling_[disease].tex` exists and compiles to PDF.
- `[disease]_overview/references.bib` has complete entries with DOIs.
- The PDF is readable as a standalone document.
- No equations or parameter tables are in the .tex -- those go in the notebook.

Then proceed to `02_toy_model.plan.md`.