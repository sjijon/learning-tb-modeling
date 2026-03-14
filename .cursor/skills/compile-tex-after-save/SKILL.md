---
name: compile-tex-after-save
description: Compile LaTeX .tex files after the user says changes are saved/accepted. Use when the user asks to compile TeX, build a PDF, or says changes are saved and wants a build.
---

# Compile TeX After Save

## Defaults
- Main file: `tb_overview/modeling_tb.tex`
- Compile command: `latexmk -pdf -interaction=nonstopmode -file-line-error <main>.tex`

## When to run
Run after the user explicitly says they saved/accepted changes or asks to compile/build the PDF.

## Workflow
1. Confirm the main `.tex` file path (use default unless the user specifies another).
2. Run the compile command from the main file's directory:
   - `latexmk -pdf -interaction=nonstopmode -file-line-error <main>.tex`
3. Report the compile result and the PDF output path.

## Example
User: "I saved changes to modeling_tb.tex, compile it."
Action:
`cd tb_overview && latexmk -pdf -interaction=nonstopmode -file-line-error modeling_tb.tex`
