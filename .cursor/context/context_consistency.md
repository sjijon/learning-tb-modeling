# Context: project-wide consistency

This file captures all information needed to check and maintain consistency across the project -- file trees in documentation, cross-references between files, table of contents structures, naming conventions, and known remaining issues.

---

## Canonical file tree (on disk)

```
2026 TB/
  README.md
  tb_overview/
    modeling_tb.tex
    modeling_tb.pdf
    references.bib
    tb_programs_stakeholders.tex
    tb_programs_stakeholders.pdf
  tb_toy_model/
    README.md
    src/
      __init__.py
      model.py
      parameters.py
      plotting.py
    notebooks/
      01_tb_model.ipynb
      02_sensitivity_analysis.ipynb
  ai_approach/
    ai_approach.tex
    ai_approach.pdf
    context.md
  .cursor/
    plans/
      tb_modeling_learning_project_1d0fe19d.plan.md
    skills/
      add-references/SKILL.md
      compile-tex-after-save/SKILL.md
    context/
      context_ai_approach.md
      context_toy_model.md
      context_consistency.md   ← this file
```

Note: there is a stray `notebooks/02_sensitivity_analysis.ipynb` at the project root that duplicates `tb_toy_model/notebooks/02_sensitivity_analysis.ipynb`. It is not referenced anywhere and should be deleted or ignored.

---

## File trees reproduced inside documentation

Every file that contains a directory tree must match the canonical tree above.

| File | Location | Last audited |
|---|---|---|
| `README.md` | "Project structure" section | March 2026 |
| `tb_toy_model/README.md` | "Structure" section | March 2026 |
| `ai_approach/ai_approach.tex` | §8 "Project file tree" (Verbatim block) | March 2026 |

### Root `README.md` tree (should contain)
```
2026 TB/
  tb_overview/
    modeling_tb.tex
    modeling_tb.pdf
    references.bib
    tb_programs_stakeholders.tex
  tb_toy_model/
    README.md
    src/  [model.py, parameters.py, plotting.py]
    notebooks/
      01_tb_model.ipynb
      02_sensitivity_analysis.ipynb
  ai_approach/
    ai_approach.tex
    ai_approach.pdf
```

### `tb_toy_model/README.md` tree (should contain)
```
tb_toy_model/
  src/
    __init__.py
    model.py
    parameters.py
    plotting.py
  notebooks/
    01_tb_model.ipynb
    02_sensitivity_analysis.ipynb
```

### `ai_approach/ai_approach.tex` §8 tree (should contain)
```
2026 TB/
  README.md
  tb_overview/
    modeling_tb.tex
    modeling_tb.pdf
    references.bib
    tb_programs_stakeholders.tex
    tb_programs_stakeholders.pdf
  tb_toy_model/
    README.md
    src/  [__init__.py, model.py, parameters.py, plotting.py]
    notebooks/
      01_tb_model.ipynb
      02_sensitivity_analysis.ipynb
  ai_approach/
    ai_approach.tex
    ai_approach.pdf
  .cursor/
    plans/  [tb_modeling_learning_project_1d0fe19d.plan.md]
    skills/  [add-references/SKILL.md, compile-tex-after-save/SKILL.md]
```

---

## Cross-references between files

All of these must name the target file and folder correctly.

| Source file | Location | Target it references |
|---|---|---|
| `README.md` | "TB transmission model" section | `tb_overview/modeling_tb.pdf` |
| `README.md` | "TB transmission model" section | `tb_toy_model/notebooks/01_tb_model.ipynb` |
| `README.md` | "TB transmission model" section | `tb_toy_model/README.md` |
| `README.md` | "TB programs..." section | `tb_overview/tb_programs_stakeholders.tex` |
| `README.md` | "AI approach" section | `ai_approach/ai_approach.pdf` |
| `tb_toy_model/README.md` | first line | `tb_overview/modeling_tb.pdf` |
| `tb_toy_model/notebooks/01_tb_model.ipynb` | cell 0 | `tb_overview/modeling_tb.pdf` |
| `ai_approach/ai_approach.tex` | §4.2 default target | `tb_overview/modeling_tb.tex` |
| `ai_approach/ai_approach.tex` | §5.1 section header | `tb_overview/` folder |
| `ai_approach/ai_approach.tex` | §6 organizational table | `tb_overview/` folder |
| `.cursor/skills/compile-tex-after-save/SKILL.md` | Defaults + example | `tb_overview/modeling_tb.tex` |

---

## Table of contents structures

### `tb_overview/tb_programs_stakeholders.tex` (has `\tableofcontents`)

1. Major Institutions and Stakeholders
   - 1.1 Multilateral and Intergovernmental Bodies
   - 1.2 Bilateral Donors and Implementing Agencies
   - 1.3 Product Development Partnerships and Research Organizations
   - 1.4 Civil Society and Patient Advocacy
2. Ongoing Prevention Programs
   - 2.1 Vaccination
   - 2.2 TB Preventive Treatment (TPT)
   - 2.3 Infection Control and Case-Finding
3. Treatments: Available and In Development
   - 3.1 Current Standard Regimens
   - 3.2 Vaccines in Advanced Clinical Development
   - 3.3 Drug Pipeline
4. Elimination Efforts
5. Institutions Using Mathematical Models for TB

### `ai_approach/ai_approach.tex` (has `\tableofcontents`)

1. Overview
2. Planning the project
   - 2.1 Initial prompt
   - 2.2 Plan refinement prompts
   - 2.3 Plan contents
3. Agents used
   - 3.1 Plan mode agent
   - 3.2 Agent mode agent
   - 3.3 Tooling agent (second conversation)
4. Cursor Skills created
   - 4.1 `add-references`
   - 4.2 `compile-tex-after-save`
5. Prompts by project component
   - 5.1 Literature review (`tb_overview/`)
   - 5.2 Model architecture (`tb_toy_model/src/`)
   - 5.3 Code (`tb_toy_model/notebooks/`)
   - 5.4 Documentation (`README.md`, this document)
6. Style instructions
   - 6.1 Project organization
   - 6.2 Document style
   - 6.3 README style
   - 6.4 Notebook style
7. Observations on the AI-assisted workflow
   - 7.1 What worked well
   - 7.2 Limitations observed
8. Project file tree

### `tb_overview/modeling_tb.tex` (no `\tableofcontents`)

Sections (unnumbered in document class default):
1. TB epidemiology and natural history
   - 1.1 Current global burden and regional distribution
   - 1.2 Twenty-year trend in global incidence
2. Mathematical modeling approaches for TB
   - 2.1 Stochastic ODE models and uncertainty analysis
   - 2.2 Extended compartmental models with drug resistance and reinfection
   - 2.3 Individual-based and microsimulation models
3. Economic evaluation approaches for TB
4. The SELT(R) model used in this project
   - 4.1 Compartments and biological rationale

The last line of §4.1 cross-references the notebook: `notebook \texttt{01\_tb\_model.ipynb}`.

---

## Notebook titles and cell 0 content

| Notebook | Title (cell 0) | Cross-reference in cell 0 |
|---|---|---|
| `tb_toy_model/notebooks/01_tb_model.ipynb` | "Toy TB model (SELT(R))" | `tb_overview/modeling_tb.pdf` |
| `tb_toy_model/notebooks/02_sensitivity_analysis.ipynb` | "Sensitivity analysis" | none |

---

## Naming conventions

| Item | Correct name | Common wrong variants to watch for |
|---|---|---|
| Folder for LaTeX overviews | `tb_overview/` | `tb_literature_review/` (old name, never existed on disk) |
| Main modeling LaTeX file | `modeling_tb.tex` / `modeling_tb.pdf` | `tb_models.tex`, `tb_background.tex` (old names) |
| First toy model notebook | `01_tb_model.ipynb` | `01_toy_model.ipynb` (old name) |
| Model acronym | SELT(R) | SEILTR, SEIR |
| R0 subscript | R0 or $R_0$ | R₀, R-naught |

---

## Skill default targets

| Skill | Default `.tex` target |
|---|---|
| `compile-tex-after-save` | `tb_overview/modeling_tb.tex` |

When the user asks to compile any other file (e.g., `tb_programs_stakeholders.tex`, `ai_approach.tex`), the skill should be invoked with that path explicitly.

---

## Consistency audit history

| Date | What was checked | Issues found and fixed |
|---|---|---|
| March 2026 | Full project audit | (1) `tb_literature_review/` → `tb_overview/` in 5 files; (2) `01_toy_model.ipynb` → `01_tb_model.ipynb` in 2 files; (3) added `tb_programs_stakeholders` to root README body; (4) fixed root README project tree; (5) fixed compile skill default to `tb_overview/modeling_tb.tex`; (6) updated ai_approach.tex §8 file tree |
