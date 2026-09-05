# Environmental Database for Bangladesh

## Overview

This project develops an integrated **Environmental Database for Bangladesh** to organize and analyze environmental, climatic, disaster, geographical, water, pollution, and greenhouse gas emission data within a structured relational database system.

The database is designed to integrate data from different sources using common **geographical and temporal dimensions**, making environmental information easier to store, manage, query, and analyze.

## Objectives

* Integrate diverse environmental datasets of Bangladesh into a centralized relational database.
* Organize geographical information through a hierarchical structure such as **Country → Division → District → Upazila → Thana → Union → Mouza**.
* Store and manage climate, rainfall, flood, river, pollution, land-use, arsenic contamination, and emission-related data.
* Apply data cleaning, transformation, and normalization techniques before database loading.
* Maintain data consistency through **Primary Keys, Foreign Keys, constraints, and normalized relational tables**.
* Provide a reliable foundation for environmental analysis and future data-driven applications.

## Database Scope

The database contains **29 related tables** covering major environmental and geographical domains, including:

* **Geographical Data:** Country, Division, District, Upazila, Thana, Union Area, Mouza, and City
* **Climate and Weather:** Surface Air Temperature, Precipitation, Rainfall, Temperature, Humidity, and Sunshine data
* **Disaster Data:** Flood-related information
* **River and Water Resources:** River Stations, River Morphology, Sediment, and related monitoring data
* **Environmental Indicators:** Environmental indicators and land-use information
* **Pollution and Contamination:** Arsenic contamination and environmental monitoring data
* **Greenhouse Gas Emissions:** Country-level, national-sectoral, agricultural, city-level, and source-level emission data
* **Data Management:** Daily data loading and processing logs

## Data Processing and ETL

The project follows an **ETL (Extract, Transform, Load)** workflow:

1. **Extract** – Environmental datasets are collected from their respective sources, primarily in CSV format.
2. **Transform** – Data is cleaned and standardized by handling missing values, inconsistent text, numeric values, and date formats.
3. **Load** – The transformed datasets are inserted into the MySQL database according to table dependencies and relationships.

Python is used to automate the ETL process, while MySQL is used for relational data storage and management.

## Repository Structure

```text
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
│   └── Environmental datasets
│
└── README.md
```

### Directory Description

| Directory/File | Purpose                                                        |
| -------------- | -------------------------------------------------------------- |
| `sql/ `         | Contains the MySQL database schema and table definitions       |
| `etl/`         | Contains Python scripts for data cleaning and database loading |
| `datasets/`    | Contains the environmental datasets used in the project        |
| `README.md`    | Project documentation and repository guide                     |

## Technologies Used

* **MySQL** – Relational database management system
* **Python** – ETL automation and data processing
* **Pandas** – Data cleaning and transformation
* **NumPy** – Numerical data processing
* **MySQL Connector/Python** – Python–MySQL database connectivity
* **GitHub** – Version control and project resource management
* **VS Code** – Development environment

## Database Design

The database follows a relational model with interconnected entities based on geographical, temporal, and environmental relationships.

Primary and foreign keys are used to maintain **referential integrity**, while normalization principles are applied to reduce redundancy and improve consistency.

The SQL schema can be found in:

```text
sql/environment_bd_schema.sql
```

## ETL Scripts

### Complete ETL

`environment_bd_etl.py`

This script performs the complete ETL process and loads the environmental datasets into the corresponding MySQL tables in dependency order.

### Missing Tables ETL

`environment_bd_missing_tables_etl.py`

This script is used to load and verify specific tables that require separate processing after the main ETL process.

## Data Sources

The project uses environmental and socio-environmental datasets obtained from reliable sources, including government organizations, international data portals, and research data repositories.

Each dataset is cleaned and transformed before being integrated into the database.

## Project Workflow

```text
Environmental Data Sources
          ↓
     Raw Datasets
          ↓
   Data Examination
          ↓
   Data Cleaning
          ↓
 Data Transformation
          ↓
       ETL
          ↓
      MySQL
          ↓
 Integrated Environmental Database
          ↓
 Environmental Analysis & Querying
```

## Future Scope

The database can be further extended to support:

* Environmental trend analysis
* Climate and disaster relationship analysis
* Geographic visualization and mapping
* Pollution and water-quality analysis
* Greenhouse gas emission analysis
* Environmental dashboards
* Predictive analytics and machine learning applications

## Project Status

**Status:** Database design, data organization, cleaning, and ETL implementation are completed.

---

**Project:** Integrated Environmental Database for Bangladesh
**Repository:** Environmental Database Project
**Database:** `environment_bd`
