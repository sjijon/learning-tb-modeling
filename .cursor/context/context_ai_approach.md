# Context: ai_approach/

## What this folder is
Meta-documentation of how AI agents were used to build the TB modeling project. Written as a LaTeX document intended for a portfolio or methods section. It is **descriptive, not prescriptive** — it records what happened, not instructions for future work.

## Files
- `ai_approach/ai_approach.tex` — main document (473 lines), compiled to `ai_approach.pdf`
- No `references.bib`; all citations are inline or none

## Document structure (sections)
1. **Overview** — project goal, tools used (Plan mode, Agent mode, Skills), transcript UUIDs
2. **Planning the project** — initial prompt, plan refinement prompts, plan contents (5 to-dos)
3. **Agents used** — Plan mode, Agent mode, tooling agent (second conversation) behaviors
4. **Cursor Skills created** — `add-references` and `compile-tex-after-save`, workflow details
5. **Prompts by project component** — verbatim prompts per deliverable (literature review, model architecture, code, documentation) as longtables
6. **Style instructions** — project organization decisions, LaTeX/README/notebook conventions
7. **Observations** — what worked well, limitations
8. **Project file tree** — full directory tree of the project

## Key design decisions recorded here
- LaTeX for narrative, notebooks exclusively for computation (prompted explicitly)
- `modeling_tb.tex` splits into biological rationale (tex) vs. ODE spec (notebook)
- Root README = entry point only; sub-folder READMEs = reference docs
- Link color: MidnightBlue via `xcolor` + `hyperref` (applied to both `.tex` documents)
- No emoji anywhere in the project

## LaTeX conventions in this file
- `\documentclass[11pt]{article}`, `\usepackage[margin=1in]{geometry}`
- Prompts displayed in custom `promptbox` environment (gray-background `mdframed`)
- Tables use `longtable` + `booktabs`; two-column layout (prompt | effect)
- Verbatim blocks use `Verbatim` from `fancyvrb` (file tree, code snippets)
- No `natbib`/bibliography; no `\cite` calls

## Current state
- Document is complete and compiled to PDF
- Covers everything up to and including the style instructions session
- The file tree in §7 does **not** include `.cursor/context/` — update it if that matters

## Cross-references to other parts of the project
- Transcripts referenced: `196c0a38-2551-4c17-9159-dae423d48a45`, `b0a3a5d5-9dff-4db2-861e-9fc242971a2e`
- Plan file: `.cursor/plans/tb_modeling_learning_project_1d0fe19d.plan.md`
- Skills described: `.cursor/skills/add-references/SKILL.md`, `.cursor/skills/compile-tex-after-save/SKILL.md`
- Described deliverables live in: `tb_overview/`, `tb_toy_model/`, `README.md`
