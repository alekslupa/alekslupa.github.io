# alekslupa.github.io

Source code for my personal ePortfolio, built with [Quarto](https://quarto.org/), version-controlled with Git, and deployed via GitHub Pages.

**Live site:** [alekslupa.github.io](https://alekslupa.github.io)

---

## What's in here

A first-year BA Business Studies portfolio at Dublin City University, combining academic project work across business strategy, data analytics, machine learning and new enterprise development with personal sections for competitive bodybuilding and hiking across Ireland.

Most charts on the project pages are generated from live Python code that re-executes at render time via Quarto's `freeze: auto` mechanism, so the visualisations are always in sync with the underlying analysis. The Ireland section uses D3.js to render an interactive county-level map from a GeoJSON source file — the same separation-of-data-from-presentation principle that runs through the rest of the site.

---

## Tech stack

| Tool | Purpose |
|------|---------|
| **Quarto** | Static site generator — renders `.qmd` files to HTML |
| **Python** | Live chart execution (Plotly, pandas, scikit-learn) |
| **SCSS** | ~4,400-line custom theme on top of Bootstrap `cosmo` / `darkly` |
| **D3.js** | Interactive Ireland county map |
| **Git + GitHub Pages** | Version control and free hosting via `docs/` output |
| **Mermaid** | Pipeline and architecture diagrams |
| **Font Awesome** | Icons via Quarto extension |

---

## Repository structure

```
.
├── _quarto.yml                  # Site config — navbar, resources, theme
├── styles.scss                  # All site-wide custom SCSS (~4,400 lines)
├── back-to-top.html             # Injected footer partial
├── index.qmd                    # Landing page
├── about.qmd                    # About — skills, languages, beyond-work
├── achievements.qmd             # Achievements timeline
├── future_goals.qmd             # Career goals page
├── ireland.qmd                  # Interactive D3 county map (full-page layout)
├── 404.qmd                      # Custom 404 page
├── .gitignore
├── .nojekyll
│
├── ireland/                     # Hiking diary sub-pages (one per county)
│   ├── wicklow.qmd
│   ├── donegal.qmd
│   ├── sligo.qmd
│   ├── mayo.qmd
│   └── down.qmd
│
├── projects/
│   ├── index.qmd                # Filterable projects hub
│   ├── projects.yml             # Manual listing data for the hub page
│   └── list/                   # Individual project pages (one .qmd each)
│       ├── eportfolio.qmd       # BAA1028 — this site, self-analysing
│       ├── pricebeo.qmd         # BAA1003 — grocery price comparison app
│       ├── ml-python.qmd        # BAA1027 — online shoppers ML analysis
│       ├── data-analytics.qmd   # BAA1026 — EcoEnergy Corp Power BI project
│       ├── superdry.qmd         # BAA1019 — strategic consulting report
│       ├── critical-thinking.qmd# SB202  — remote work research design
│       ├── applegreen.qmd       # SB104  — app innovation group project
│       ├── fitness.qmd          # Personal — bodybuilding journey log
│       ├── vip-ireland.qmd      # Personal — WordPress client site
│       └── bathstore.qmd        # Personal — WordPress client site
│
├── assets/
│   ├── ireland-counties.geojson # GeoJSON source for the D3 map
│   ├── hikes/                   # Hike photography, organised by county
│   │   ├── wicklow/
│   │   ├── donegal/
│   │   ├── sligo/
│   │   └── mayo/
│   └── pdfs/                   # Downloadable project reports and slides
│
├── images/                      # Site images (profile, logos, project cards)
│
├── cv/
│   └── Aleksander_Lupa_CV.pdf
│
├── data/                        # CSV outputs from generate_repo_stats.py
│   ├── commits_over_time.csv
│   ├── file_inventory.csv
│   ├── scss_growth.csv
│   └── top_edited_files.csv
│
├── scripts/
│   └── generate_repo_stats.py   # Walks git history + file tree, writes data/
│
├── _freeze/                     # Frozen Python execution results (committed)
├── _extensions/
│   └── quarto-ext/fontawesome/
└── docs/                        # Build output (served by GitHub Pages)
```

---

## Pages with live Python

These pages execute Python chunks at render time and use `freeze: auto` to cache results so GitHub Pages can serve them without a CI Python environment:

- `projects/list/eportfolio.qmd` — repo commit history, file inventory, SCSS growth, most-edited files
- `projects/list/pricebeo.qmd` — market share, primary research findings, revenue model, user growth projections
- `projects/list/ml-python.qmd` — classifier benchmark, overfitting comparison, cost-sensitive threshold analysis, feature importance
- `projects/list/data-analytics.qmd` — regional profitability scorecard, Asia deep-dive, outsourcing strategy, predictive forecast
- `projects/list/superdry.qmd` — revenue history, Porter's Five Forces radar, value stick, SWOT, strategy roadmap

---

## A few things worth knowing

- **The ePortfolio page analyses itself.** `scripts/generate_repo_stats.py` walks the actual Git history and file tree, writes four CSVs to `data/`, and `eportfolio.qmd` reads those CSVs at render time. The charts show real repository metrics, not estimates.
- **The Ireland map** (`ireland.qmd`) loads county boundaries from `assets/ireland-counties.geojson` at page load via D3. The clickable counties are declared in a single JavaScript object at the top of the script — adding a new hiking entry is a one-line change plus a new sub-page.
- **Dark mode** is fully supported. The SCSS defines a parallel set of CSS custom properties under `.quarto-dark` for every custom component. Inline SVG diagrams carry their own embedded `<style>` blocks with `.quarto-dark` overrides so they adapt without JavaScript.
- **Frozen execution** (`_freeze/`) is committed to the repo. GitHub Pages serves static HTML from `docs/` with no build step, so freezing Python outputs locally and committing them is what makes the live charts reproducible on the deployed site.
- **PDF assets** live in `assets/pdfs/` rather than alongside images. The `_quarto.yml` resources list ensures they are copied into `docs/assets/pdfs/` at render time.

---

## Local development

```bash
# Render the full site
quarto render

# Live preview with hot reload
quarto preview

# Render a single page (uses frozen outputs for Python chunks)
quarto render projects/list/ml-python.qmd

# Regenerate the repo stats CSVs before rendering the ePortfolio page
python scripts/generate_repo_stats.py
quarto render projects/list/eportfolio.qmd
```

---

## Deployment

GitHub Pages serves from the `docs/` folder on the `main` branch. After any change:

```bash
quarto render
git add .
git commit -m "Descriptive message"
git push
```

The live site updates within 30–60 seconds. `.nojekyll` at the repo root tells GitHub Pages to skip Jekyll processing and serve Quarto's output as-is.

---

## Author

**Aleksander Lupa**
BA Business Studies — Dublin City University (Year 1)

[LinkedIn](https://www.linkedin.com/in/alekslupa/) · [GitHub](https://github.com/alekslupa)

---

*Built with [Quarto](https://quarto.org/) · Managed with Git · Published on GitHub Pages*
