# Reusable Prompts for Building an Infectious Disease Learning Repo

## What this is

This folder contains a sequence of buildable Cursor plans that replicate the structure of the [TB modeling learning project](https://github.com/sjijon/learning-tb-modeling) for other infectious diseases. The TB project was built with roughly 46 user prompts across 9 conversations over 3 days. These plans were themselves built with ai assistance to distill that process into 4 steps, each with its own "Build" button. 

## How to use

### 1. Fill in your project choices

Open `project_choices.md` and fill in the tables: disease, language (Python/R), modeling approach (deterministic ODE / stochastic / agent-based), and optional fields (compartmental structure, time horizon, population size).

### 2. Build the plans in order

Each plan is a `.plan.md` file with a "Build" button. Click "Build" to open an Agent conversation that works through the todos. **Stay in the conversation** -- some steps need your review before the agent continues.

| Step | Plan file | What it produces | User input needed? |
|---|---|---|---|
| 0 | `00_project_setup.plan.md` | Rule, skills, folder skeleton, .gitignore | No -- fully automated |
| 1 | `01_literature_review.plan.md` | LaTeX lit review, references.bib, PDF | Yes -- review the PDF, check citations |
| 2 | `02_toy_model.plan.md` | src/ package, 2 notebooks, requirements.txt | Yes -- run notebooks yourself, paste errors back |
| 3 | `03_documentation.plan.md` | READMEs, stakeholder doc (optional), context files | Yes -- verify cross-references |
| 4 | `04_ai_approach.plan.md` | AI workflow documentation in LaTeX | Yes -- verify prompts match reality |

### 3. Attach project_choices.md to every Build

When you click "Build" on any plan, the agent needs to know your disease and preferences. Type `@project_choices.md` in the chat before or alongside clicking Build, so the agent can read your choices.

### 4. Start a new conversation for each plan

Don't run all plans in one conversation. Each plan should be its own conversation -- this keeps context fresh and prevents the agent from losing track of earlier work. After each plan completes, the context files (created in Step 3) carry the project state forward.

---

## Prerequisites

Before starting Step 0, you need:

1. **Cursor IDE** with Agent mode and Plan mode (Cursor Pro or free tier).
2. **LaTeX** installed locally. On macOS: `brew install --cask mactex`. On Ubuntu: `sudo apt install texlive-full`.
3. **Python 3.9+** with `pip` (or R, depending on your choice).
4. An **empty folder** opened in Cursor as your workspace.

---

## Cursor concepts

- **Plan mode** -- read-only; the agent researches and proposes without changing files.
- **Agent mode** -- execution; the agent reads, writes, and edits files.
- **Skills** (`.cursor/skills/`) -- reusable instruction files the agent follows for specific tasks.
- **Context files** (`.cursor/context/`) -- project state summaries; attach with `@` at conversation start.
- **Rules** (`.cursor/rules/`) -- constraints that apply to every conversation automatically.
- **`@` symbol** -- references a file in your workspace; attaches its contents to the conversation.

---

## When things go wrong

- **The agent writes files in the wrong folder.** Tell it: "Move `[file]` to `[correct_folder]/`."
- **The agent hallucinates a citation.** Verify DOIs by clicking them. Say: "The DOI for [paper] is wrong. Look it up again."
- **The agent puts equations in the literature review.** The `content-split-check` todo in Step 1 should catch this. If not, say: "Move the ODE system and parameter table to the notebook."
- **A notebook doesn't run.** Run it yourself, paste the error into the chat.
- **Folder names diverge from the plan.** The context files (Step 3) capture the actual state.

---

## Files in this folder

| File | Purpose |
|---|---|
| `project_choices.md` | Your disease, language, and modeling preferences -- shared across all plans |
| `00_project_setup.plan.md` | Step 0: Rule, skills, folder skeleton |
| `01_literature_review.plan.md` | Step 1: LaTeX literature review + references |
| `02_toy_model.plan.md` | Step 2: Model code + notebooks |
| `03_documentation.plan.md` | Step 3: READMEs, stakeholder doc, context files |
| `04_ai_approach.plan.md` | Step 4: AI workflow documentation (optional) |
| `tb_modeling_learning_project_1d0fe19d.plan.md` | Original TB project plan (reference only) |

---

## Adapting the model structure for other diseases

The initial prompt in Step 1 lets the agent propose a disease-appropriate compartmental structure. These are reasonable starting points:

| Disease | Suggested base model | Key features to capture |
|---------|---------------------|------------------------|
| TB | SELT(R) | Two-speed latency, self-cure, treatment/relapse, TB mortality |
| Malaria | Ross-Macdonald / SEIR+vector | Vector dynamics, seasonality, partial immunity, superinfection |
| HIV | SI with CD4 stages | Long asymptomatic period, ART as suppression not cure, viral load stages |
| Cholera | SIR + environment | Environmental reservoir (water), short incubation, waning immunity |
| Dengue | Multi-strain SEIR | 4 serotypes, cross-immunity, antibody-dependent enhancement |
| COVID-19 | SEIR with presymptomatic | Presymptomatic transmission, age-stratification, vaccination |
| Measles | SIR | High R0, vaccine-derived immunity, waning |
| Influenza | SEIR + strain drift | Seasonal forcing, antigenic drift, cross-immunity between strains |

---

## What this does not cover

- **Calibration to real data.** The TB project used plausible but uncalibrated parameters.
- **Cost-effectiveness analysis.** Covered conceptually in the literature review but not implemented.
- **Multi-model comparison.** Each project builds one model. Comparing approaches is a follow-up.
