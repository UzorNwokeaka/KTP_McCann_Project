# KTP McCann Backpack PoC Project

This project is a prototype/Proof of Concept user interface for the proposed Backpack software system for J McCann & Co Ltd.

The prototype allows an operative to capture job completion details, including time on site, vehicles, plant/tools, materials used, and work completed. The app calculates an estimated job cost for QS review.

## Features

- Job reference and asset capture
- Time-on-site calculation
- Vehicle, plant/tool, and material cost calculation
- Estimated cost breakdown
- QS-ready job summary
- Basic validation
- Unit tests
- DevOps-ready CI pipeline

## Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run src/app.py
