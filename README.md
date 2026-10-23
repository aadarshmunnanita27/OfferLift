# OfferLift

An independent data-science portfolio project. Not affiliated with CRED. The deployed static app runs real exported model inference in the browser; it is not a live banking integration.

## Quick start

Use Python 3.11 or 3.12:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

On Windows, activate with `.venv\Scripts\activate` instead. The included trained model and `dist/data.json` let you run immediately, without retraining. Load only trusted joblib files.

## Reproduce training

```bash
python train.py
```

Or pass your dataset: `python train.py --data /path/to/hillstrom.csv`.
Training writes model.joblib, metrics.json, split.npz, dist/data.json and dist/sample.csv. Keep library versions pinned to reproduce serialization and outputs. The raw input SHA-256 is recorded in metrics.json. Random seed is 42. Full training data is fetched on demand, not included.

## Deploy to Streamlit Community Cloud

Create your own GitHub repository, upload this project's files, and connect it to Streamlit Community Cloud. Select `streamlit_app.py` and Python 3.11 or 3.12. Include model.joblib and dist/data.json. The Community Cloud publication requires your own connected account; no deployment there has been claimed.

## Run the browser app locally

```bash
python -m http.server 8000 --directory dist
```

Open http://localhost:8000. `dist/index.html`, `dist/app.js`, and `dist/data.json` are sufficient for the interactive model app. There is no API key or paid model dependency.

## Project structure

- train.py: data acquisition, preprocessing, splits, training and evaluation
- streamlit_app.py: portable Python dashboard and CSV scoring
- dist/: hosted browser application, exported models and held-out rows
- analysis.sql + run_sql.py: reproducible SQL segment analysis
- model.joblib: trained Python estimators
- metrics.json: measured results
- split.npz: original row indices for reproducibility
- INTERVIEW_GUIDE.md: explanation, Q&A, limitations and practice changes
- EXPERIMENTS.md: actual experimental record
- validate.js: browser model parity and application-render checks

## Data and attribution

Kevin Hillstrom, MineThatData E-Mail Analytics and Data Mining Challenge (2008). https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html . Download fallback: W-Tran/uplift-modelling on GitHub, original CSV filename. Dataset attribution remains with Kevin Hillstrom; review original usage terms before redistribution. Only the held-out subset needed for this educational demonstration is bundled in the browser export.

## Limitations

Uplift ranking failed to beat random targeting on this held-out sample. Do not claim business lift from the targeting model. Two independent models produce noisy differences with rare conversions. Bootstrap intervals condition on trained models and omit training uncertainty. Profit uses assumed margin and contact cost, not measured campaign profit. Email results do not generalize automatically to cashback or CRED users.

## Ownership and interview use

Study and modify the project before describing it as your work. Keep a genuine experiment log and disclose AI assistance honestly if asked. No production experience, customer impact, or commercial affiliation is implied. Resume language should use only measured results and features you can explain.

## Verification

Run `node validate.js` to compare browser inference against all held-out Python predictions and exercise rendering functions and sample CSV parsing. Both Streamlit apps passed AppTest startup with no exceptions. These checks do not replace visual browser QA, which was unavailable.
