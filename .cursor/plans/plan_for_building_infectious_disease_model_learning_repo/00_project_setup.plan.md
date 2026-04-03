---
name: "Step 0: Project setup"
overview: Create the workspace skeleton -- anti-hallucination rule, reference and compilation skills, and folder structure. Run this plan first, before any other. Read @project_choices.md before building.
todos:
  - id: hallucination-rule
    content: Create .cursor/rules/avoid-hallucinations.mdc -- a rule that prevents fabricating citations, file contents, or API signatures. The rule should apply automatically to every conversation in the workspace.
    status: pending
  - id: skill-add-references
    content: "Create .cursor/skills/add-references/SKILL.md -- a skill that looks up academic references online, fetches DOI metadata via WebSearch and WebFetch, and appends complete BibTeX entries to references.bib. Trigger: user asks to add a reference, cite a paper, find a DOI, or build a .bib file."
    status: pending
  - id: skill-compile-tex
    content: "Create .cursor/skills/compile-tex-after-save/SKILL.md -- a skill that compiles LaTeX files to PDF using latexmk -pdf -interaction=nonstopmode -file-line-error. Trigger: user says changes are saved/accepted or asks to compile/build PDF."
    status: pending
  - id: folder-skeleton
    content: "Create the folder skeleton based on @project_choices.md: [disease]_overview/ (for LaTeX literature review), [disease]_toy_model/src/ or R/ (for model code), [disease]_toy_model/notebooks/ (for .ipynb or .Rmd), ai_approach/ (if chosen). Create placeholder .gitkeep files so folders are tracked by git."
    status: pending
  - id: gitignore
    content: "Create a .gitignore with standard entries: *.aux, *.log, *.bbl, *.blg, *.fdb_latexmk, *.fls, *.out, *.toc, *.synctex.gz, __pycache__/, .ipynb_checkpoints/, .DS_Store, *.pdf (or not, depending on whether PDFs should be tracked)."
    status: pending
isProject: false
---

# Step 0: Project setup

## What this plan does

Creates the workspace infrastructure that all subsequent plans depend on:

1. An anti-hallucination rule to prevent fabricated citations.
2. Two Cursor skills (reference management and LaTeX compilation).
3. The folder skeleton for the project.
4. A `.gitignore`.

## Prerequisites

- An empty folder opened in Cursor as your workspace.
- LaTeX installed locally (`latexmk`, `pdflatex`).
- Python 3.9+ or R, depending on your choice.
- **Fill in `@project_choices.md` before clicking Build.** The agent reads that file to determine the disease name, language, and folder names.

## After this plan completes

Verify:

- `.cursor/rules/avoid-hallucinations.mdc` exists.
- `.cursor/skills/add-references/SKILL.md` exists.
- `.cursor/skills/compile-tex-after-save/SKILL.md` exists.
- The folder skeleton matches your choices.
- `.gitignore` exists.

Then proceed to `01_literature_review.plan.md`.