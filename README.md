# Komplexity — Decision Intelligence

A polished German-language Streamlit application for selecting assembly-complexity assessment methods and documenting operational and economic implications.

## Features

- Eight coded scientific method profiles (M1–M8), with required data classes, maturity, evidence and outputs.
- Technical eligibility gate and explicit professional approval.
- Resource-impact modelling across six resource classes.
- W0 / W1 / W2 evidence-based progression; monetary results only when consumption, rate and verification exist.
- Multi-variant scenario comparison with completeness checks.
- Downloadable, multi-page PDF decision report, including method portfolio, assumptions and cost positions.
- Modern dashboard, German labels and responsive Streamlit layout.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Upload **all** files including `.streamlit/config.toml` to GitHub. Deploy through Streamlit Community Cloud using `app.py` as the main file.

## Technical boundaries

The scientific original formulas for M1–M8 are **not** implemented. Their profiles provide method-selection logic, not substitute complexity scores. Cost computations are real arithmetic (`U × K`) on explicitly documented scenario data; they are not validated causal estimates of complexity costs. The tool does not imply industrial validation or certify economic benefits. Resource cost units must match quantity units, and project users are responsible for source validation. User-entered data is held in the Streamlit session and is not a persistent database.

## Project structure

- `app.py`: user interface and workflows
- `engine.py`: deterministic selection and resource-cost functions
- `methods.json`: method metadata
- `pdf_reports.py`: ReportLab PDF generator
- `.streamlit/config.toml`: theme
- `tests/test_engine.py`: automated checks

## License

Add a suitable LICENSE before public commercial distribution. Review third-party dependencies and the research references underlying method descriptions.
