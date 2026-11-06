# CogniStream dashboard

## Run locally

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\dashboard\requirements.txt
.\.venv\Scripts\python.exe -m streamlit run .\dashboard\app.py
```

The dashboard opens in the browser and reads:

```text
data/processed/ai_dev_productivity_cleaned.csv
```

Use the sidebar to filter task outcome and cognitive-load group. The dashboard
shows KPI cards, success-rate comparisons, cognitive-load signals, and a
selectable feature comparison.
