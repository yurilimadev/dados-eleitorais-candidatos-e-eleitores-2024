# AGENTS.md

Streamlit app (Portuguese UI) analyzing Brazilian TSE election data (candidates + voters), designed to be updated across municipal and federal elections. No lint config, no CI — don't invent any. Tests exist: `python -m pytest tests/`.

## Run

```bash
pip install -r requirements.txt
streamlit run main.py
```

## Architecture

- `main.py` renders a selectbox and lazily imports pages from `my_pages/` (`app_eleitores`, `app_candidatos`).
- `dados_eleitorais/` is the deep module at the data seam; pages are thin renderers:
  - `ingestao.py`: `carregar_candidatos(anos, tipo_eleicao, base_dir)` / `carregar_eleitores(base_dir)`. Owns all TSE conventions (`sep=';'`, `encoding='latin-1'`, `decimal=','`), dtype dicts, and **`ELEICOES`** — the election registry. A new election (municipal or federal) is one entry in `ELEICOES`; pages and tests never mention filenames. Error mode: unknown year/type or missing schema columns raise `ValueError` listing what's available.
  - `calculo.py`: pure DataFrame→DataFrame functions (counts, rankings, year diffs, per-UF summary) used by both pages.
  - `localidades.py`: single source of UF + foreign-city (ZZ) coordinates for the Folium maps (was duplicated across both pages; root `cidades_zz.py` deleted).
- No data loads at module import time anymore; pages wrap loaders in `@st.cache_data`. Importing `app_candidatos` no longer triggers the Eleitores load.

## Data / gotchas

- **Git LFS required.** `*.csv`, `*.parquet`, `*.zip` are LFS-tracked; a plain clone leaves 134-byte pointer stubs. Real CSVs are ~145 MB. Run `git lfs install && git lfs pull` before running the app with real data.
- Tests do NOT need LFS: `tests/fixtures/` holds synthetic mini-CSVs (36 candidate columns, 19 RAE columns, same TSE format — note `decimal=','`, so float values must be written with comma decimals).
- `parquet/` files were produced by `csv-para-parquet.ipynb` (EDA, not the official pipeline). The candidatos parquet has only 12 columns; the RAE parquet lacks `DT_GERACAO` and all `DS_*` columns — **neither parquet is loadable by the app as-is**. The app reads the full CSVs via `carregar_*`.
- `requirements.txt` pins pandas 2.2.2 / numpy 1.26.4 for compatibility with the pinned matplotlib 3.6.2 + streamlit 1.38 (Streamlit Cloud target).

## Repo quirks

- `__pycache__/`, `.ipynb_checkpoints/`, and a `dados-eleitorais-candidatos-e-eleitores-2024.git/` bare-clone directory are **tracked in git** (`.gitignore` doesn't cover them). Don't treat their contents as intentional code.
- UI text, comments, column names, and new module names are in Portuguese; keep that convention.
- Deploys via Streamlit Cloud (streamlit.app); main branch is what's live.
- `CONTEXT.md` is the domain glossary (Eleição, Perfil, Ingestão, Cálculo, Localidade…); keep new domain terms there.
