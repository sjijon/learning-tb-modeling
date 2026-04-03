---
name: "Step 4: AI approach documentation"
overview: Document how AI agents were used to build this project -- the skills, plans, agents, prompts, and observations. This step is optional (check @project_choices.md). Read existing conversation transcripts and project files before writing.
todos:
  - id: write-ai-tex
    content: "Create ai_approach/ai_approach.tex documenting: (1) Overview -- project goal, tools used (Plan mode, Agent mode, Skills, Context files), (2) Planning -- initial prompt and plan refinement, (3) Agents used -- Plan mode vs Agent mode behaviors, (4) Skills created -- add-references and compile-tex-after-save, with the prompts that created them, (5) Prompts by component -- verbatim prompts for literature review, model, code, documentation in longtable format, (6) Style instructions -- organizational decisions, LaTeX/README/notebook conventions, (7) Observations -- what worked, what didn't. Use same LaTeX style: 11pt article, 1-inch margins, MidnightBlue links."
    status: pending
  - id: compile-ai-pdf
    content: "Compile ai_approach/ai_approach.tex to PDF using latexmk. Fix any compilation errors."
    status: pending
  - id: context-ai
    content: "Create .cursor/context/context_ai_approach.md consolidating: document structure, section list, scope, style conventions, cross-references."
    status: pending
  - id: update-root-readme
    content: "Add a section about the AI approach to the root README.md, with a link to ai_approach/ai_approach.pdf."
    status: pending
  - id: update-consistency
    content: "Update .cursor/context/context_consistency.md with the new ai_approach/ files and any new cross-references."
    status: pending
isProject: false
---

# Step 4: AI approach documentation

## What this plan does

Creates a LaTeX document recording how the project was built using AI agents. This is a meta-documentation artifact -- useful for portfolios and for understanding the AI-assisted workflow.

## Prerequisites

- All previous plans completed (the project is fully built).
- `@project_choices.md` has "Include AI approach documentation?" set to "yes".
- Conversation transcripts are available in `.cursor/agent-transcripts/` (the agent reads these to extract verbatim prompts).

## What the agent reads

Attach `@project_choices.md` and all context files when clicking Build. The agent should also read:
- Agent transcript files to extract verbatim prompts.
- Both skill SKILL.md files.
- The plan files from previous steps.

## After this plan completes

Verify:
- `ai_approach/ai_approach.tex` exists and compiles to PDF.
- The prompts documented match what actually happened.
- The root README mentions the AI approach folder.
- `context_consistency.md` is up to date with the full file tree.

The project is now complete.
