# Context: Style and Organization Preferences

All style and organization decisions recorded here were either explicitly requested in a user prompt or accepted without change after the agent proposed them. Sources: all agent transcripts in this project.

---

## Project organization — what lives where

| Location | Content |
|---|---|
| `tb_overview/` | Background science: epidemiology, biological rationale for model structure, economic evaluation framing. No equations, no parameter values. |
| `tb_toy_model/notebooks/` | Full model spec (ODEs, R₀ formula, parameter table) and all computational results. |
| `tb_toy_model/src/` | Reusable Python implementation only. No narrative text. |
| `README.md` (root) | Entry point: goals, folder map, one-paragraph summaries with links. Nothing longer than a short paragraph per section. |
| `tb_toy_model/README.md` | Reference doc for model code and notebooks: compartments, setup commands, design decisions. |
| `ai_approach/` | Meta-documentation: how the project was built using AI agents. Descriptive record, not instructions. |
| `.cursor/context/` | Agent context files (one per sub-project or cross-cutting concern). Referenced explicitly at session start via `@`. |

**Core principle:** LaTeX for narrative scientific writing; `.ipynb` exclusively for computation and visualization. Never duplicate narrative content across documents.

**Content split between `modeling_tb.tex` and `01_tb_model.ipynb`:**
- In the literature review: biological rationale for each compartment, cross-reference to notebook for equations.
- In the notebook: full ODE system, R₀ formula with derivation notes, parameter table with units and sources.

---

## LaTeX style

Applies to all `.tex` files in this project (`modeling_tb.tex`, `tb_programs_stakeholders.tex`, `ai_approach.tex`).

**Document class and layout:**
```latex
\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
```

**Color scheme — all links, citations, and URLs:**
```latex
\usepackage[dvipsnames]{xcolor}
\usepackage[colorlinks=true,
            linkcolor=MidnightBlue,
            citecolor=MidnightBlue,
            urlcolor=MidnightBlue]{hyperref}
```
MidnightBlue on all internal links, citations, and URLs. Prints legibly in greyscale.

**Bibliography:** `natbib` + `plainnat` style (author-year citations). Applied to documents with references; `ai_approach.tex` has no bibliography.

**Tables:** `longtable` + `booktabs`. Two-column layout for prompt/effect tables.

**Verbatim:** `fancyvrb`'s `\Verbatim[fontsize=\small]` for file trees and code snippets.

**Prompt display** (in `ai_approach.tex` only): custom `promptbox` environment using `mdframed` with gray background (`gray!10`), gray border (`gray!40`).

**Section depth:** `\section`, `\subsection`, `\subsubsection`, `\paragraph`. No deeper.

**Institutions and programs in `tb_programs_stakeholders.tex`:**
- Individual entries use `\paragraph{Name (location)}`
- Each entry includes a clickable URL preceded by a linebreak and `Website:` label:
  ```latex
  \\ \textbf{Website:} \href{https://...}{https://...}
  ```

---

## README and Markdown style

**Root `README.md`:**
- Short sections only; no detail block longer than one short paragraph
- All detail delegated to sub-folder READMEs or PDFs via links
- Section headers: `##` (H2); no deeper than `###` (H3)

**Sub-folder `README.md` files:**
- Self-contained for their folder's audience
- Include setup commands, file annotations, design rationale
- Same header depth rule: `##` max `###`

**Both:**
- No emoji anywhere in the project
- Code blocks for: directory trees, shell commands, model flow diagrams
- No inline HTML

---

## Notebook style (`.ipynb`)

- Begin with a title markdown cell stating the notebook's purpose and cross-referencing the relevant PDF
- Mathematical specification (ODEs, R₀, parameter table) as markdown cells using MathJax `$$...$$` for display equations
- Code cells follow the markdown spec cells
- No narrative text that belongs in the literature review is duplicated in notebooks
- Notebooks import from `tb_toy_model/src/`; they do not redefine model logic inline

---

## Python code style

From the project's persistent coding rules:
- Explicit, human-readable variable and function names — assume the reader is unfamiliar with the code
- No unnecessary abstractions; keep code readable
- No defensive safeguards unless explicitly requested — fail fast and explicitly
- Prefer single-line comments in the main blocks of long functions
- f-strings for all string formatting
- No auto-generated documentation comments that just restate what the code does

---

## Consistency checkpoints

When making changes, verify these are consistent across the project:
- Tables of contents in both `.tex` files reflect actual section structure
- Root `README.md` folder map matches actual directory layout
- Cross-references between documents (e.g., "see notebook §X", "see §3 of the literature review") point to real sections
- File tree in `ai_approach.tex` §7 reflects actual files present
- Both `.tex` documents use the same MidnightBlue color scheme

---

## Context file conventions

- Stored under `.cursor/context/context_<descriptive_title>.md`
- Referenced at session start with `@.cursor/context/context_<title>.md`
- One file per sub-project or cross-cutting concern
- Contents: purpose, file locations, current state, key decisions, cross-references to related files
