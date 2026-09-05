Environmental Database for Bangladesh

Overview

This project focuses on developing a relational database for storing and managing different environmental datasets of Bangladesh. The collected data includes information about rainfall, precipitation, flood, rivers, temperature, humidity, sunshine, land use, arsenic contamination, environmental indicators, and greenhouse gas emissions.

The datasets were collected from different sources and prepared in CSV format. Since the datasets had different structures and formats, they were cleaned and transformed before being loaded into the database.

Objectives

- To collect and organize environmental data of Bangladesh.
- To clean and prepare datasets before database loading.
- To design a relational database using an ER model.
- To connect related environmental and geographical information.
- To maintain data consistency using primary keys and foreign keys.
- To automate data loading using Python ETL.

Database

The database is created using MySQL and is named:

environment_bd

The final database contains 29 tables covering geographical, climate, flood, river, water quality, environmental indicator, pollution, and greenhouse gas emission data.

The main entities identified during database design include:

- Location
- Rainfall
- Precipitation
- Flood
- Sediment
- Land Use
- Arsenic Contamination
- Surface Water Quality
- River Station
- River Morphology
- Environment Indicator
- Temperature
- Humidity
- Sunshine
- Different levels of Gas Emissions

Primary keys and foreign keys are used to maintain relationships between the tables.

Data Processing and ETL

The project follows a simple ETL workflow:

Raw Datasets
     ↓
Data Examination
     ↓
Data Cleaning
     ↓
Data Transformation
     ↓
Python ETL
     ↓
MySQL Database

Python is used to read the CSV files, clean and transform the data, and load it into MySQL.

Two Python scripts are used:

environment_bd_etl.py
environment_bd_missing_tables_etl.py

The second script is used for tables that require additional processing after the main ETL process.

Repository Structure

environmental-database/
│
├── sql/
│   └── environment_bd_schema.sql
│
├── etl/
│   ├── environment_bd_etl.py
│   └── environment_bd_missing_tables_etl.py
│
├── datasets/
│   └── Environmental CSV datasets
│
└── README.md

Technologies Used

- MySQL — Database management
- Python — ETL and data processing
- Pandas — Data cleaning and transformation
- NumPy — Numerical data processing
- MySQL Connector/Python — Database connection
- VS Code — Development environment
- GitHub — Project file management

Future Scope

The database can later be used for environmental trend analysis, geographic visualization, climate and flood analysis, greenhouse gas emission analysis, dashboards, and predictive analysis.

Project Status

Status: Database design, data cleaning, SQL implementation, and ETL development are completed, with final data verification in progress.

Project: Integrated Environmental Database for Bangladesh
Database: "environment_bd"
