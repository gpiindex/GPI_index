# GPI Index — 5-Minute Self Check

A Streamlit app that scores everyday habits against the three gunas (Goodness, Passion, Ignorance) and shows a personal reflection.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub (already done if you're reading this on GitHub).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **New app** → select `gpiindex/GPI_index`, branch `main`, main file `app.py` → **Deploy**.

Responses are appended to `responses.csv` on the server (local to the deployed container — it resets on redeploy).
