Environmental Database for Bangladesh

1. Project Overview

This project is about developing a relational database for storing and managing different types of environmental data of Bangladesh.

For this project, we collected datasets from different sources. These datasets contain information related to rainfall, precipitation, flood, rivers, temperature, humidity, sunshine, land use, arsenic contamination, environmental indicators, and greenhouse gas emissions.

Since the datasets came from different sources, their formats and column structures were not the same. We therefore cleaned and organized the data before loading it into MySQL. The main purpose was to bring these separate datasets into one database so that related environmental information can be queried from a single system.

The database is named "environment_bd".

2. Project Objectives

The main objectives of this project are:

- To collect different environmental datasets related to Bangladesh.
- To examine and clean the collected datasets before storing them.
- To design a relational database based on the collected data.
- To organize geographical information such as country, division, district, upazila, union, mouza, thana, and city.
- To store environmental and climate-related information in separate but related tables.
- To maintain relationships between tables using primary keys and foreign keys.
- To use Python for data cleaning and ETL operations.
- To load the cleaned datasets into MySQL.
- To make the database suitable for SQL queries and further environmental analysis.

3. Database Scope

Our database contains 29 tables. The tables cover several areas of environmental information.

Geographical Information

The geographical part of the database contains information about:

- Country
- Division
- District
- Upazila
- Thana
- Union Area
- Mouza
- City

These tables help connect environmental information with specific geographical areas.

Climate and Weather Data

The database includes different types of climate-related data, such as:

- Daily maximum temperature
- Daily minimum temperature
- Daily humidity
- Daily sunshine
- Mean surface air temperature
- Maximum surface air temperature
- Yearly temperature change
- Rainfall
- Precipitation

Flood and River Data

The database also contains information related to:

- Flood events
- River stations
- River morphology
- Sediment data

These tables contain information such as river stations, survey dates, flood periods, affected areas, and other monitoring-related values.

Environmental and Water Information

Environmental monitoring data includes:

- Environmental indicators
- Land use
- Arsenic contamination
- Surface water quality

Greenhouse Gas Emission Data

Several tables are used for storing emission-related datasets at different levels:

- Country-level gas emissions
- National sectoral emissions
- Emissions from pre- and post-agricultural production
- City-level gas emissions
- Source-level gas emissions

Keeping these datasets in separate tables allows the different emission data structures to be stored without forcing unrelated columns into one table.

Data Loading Information

A separate loading log table is also used to keep track of the ETL/data loading process.


4. Database Design

Before creating the database, we examined the collected datasets and identified the entities and their attributes.

The final design contains 24 main environmental and geographical entities, which are represented through the database tables.

Some of the main entities are:

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
- Daily Maximum Temperature
- Daily Minimum Temperature
- Daily Humidity
- Daily Sunshine
- Country-Level Emissions
- City-Level Emissions
- Source-Level Emissions
- National Sectoral Emissions
- Agricultural Production Emissions
- Mean Surface Air Temperature
- Maximum Surface Air Temperature
- Yearly Temperature Change

The geographical information is used as a common connection between many environmental datasets.

Primary keys are used to uniquely identify records, while foreign keys are used where one table depends on information stored in another table.



5. Data Collection

The datasets used in the project were collected from different environmental data sources. The sources include government organizations, international data portals, research datasets, and publicly available repositories.

Some of the sources used in our project include:

- Worldometer
- Humanitarian Data Exchange
- Climate Change Knowledge Portal
- Flood Forecasting and Warning Centre
- Hydroinformatics and Flood Forecasting Circle
- Joint Monitoring Programme
- Kaggle
- Mendeley Data
- Sustainable and Renewable Energy Development Authority
- CORGIS Datasets Project
- British Geological Survey
- Food and Agriculture-related data platforms
- Research publications and data repositories

The collected files were converted and organized mainly in CSV format so that they could be processed using Python.


6. Data Cleaning and Preparation

The collected datasets did not have exactly the same structure. Some files contained missing values, different date formats, inconsistent text values, and numeric values stored in different formats.

Before loading the data into MySQL, we performed several cleaning operations.

The main steps were:

1. Checking the columns and data types of each dataset.
2. Removing unnecessary formatting differences.
3. Handling missing values.
4. Standardizing text values.
5. Converting numeric columns into appropriate numeric types.
6. Converting date values into consistent formats.
7. Matching dataset column names with the database column names.
8. Checking primary key and foreign key related values.
9. Preparing the cleaned CSV files for database loading.

We kept the original information of the datasets as much as possible and mainly performed transformations that were necessary for storing them properly in the relational database.


7. ETL Process

We used an ETL (Extract, Transform, Load) process to transfer the datasets into the database.

Extract

The datasets were collected and stored as CSV files. The Python program reads these files from the dataset folder/ZIP file.

Transform

After reading a file, Python processes the data before insertion. Depending on the dataset, this includes:

- Handling empty values
- Cleaning text fields
- Converting numbers
- Converting dates
- Renaming columns
- Removing unwanted formatting
- Preparing values for MySQL

Different datasets required slightly different transformations because their original structures were not identical.

Load

After transformation, the data is inserted into the corresponding MySQL tables.

The database uses primary and foreign key relationships, so tables with required parent information are considered when loading dependent data.


8. Python ETL Implementation

Python was used as the main tool for automating the data loading process.

The ETL program uses libraries such as:

- Pandas for reading and transforming CSV data
- NumPy for numerical and missing-value handling
- MySQL Connector/Python for connecting Python with MySQL
- OS/File handling modules for working with the dataset files

The main ETL script reads the datasets, processes the data according to the required table structure, and inserts the records into the "environment_bd" database.

We also created a separate ETL script for the tables that needed additional processing after the main loading process.

Main ETL Script

environment_bd_etl.py

This is used for the main data extraction, transformation, and loading process.

Additional ETL Script

environment_bd_missing_tables_etl.py

This script is used to process and load specific tables separately when required.

This separate script was useful because some datasets had column structures or relationships that needed additional handling.


9. MySQL Database

The cleaned data is stored in a MySQL database named:

environment_bd

The SQL schema contains the database and table definitions, including:

- Primary keys
- Foreign keys
- Data types
- Constraints
- Table relationships

The schema file is:

environment_bd_schema.sql

The database tables were designed according to the ER model prepared during the database design stage.

---

10. Database Loading

After creating the database schema, the Python ETL program was used to load the CSV data into the appropriate tables.

During loading, the program checks and prepares values before inserting them into MySQL.

The loading process was tested by checking the number of records in the database tables after execution. This helped us identify tables where additional transformation or loading steps were required.

For some datasets, a separate loading script was used rather than changing the database design.



11. Project Workflow

The overall workflow of our project can be summarized as:

Data Sources
     ↓
Dataset Collection
     ↓
CSV Files
     ↓
Data Examination
     ↓
Data Cleaning
     ↓
Data Transformation
     ↓
ER Diagram / Database Design
     ↓
MySQL Schema Creation
     ↓
Python ETL
     ↓
Data Loading
     ↓
environment_bd Database
     ↓
SQL Queries and Analysis



12. Repository Structure

The project files are organized approximately as follows:

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

File and Folder Description

File/Folder| Description
"sql/"| Contains the SQL database schema
"environment_bd_schema.sql"| Creates the database and defines the tables and relationships
"etl/"| Contains Python ETL scripts
"environment_bd_etl.py"| Main ETL script for processing and loading datasets
"environment_bd_missing_tables_etl.py"| Additional ETL script for specific tables
"datasets/"| Contains the collected CSV datasets
"README.md"| Project documentation



13. Technologies Used

The main technologies and tools used in this project are:

- MySQL — Used for creating and managing the relational database.
- Python — Used for ETL and data processing.
- Pandas — Used for reading and cleaning datasets.
- NumPy — Used for numerical and missing-value processing.
- MySQL Connector/Python — Used to connect Python with MySQL.
- Excel/CSV — Used during dataset preparation and organization.
- VS Code — Used for writing and running the Python scripts.
- GitHub — Used for organizing and sharing the project files.



14. Database Relationships

The database is not simply a collection of separate datasets. Several tables are connected through common geographical and temporal information.

For example, environmental records can be associated with geographical information through location-related tables. Similarly, river-related datasets use river station information to organize monitoring data.

Foreign keys are used where relationships between tables are required. This helps prevent invalid references and keeps related information consistent.

The ER diagram was prepared before implementing the final SQL schema so that the relationships between entities could be identified clearly.



15. Testing and Verification

After creating the database and running the ETL process, we checked the loaded tables using SQL queries.

Some of the checks performed include:

- Checking whether tables were created successfully.
- Checking the number of records in each table.
- Checking whether data was inserted correctly.
- Checking primary key values.
- Checking foreign key relationships.
- Checking NULL and missing values.
- Comparing selected database records with the original CSV data.

When a table did not load as expected, we examined the corresponding CSV structure and adjusted the ETL processing instead of changing the database structure unnecessarily.

---

16. Possible Uses of the Database

Once the database is fully populated, it can be used for different types of environmental queries and analysis.

For example, users can query:

- Rainfall information for a particular location or year.
- Flood-affected areas during a specific period.
- River station and morphology information.
- Temperature and humidity records.
- Environmental indicator values for different years.
- Arsenic contamination information.
- City-level or country-level greenhouse gas emissions.
- Emission information for different sectors or sources.

This makes the database useful as a starting point for further environmental data analysis.



17. Future Scope

There are several ways in which the project can be extended in the future.

Possible improvements include:

- Adding more recent environmental datasets.
- Connecting more datasets through common geographical identifiers.
- Developing a web-based interface for database queries.
- Creating environmental dashboards.
- Adding maps and geographic visualization.
- Performing long-term climate and rainfall trend analysis.
- Comparing flood and rainfall patterns.
- Analyzing greenhouse gas emission trends.
- Using the database for predictive analysis and machine learning.



18. Project Status

Current Status: Database design, dataset preparation, data cleaning, SQL implementation, and ETL development have been completed/in progress as part of the project workflow. Final verification of loaded records is being performed.



19. Project Information

Project: Integrated Environmental Database for Bangladesh

Database Name: "environment_bd"

Database Type: Relational Database

Primary Database System: MySQL

ETL Language: Python

Data Format: CSV

Development Environment: VS Code
