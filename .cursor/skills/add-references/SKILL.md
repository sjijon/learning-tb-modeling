---
name: add-references
description: Look up academic references online and produce complete BibTeX entries with DOIs. Use when the user asks to add a reference, cite a paper, find a DOI, or build a references.bib file.
---

# Add Full References (BibTeX + DOI)

## Scope
Use this skill to add complete BibTeX references with DOIs. Default output is a BibTeX entry appended to `references.bib` at the project root, unless the user specifies another destination.

## Workflow
1. Identify the paper from the user input (title, author, year, venue, keywords).
2. Search for the DOI with `WebSearch`:
   - Query patterns: `"<title>" doi`, `"<title>" crossref`, `<author> <year> <keyword> doi`
3. Resolve metadata:
   - If a DOI is found, fetch `https://doi.org/<doi>` with `WebFetch` and extract canonical metadata.
   - If the DOI is not on the landing page, use metadata from search results to fill fields.
4. Build a complete BibTeX entry with all available fields.
5. Write the entry where the user requests:
   - Append to `references.bib` (create if missing), or
   - Insert into a notebook markdown cell if the user specifies.

## Required fields
Always include:
- `doi`
- `url` as `https://doi.org/<doi>`
- Standard bibliographic fields for the source type:
  - Articles: `author`, `title`, `journal`, `year`, `volume`, `number`, `pages`
  - Conference papers: `author`, `title`, `booktitle`, `year`, `pages`, `publisher` (if available)
  - Books/chapters: `author` or `editor`, `title`, `publisher`, `year`

## Entry type and cite key
- Choose the appropriate BibTeX entry type (`@article`, `@inproceedings`, `@book`, `@incollection`, `@misc`).
- Default cite key: `FirstAuthorLastNameYear` (example: `Vynnycky1997`) unless the user provides a key.

## De-duplication
Before appending, check `references.bib` for the DOI. If it already exists, report the match and skip adding a duplicate entry.

## Output template
```bibtex
@article{FirstAuthorYear,
  author  = {Last, First and Last, First},
  title   = {Full title},
  journal = {Journal Name},
  year    = {2024},
  volume  = {10},
  number  = {3},
  pages   = {100--115},
  doi     = {10.xxxx/xxxxx},
  url     = {https://doi.org/10.xxxx/xxxxx}
}
```

## When search fails
Report what was searched and ask for missing details (exact title, first author, year, venue).
