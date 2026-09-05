# Environmental Database for Bangladesh

## Overview

A relational database project designed to store, manage, and integrate environmental data from Bangladesh, including climate, rainfall, floods, rivers, water quality, land use, pollution, and greenhouse gas emissions.

The datasets were collected from multiple sources, cleaned, transformed, and loaded into a centralized MySQL database.

---

## Objectives

* Organize environmental datasets of Bangladesh.
* Design a relational database using an ER model.
* Maintain relationships and data integrity using primary and foreign keys.
* Clean and transform datasets for database integration.
* Automate data loading using Python ETL.

---

## ER Diagram

The database structure was designed using an Entity-Relationship (ER) Diagram, which defines the entities and relationships within the system.

![Entity Relationship Diagram](diagrams/ER_Diagram_final.PNG)

---

## Database

**Database:** `environment_bd`

The database contains **29 tables** covering geographical, climate, environmental, flood, river, water quality, pollution, land use, and greenhouse gas emission data.

The database schema is available in:

```text id="a1k9qz"
sql/environment_bd_schema.sql
```

---

## ETL Process

```text id="p7x3mn"
Raw Datasets
     ↓
Data Cleaning
     ↓
Data Transformation
     ↓
Python ETL
     ↓
MySQL Database
```

### ETL Scripts

* `environment_bd_etl.py` — Main ETL process.
* `environment_bd_missing_tables_etl.py` — Processes additional tables requiring separate handling.

---

## Repository Structure

```text id="r5v2kc"
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
├── diagrams/
│   └── ER_Diagram_final.PNG
│
└── README.md
```

---

## Technologies Used

* MySQL
* Python
* Pandas
* NumPy
* MySQL Connector/Python
* VS Code

---

## Project Status

**Status:** Completed
