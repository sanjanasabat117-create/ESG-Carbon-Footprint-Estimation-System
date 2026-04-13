# Carbon Footprint Estimation Methodology

This project follows the **GHG Protocol Corporate Accounting and Reporting Standard**, the most widely used international accounting tool for government and business leaders to understand, quantify, and manage greenhouse gas emissions.

## Emission Scopes Covered

### Scope 1: Direct Emissions
- **Stationary Combustion**: Natural gas used for heating and onsite power.
- **Mobile Combustion**: Diesel and gasoline used by the company-owned vehicle fleet.

### Scope 2: Indirect Emissions
- **Purchased Electricity**: Emissions from the generation of electricity purchased and consumed by the organization. Calculation uses regional grid-average factors.

### Scope 3: Value Chain Emissions
- **Business Travel**: Air travel categorized by haul length (Short/Medium/Long).
- **Waste Management**: Emissions from waste sent to landfills.

## Data Pipeline & Calculation Logic
1. **Ingestion**: Raw activity logs (CSV) are validated for unit consistency.
2. **Conversion**: Activity data (e.g., kWh, Gallons) is converted into Metric Tons of CO2 equivalent (tCO2e).
3. **Database**: A SQLite backend maintains a historical audit trail of all business unit activities.
4. **Analysis**: The Streamlit dashboard applies dynamic reduction logic to model future decarbonization targets.

## Data Sources
Emission factors are referenced from **EPA (US)** and **DEFRA (UK)** 2023/2024 datasets.
