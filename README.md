# Carbon Footprint Estimation System (ESG Analytics)

An end-to-end Carbon Footprint Estimation System built with Python and SQL to calculate Scope 1, 2, and 3 emissions adhering to the GHG Protocol Corporate Standard and EPA/DEFRA methodologies.

## 📊 Dashboard Preview
!<img width="1920" height="1020" alt="Screenshot 2026-04-14 110839" src="https://github.com/user-attachments/assets/7af9adee-399a-466d-b819-990e08463058" />

*Professional executive view with GHG Scope breakdown and monthly trends.*

!
<img width="1920" height="1020" alt="Screenshot 2026-04-14 110713" src="https://github.com/user-attachments/assets/745520ec-175e-4a0b-9ccd-c77effe5814e" />

*Interactive "What-If" analysis tool for strategic decarbonization planning.*

## Features
- **Data Pipeline**: Automated activity log ingestion and unit-conversion logic.
- **SQLite Database**: Structured tracking of historical emission trends across global business units.
- **Executive Dashboard**: Interactive analytical tools using Streamlit, Seaborn, and Plotly.
- **Decarbonization Modeling**: Strategic identifying of decarbonization opportunities.

## Tech Stack
- **Language**: Python
- **Database**: SQLite3
- **Visualization**: Plotly, Seaborn, Matplotlib
- **Dashboard**: Streamlit
- **Methodology**: GHG Protocol, EPA, DEFRA

## Project Structure
- `src/database/`: SQL schemas and database management.
- `src/pipeline/`: ETL scripts for data ingestion.
- `src/engine/`: Calculation logic for emissions.
- `src/dashboard/`: Streamlit dashboard implementation.
- `data/`: Raw and processed data storage.

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Initialize database: `python src/database/db_manager.py`
3. Run dashboard: `streamlit run src/dashboard/app.py`
