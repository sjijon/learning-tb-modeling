---
name: "Step 3: Documentation"
overview: Write the root README, model sub-folder README, optional stakeholder document, and context files. Read @project_choices.md for the disease and optional components.
todos:
  - id: root-readme
    content: "Write README.md at the project root. Include: project title and purpose, goals (learn [DISEASE], learn modeling, build toy model, use AI agents), project structure with a directory tree, one-paragraph summary of each component with links to relevant files. Keep it short -- delegate details to sub-folder READMEs and PDFs."
    status: pending
  - id: model-readme
    content: "Write [disease]_toy_model/README.md. Include: model description (compartments, flow diagram, ODE summary), file annotations for src/ and notebooks/, setup commands (pip install or R equivalent), design decisions and rationale. This is the reference doc for anyone working with the code."
    status: pending
  - id: stakeholder-doc
    content: "(Optional -- check @project_choices.md) Write [disease]_overview/[disease]_programs_stakeholders.tex covering: major institutions and funders, ongoing prevention programs, current and pipeline treatments, elimination or control targets, academic groups using mathematical models for [DISEASE]. Use the same LaTeX style as the literature review (MidnightBlue links, 11pt article, 1-inch margins). Compile to PDF."
    status: pending
  - id: context-model
    content: "Create .cursor/context/context_toy_model.md consolidating: model structure, ODE system, R0 formula, parameter table, src/ API, notebook outlines, design decisions, setup commands. Read all source files before writing."
    status: pending
  - id: context-litreview
    content: "Create .cursor/context/context_literature_review.md consolidating: document purpose, file locations, section structure, reference list, LaTeX conventions, compile command."
    status: pending
  - id: context-consistency
    content: "Create .cursor/context/context_consistency.md consolidating: canonical file tree, cross-references between documents, naming conventions, known issues."
    status: pending
isProject: false
---

# Step 3: Documentation

## What this plan does

Creates all the documentation that ties the project together: READMEs, an optional stakeholder document, and context files for future conversations.

## Prerequisites

- `02_toy_model.plan.md` completed (model code and notebooks exist).
- `@project_choices.md` filled in (especially "Include stakeholder document?" and disease name).

## What the agent reads

Attach `@project_choices.md` when clicking Build. The agent should also read the existing literature review, model code, and notebooks to write accurate documentation.

## After this plan completes

Verify:
- `README.md` exists at project root with correct directory tree and links.
- `[disease]_toy_model/README.md` exists with model details.
- If stakeholder document was requested: `[disease]_overview/[disease]_programs_stakeholders.tex` exists and compiles.
- Context files exist in `.cursor/context/`.
- All cross-references between documents point to real files with correct names.

Then proceed to `04_ai_approach.plan.md` (if chosen in project_choices.md).
