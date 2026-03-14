# Context: TB Literature Review (`tb_overview/modeling_tb`)

This file captures all context needed to work on the literature review document in `tb_overview/`.

---

## Purpose

A standalone LaTeX document providing the epidemiological background, modeling rationale, and economic evaluation framing for the TB toy model project. It is referenced from the toy model notebooks and is compiled to `modeling_tb.pdf`. It is a living document—sections are expected to grow as the project expands.

---

## File locations

```
tb_overview/
  modeling_tb.tex     # main LaTeX source
  modeling_tb.pdf     # compiled output (do not edit directly)
  references.bib      # BibTeX database for this document
  tb_programs_stakeholders.tex / .pdf   # separate document (TB programs overview)
```

---

## Document structure

### Section 1 — TB epidemiology and natural history (`\section{TB epidemiology and natural history}`, `\label{sec:epi}`)

Covers transmission route, latency, disease spectrum, and global burden. Contains three subsections and a TikZ flow diagram.

**1.1 Intro paragraphs** (no subsection heading)
- Airborne transmission, latency, 5–10% fast progression rule
- Global burden, HIV co-infection, latent reservoir (~1/4 of global population)

**1.2 `\subsection{Current global burden and regional distribution}`**
- 2024 global figure: 10.7 million new cases, 131 per 100,000
- Top-8 countries by share of global cases
- `\ref{tab:who_region_2024}` — exact 2024 incidence by WHO region (from GTB 2025)

| WHO Region | New cases (thousands) | Rate per 100,000 |
|---|---|---|
| South-East Asia | 3,680 | 201 |
| Western Pacific | 2,910 | 131 |
| Africa | 2,620 | 207 |
| Eastern Mediterranean | 920 | 112 |
| Americas | 350 | 33 |
| Europe | 204 | 22 |
| **Global** | **10,700** | **131** |

> Note: Indonesia was reclassified from SEAR to WPR by WHA Resolution 78 (2025). This affects comparability of SEAR and WPR figures with all earlier WHO report editions.

**1.3 `\subsection{Twenty-year trend in global incidence}`**
- Decline since ~2000; End TB Strategy baseline 2015 ≈ 142/100k; target −50% by 2025
- `\ref{tab:global_trend}` — approximate 5-year benchmark table 2005–2024:

| Year | Rate per 100,000 | New cases (millions) |
|---|---|---|
| 2005 | ≈179 | — |
| 2010 | ≈160 | — |
| 2015 | ≈142 | ≈10.4 |
| 2019 | ≈130 | ≈10.0 |
| 2020 | 127 (exact) | 9.9 (exact) |
| 2022 | ≈133 | ≈10.6 |
| 2024 | 131 (exact) | 10.7 (exact) |

  Pre-2015 values are approximate; case counts before 2015 omitted because of retrospective upward revisions.
- COVID-19 disruption: diagnosed cases fell 7.1M (2019) → 5.8M (2020); estimated incidence rose 4.6% from 2020–2023 (peak 10.8M in 2023); reversed in 2024
- Regional 2015–2024 changes: Europe −39%, Africa −28%, SEAR −16%, EMR −5.9%, WPR +1.7%, Americas +13%
- Prevalence note: global active TB prevalence ≈ 1.5–2× incidence count; requires national surveys; not reported by region in this document

**1.4 Remaining natural history paragraphs** (no subsection)
- Untreated duration ~3 years; high case fatality in smear-positive (Tiemersma 2011)
- Disease spectrum: minimal / subclinical / clinical (Richards 2023, Kendall 2021)

**1.5 TikZ flow diagram** (`\begin{figure}[h]`) — `\label{fig:tb_flow}`
- Compartments: S, L_fast, L_slow, I, T, R, D
- Arrows: infection, fast progression, slow reactivation, treatment, self-cure, TB mortality, relapse, reactivation
- Caption: "Simplified TB natural history used for the toy model."

---

### Section 2 — Mathematical modeling approaches (`\section{Mathematical modeling approaches for TB}`)

Intro: ODE compartmental models as entry point; two-speed latency; R0 via next-generation matrix; deterministic vs stochastic tradeoffs.

**2.1 `\subsection{Stochastic ODE models and uncertainty analysis}`**
- Blower et al. 1995: Monte Carlo + ODE → probabilistic epidemic trajectories
- TB epidemics evolve over decades to centuries
- PRCC sensitivity analysis for R0 / incidence uncertainty

**2.2 `\subsection{Extended compartmental models with drug resistance and reinfection}`**
- Trauer et al. 2014: 10-compartment ODE for Asia-Pacific high-burden settings
- Key additions: declining hazard post-infection, reinfection, MDR-TB strain with fitness cost + de novo resistance, vaccine compartment
- Key finding: model could not fit data without reinfection during latency; MDR-TB dominates at equilibrium under most parameterizations

**2.3 `\subsection{Individual-based and microsimulation models}`**
- Goodell et al. 2019: discrete-time stochastic microsimulation, California
- Individual attributes: age, race/ethnicity, nativity, medical risk factors
- Semi-random mixing by nativity group; calibrated 2001–2014
- Enables cost-per-QALY by targeted subgroup; models WHO pre-elimination threshold (<10 cases/million)
- Trade-off: higher compute cost and data requirements vs ODE

---

### Section 3 — Economic evaluation approaches (`\section{Economic evaluation approaches for TB}`)

- Three frameworks: CEA, CUA, BIA
- ICER formula: ΔCost / ΔHealth outcome
- TB uses DALYs (WHO convention); threshold ~1–3× per-capita GDP (contested)
- Dynamic transmission models often coupled with cost modules because interventions reduce downstream transmission
- Menzies et al. 2012: Xpert MTB/RIF in 5 southern African countries; 132k cases and 182k deaths averted over 10 years; ~$959/DALY; unexpected large cost driver = ART for HIV+ survivors
- BIA vs CEA: BIA asks "can we afford it?" not "is it worth it?" — complementary roles

---

### Section 4 — The SELT(R) model used in this project (`\section{The SELT(R) model used in this project}`)

- Deterministic ODE, 6 state variables (S, L_fast, L_slow, I, T, R)
- Rationale: two-speed latency, self-cure, treatment modifies infectious duration, TB-excess mortality
- Compartment list with biological interpretation
- Cross-reference to notebook `01_tb_model.ipynb` for full ODE system, R0 expression, and parameter table

---

## References (`references.bib`)

All cite keys and their roles in the document:

| Cite key | Reference | Used for |
|---|---|---|
| `vynnycky1997natural` | Vynnycky & Fine, *Epidemiology and Infection* 1997 | Latency / two-speed progression / fast–slow split; ODE model rationale |
| `who2025global` | WHO Global Tuberculosis Report 2025 | Global burden data; 2024 regional incidence; 20-year trend; COVID disruption |
| `houben2016latent` | Houben & Dodd, *PLOS Medicine* 2016 | ~1/4 global population latently infected |
| `tiemersma2011natural` | Tiemersma et al., *PLOS ONE* 2011 | Untreated TB duration ~3 years; case fatality; anchor for δ and γ parameters |
| `kendall2021subclinical` | Kendall et al., *AJRCCM* 2021 | Epidemiological importance of subclinical TB |
| `richards2023spectrum` | Richards et al., *Lancet Global Health* 2023 | TB disease spectrum (minimal / subclinical / clinical) |
| `diekmann1990r0` | Diekmann et al., *J Math Biol* 1990 | Next-generation matrix method for R0 |
| `blower1995dynamics` | Blower et al., *Nature Medicine* 1995 | Stochastic ODE + uncertainty analysis; epidemic timescales; PRCC |
| `trauer2014construction` | Trauer et al., *J Theoretical Biology* 2014 | Extended ODE with MDR-TB, reinfection, declining hazard, vaccine |
| `goodell2019california` | Goodell et al., *PLOS ONE* 2019 | Individual-based microsimulation; policy evaluation; cost-per-QALY |
| `menzies2012xpert` | Menzies et al., *PLOS Medicine* 2012 | Dynamic model + cost-effectiveness; DALYs; Xpert MTB/RIF evaluation |

---

## LaTeX setup

- Class: `article`, 11pt, 1-inch margins
- Key packages: `amsmath`, `booktabs`, `longtable`, `graphicx`, `xcolor` (dvipsnames), `tikz` + `arrows.meta` + `positioning`, `hyperref` (MidnightBlue links), `natbib`, `siunitx`
- Bibliography style: `plainnat`; bibliography file: `references`
- Compile command (from `tb_overview/`):
  ```
  latexmk -pdf -interaction=nonstopmode -file-line-error modeling_tb.tex
  ```

---

## Conventions

- All WHO incidence data cited as `\citep{who2025global}` regardless of which report edition the specific data point comes from, unless a different year's edition is the more direct source.
- Approximate values in tables use `$\approx$` prefix; exact values have no prefix.
- Regional figures for 2024 onward reflect Indonesia in WPR (post-WHA78 reclassification). When discussing 2020 or earlier data, Indonesia was in SEAR — note this in context when comparing across years.
- The document uses `{,}` for thousands separators in math mode (e.g., `10{,}700`).
- New sections added to this document should also be reflected here.

---

## Related files

| File | Role |
|---|---|
| `tb_overview/references.bib` | BibTeX source; append new entries here |
| `tb_toy_model/notebooks/01_tb_model.ipynb` | Implements the SELT(R) model documented in Section 4 |
| `tb_overview/tb_programs_stakeholders.tex` | Companion document on TB programs and stakeholders (separate compilation) |
| `.cursor/context/context_toy_model.md` | Context for the toy model implementation |
| `.cursor/context/context_ai_approach.md` | Context for the AI approach document |
