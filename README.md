# Environmental Database for Bangladesh

## Overview

This project develops a relational **Environmental Database for Bangladesh** to store and manage diverse environmental datasets in a structured MySQL database.

The collected datasets cover **rainfall, precipitation, flood, river monitoring, temperature, humidity, sunshine, land use, arsenic contamination, environmental indicators, water quality, and greenhouse gas emissions**.

Since the datasets were collected from different sources and had different structures, they were examined, cleaned, transformed, and organized before being loaded into the database.

The database is named **`environment_bd`**.

---

## Objectives

* Collect and integrate environmental datasets related to Bangladesh.
* Examine, clean, and standardize datasets before database insertion.
* Design a relational database based on the collected data.
* Organize geographical information such as country, division, district, upazila, thana, union, mouza, and city.
* Establish relationships between related datasets using primary and foreign keys.
* Automate data transformation and loading using Python.
* Store the processed datasets in MySQL for querying and analysis.

---

## Database Scope

The database contains **29 tables** covering the following major areas:

### Geographical Information

* Country
* Division
* District
* Upazila
* Thana
* Union Area
* Mouza
* City

### Climate and Weather

* Rainfall
* Precipitation
* Daily Maximum Temperature
* Daily Minimum Temperature
* Daily Humidity
* Daily Sunshine
* Mean Surface Air Temperature
* Maximum Surface Air Temperature
* Yearly Temperature Change

### Flood and River

* Flood
* River Station
* River Morphology
* Sediment

### Environmental and Water

* Environmental Indicators
* Land Use
* Arsenic Contamination
* Surface Water Quality

### Greenhouse Gas Emissions

* Country-Level Emissions
* National Sectoral Emissions
* Agricultural Production Emissions
* City-Level Emissions
* Source-Level Emissions

An ETL/loading log table is also included to track the data loading process.

---

## Database Design

The database design was developed by first examining the collected datasets and identifying the required entities, attributes, and relationships.

An **ER diagram was prepared before implementing the database**, which was then used as the basis for the relational database design and SQL schema.

The geographical entities provide a common structure for connecting environmental datasets with specific locations. Primary keys uniquely identify records, while foreign keys maintain relationships and referential integrity between related tables.

---

## Data Collection

Datasets were collected from various government organizations, international data portals, research repositories, and publicly available sources.

Some of the sources include:

* Worldometer
* Humanitarian Data Exchange
* Climate Change Knowledge Portal
* Flood Forecasting and Warning Centre
* Hydroinformatics and Flood Forecasting Circle
* Joint Monitoring Programme
* Kaggle
* Mendeley Data
* Sustainable and Renewable Energy Development Authority
* CORGIS Datasets Project
* British Geological Survey
* Other relevant research and environmental data repositories

The collected datasets were organized mainly in **CSV format** for further processing.

---

## Data Cleaning and Preparation

The collected datasets had differences in column names, data types, date formats, missing values, and text formats.

Before loading them into MySQL, the datasets were processed to:

* Handle missing and empty values.
* Standardize text values.
* Convert numeric values into appropriate data types.
* Standardize date formats.
* Rename columns according to the database schema.
* Remove unnecessary formatting differences.
* Check values required for primary and foreign key relationships.

The original information was preserved as much as possible while applying only the transformations necessary for database integration.

---

## ETL Process

Python was used to implement the **Extract, Transform, and Load (ETL)** process.

### Extract

The ETL scripts read the collected CSV datasets from the dataset directory.

### Transform

The data is processed according to the requirements of the corresponding database tables. This includes cleaning values, handling missing data, converting data types and dates, renaming columns, and preparing records for MySQL.

### Load

The transformed data is inserted into the appropriate tables of the **`environment_bd`** database while maintaining the required table relationships.

---

## Python ETL Implementation

The ETL process is implemented using Python and the following libraries:

* **Pandas** — Data reading and transformation
* **NumPy** — Numerical and missing-value handling
* **MySQL Connector/Python** — MySQL database connection
* **OS/File handling modules** — Dataset and file management

### ETL Scripts

**`environment_bd_etl.py`**
Main script for extracting, transforming, and loading the datasets.

**`environment_bd_missing_tables_etl.py`**
Additional ETL script for tables that require separate or specialized processing.

---

## MySQL Implementation

The database is implemented using **MySQL**.

The SQL schema defines:

* Database and table structures
* Primary keys
* Foreign keys
* Data types
* Constraints
* Relationships between tables

The schema file is:

**`environment_bd_schema.sql`**

---

## Project Workflow

```text
Data Sources
     ↓
Dataset Collection
     ↓
Data Examination
     ↓
Data Cleaning & Preparation
     ↓
ER Diagram & Database Design
     ↓
MySQL Schema Creation
     ↓
Python ETL
     ↓
Data Loading
     ↓
environment_bd Database
     ↓
SQL Queries & Analysis
```

---

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
│   └── Environmental CSV datasets
│
└── README.md
```

| File/Folder                            | Description                                                                   |
| -------------------------------------- | ----------------------------------------------------------------------------- |
| `sql/`                                 | Contains the SQL database schema                                              |
| `environment_bd_schema.sql`            | Creates the database and defines tables, keys, constraints, and relationships |
| `etl/`                                 | Contains Python ETL scripts                                                   |
| `environment_bd_etl.py`                | Main ETL script                                                               |
| `environment_bd_missing_tables_etl.py` | ETL script for separately processed tables                                    |
| `datasets/`                            | Contains the collected CSV datasets                                           |
| `README.md`                            | Project documentation                                                         |

---

## Technologies Used

* **MySQL** — Relational database management system
* **Python** — ETL and data processing
* **Pandas** — Dataset processing
* **NumPy** — Numerical and missing-value handling
* **MySQL Connector/Python** — Database connectivity
* **CSV/Excel** — Dataset preparation and organization
* **VS Code** — Development environment
* **GitHub** — Project version control and file management

---

## Testing and Verification

After schema creation and data loading, the database was verified by:

* Checking successful table creation.
* Checking record counts.
* Verifying inserted data.
* Checking primary key values.
* Checking foreign key relationships.
* Checking NULL and missing values.
* Comparing selected database records with the original datasets.

Tables requiring additional processing were handled through the separate ETL script without unnecessarily changing the database structure.

---

## Possible Uses

The database can be used to query and analyze:

* Rainfall and precipitation by location and time.
* Flood events and affected areas.
* River station and morphology data.
* Temperature, humidity, and sunshine records.
* Environmental indicators and land-use information.
* Arsenic contamination and water-quality data.
* Greenhouse gas emissions by country, city, sector, and source.

---

## Future Scope

The project can be extended by:

* Adding more recent environmental datasets.
* Integrating additional geographical and environmental data.
* Developing a web-based database interface.
* Creating environmental dashboards and visualizations.
* Adding GIS-based maps.
* Performing long-term climate and environmental trend analysis.
* Applying predictive analytics and machine learning.

---

## Project Information

| Item                        | Details                                          |
| --------------------------- | ------------------------------------------------ |
| **Project**                 | Integrated Environmental Database for Bangladesh |
| **Database**                | `environment_bd`                                 |
| **Database Type**           | Relational Database                              |
| **DBMS**                    | MySQL                                            |
| **ETL Language**            | Python                                           |
| **Data Format**             | CSV                                              |
| **Development Environment** | VS Code                                          |
