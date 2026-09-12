# PAVR

**Personalized Adaptive Virtual Reality for Early Cybersickness Prevention with Minimal Experience Disruption**

PAVR is a reproducible closed-loop VR research prototype for early cybersickness-risk estimation and minimum-disruption adaptive intervention.

## Pipeline

`VR telemetry → personalized risk prediction → early warning → intervention selection → adaptive VR → reassessment`

## Included

- synthetic VR telemetry generator
- personalized risk scoring
- minimum-cost intervention controller
- Fixed VR, Threshold-Adaptive VR, and PAVR baselines
- Streamlit dashboard
- automated tests
- GitHub Actions reproducibility workflow
- generated CSV/JSON/report artifacts

## Run

```bash
python -m pip install -r requirements.txt
pip install -e .
pytest -q
python scripts/run_all.py
streamlit run app.py
```

## Scope

Current results are controlled **synthetic computational validation**. They do not establish human-subject efficacy, clinical validity, diagnosis, or deployed-system superiority.

## License

Apache License 2.0

Copyright (C) 2026 Mohammad Amir Khusru Akhtar
