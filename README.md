# Planet of Ondoriya — Data Analysis (lab)

## Overview
This repository contains a compact, time-boxed data analysis lab for the Ondoriya dataset. The workflow implemented here:
- Ingest CSV files from a public source into a MinIO data lake (simulates R2).
- Store/query the files with DuckDB using a lightweight lakehouse pattern.
- Present EDA and KPIs via a Streamlit dashboard.

## Part 1 — Data ingestion
Purpose: download the public CSVs and push them into a MinIO bucket so the raw data are centrally available.

How it works
- `src/data_ingestion.py` defines the file list, downloads each file from `BASE_URL`, and uploads it to the configured MinIO bucket using the `minio` client.

## Part 2 — Storage & modeling (DuckLake / DuckDB)
Approach summary
- Keep data files (Parquet preferred) in the data lake and use DuckDB to query them directly. This minimizes ETL and provides a fast, local analytical engine for the dashboard.
- `src/db_sync.py` wires files into the DuckDB catalog (`catalog.ducklake`) and creates convenience views that the dashboard uses.

Why this choice
- Fast analytical queries without managing a separate DB server.
- Works directly against Parquet/CSV in MinIO or local `data/RAW/`.
- Portable and quick to iterate within a 1.5 day timebox.

## Part 3 — EDA & Streamlit dashboard
Implemented KPIs
- Total Population — sum of individuals from the people dataset.
- Dominant Faction — faction with the highest percentage from faction_distribution.

Visualizations
- Population density by region (uses `regions.csv` + `households.csv` / `people`).
- Faction distribution (bar / pie chart).
- Top 5 most populous regions (table + bar chart).

Run the Streamlit app
```bash
streamlit run streamlit/app.py
```

The dashboard queries DuckDB (via the catalog or directly from parquet files) and displays the KPIs and charts.

## Notes
- This lab was implemented in a strict 1.5 day timebox: get things working first; iterate later.
- The code is modular: ingestion, catalog sync, and dashboard are separate to simplify testing and iteration.
