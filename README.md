# Backpack Operational Platform

### Street Lighting Job Cost Capture & QS Cost Visibility System

---

## Project Overview

Backpack Operational Platform is a prototype operational optimisation application developed as part of the Knowledge Transfer Partnership (KTP) interview exercise between **J. McCann & Co. Ltd** and the **University of Suffolk**.

The system provides a structured workflow for capturing street lighting maintenance activities completed by field Operatives and automatically generating estimated job costs for review by Quantity Surveyors (QS). The platform aims to improve operational visibility, cost transparency, data quality, and decision-making across the Suffolk Street Lighting Contract.

The prototype demonstrates how digital technologies can replace paper-based or spreadsheet-driven processes with a modern cloud-based application that supports operational reporting, auditability, and future analytics capabilities.

---

## Business Problem

J. McCann & Co. Ltd manages a large portfolio of street lighting assets across Suffolk.

Following completion of maintenance activities, the business requires improved visibility of:

* Time spent on site
* Labour utilisation
* Vehicles used
* Plant and equipment usage
* Materials consumed
* Work completed
* Estimated operational costs

Historically, this information may be distributed across multiple systems, forms, or manual processes, making commercial review and operational reporting more challenging.

The Backpack Operational Platform addresses this challenge by providing a centralised workflow for job capture and cost visibility.

---

## Solution Overview

The prototype consists of two primary components:

### Operative Operational Platform

Used by field Operatives to:

* Record completed maintenance jobs
* Capture job details and asset information
* Record labour, vehicles, tools, and materials used
* Calculate estimated job costs
* Submit records to a central database

### QS Operational Dashboard

Used by Quantity Surveyors and operational managers to:

* Review submitted jobs
* Monitor estimated costs
* Analyse cost trends
* Review work completion records
* Access audit logs
* Support commercial decision-making

---

## Key Features

### Operative Job Capture

* Operative Name
* Employee Number
* Job Reference
* Asset ID
* Location
* Job Type
* Arrival Time
* Departure Time
* Number of Operatives

### Resource Tracking

* Vehicle Usage
* Plant / Tool Usage
* Tool Hours
* Materials Used
* Labour Utilisation

### Automated Cost Calculation

Calculates:

* Labour Cost
* Vehicle Cost
* Plant / Tool Cost
* Material Cost
* Total Estimated Job Cost

### Validation Rules

* Mandatory field validation
* Arrival/Departure time validation
* Tool usage validation
* Data quality controls

### PostgreSQL Data Persistence

Stores:

* Job records
* Cost calculations
* Operative details
* Audit records

### QS Dashboard

Provides:

* Operational Performance Summary
* Job Register
* Detailed Cost Records
* Work Completion Records
* Cost Analysis by Job Type
* Cost Component Analysis
* Audit Trail

### Accessibility

* High-contrast visual design
* White background
* Black text
* Improved readability
* Accessible user interface

---

## System Architecture

```text
Operative User
      │
      ▼
Streamlit Operative App
      │
      ▼
Business Logic Layer
(Cost Calculation & Validation)
      │
      ▼
SQLAlchemy ORM
      │
      ▼
PostgreSQL Database
      │
      ▼
QS Dashboard
      │
      ▼
Operational Reporting & Analysis
```

---

## Technology Stack

### Frontend

* Streamlit

### Backend

* Python 3.11
* SQLAlchemy

### Database

* PostgreSQL
* SQLite (local development)

### Data Processing

* Pandas

### Testing

* Pytest

### Code Quality

* Black
* Ruff

### CI/CD

* GitHub Actions

### Hosting

* Render

### Version Control

* Git
* GitHub

---

## Project Structure

```text
KTP_McCann_Project/
│
├── assets/
│   └── jmccann_logo.png
│
├── src/
│   ├── app.py
│   ├── db.py
│   └── pages/
│       └── 1_QS_Dashboard.py
│
├── tests/
│   └── test_app.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .streamlit/
│   └── config.toml
│
├── requirements.txt
├── runtime.txt
├── pytest.ini
├── .gitignore
└── README.md
```

---

## Local Installation

### Clone Repository

```bash
git clone https://github.com/UzorNwokeaka/KTP_McCann_Project.git

cd KTP_McCann_Project
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

### Start Operative App

```bash
streamlit run src/app.py
```

---

## Running Tests

### Execute Unit Tests

```bash
pytest
```

### Run Linting

```bash
ruff check src tests
```

### Run Formatting

```bash
black src tests
```

---

## Continuous Integration

The project includes a GitHub Actions workflow that automatically executes:

* Dependency installation
* Code formatting validation
* Linting checks
* Unit tests

The workflow runs on:

* Push to main
* Pull Requests

---

## Deployment

The application is deployed using Render.

### Deployment Components

#### Web Service

Hosts:

* Operative Operational Platform
* QS Operational Dashboard

#### PostgreSQL Database

Stores:

* Job submissions
* Cost records
* Audit logs

Environment variables are managed securely through Render.

---

## Future Enhancements

Potential future development areas include:

### Operational Optimisation

* Work order management
* Engineer scheduling
* Asset lifecycle management
* SLA monitoring

### Geospatial Intelligence

* GIS integration
* Asset mapping
* Route optimisation

### Advanced Analytics

* KPI monitoring
* Operational dashboards
* Trend analysis

### Artificial Intelligence

* Predictive maintenance
* Asset failure prediction
* Resource optimisation
* Cost forecasting

### Security

* User authentication
* Role-based access control
* Multi-user permissions

### Enterprise Deployment

* Docker containerisation
* Infrastructure as Code
* Monitoring and observability
* Automated backups

---

## Author

**Uzordinma Malcolm Nwokeaka**

AI/ML Engineer | Software Engineer | Analytics Engineer

GitHub:
https://github.com/UzorNwokeaka

LinkedIn:
https://linkedin.com/in/uzornwokeaka

---

## Disclaimer

This repository contains a prototype developed as part of a Knowledge Transfer Partnership (KTP) interview exercise. The solution demonstrates the proposed technical approach and is intended as a proof-of-concept rather than a production-ready implementation.
