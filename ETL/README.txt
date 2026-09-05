ETL SCRIPTS
------------

This folder contains the Python scripts used to clean, transform,
and load environmental datasets into the MySQL database.

Files:
- environment_bd_etl.py
    Performs the complete ETL process and loads the environmental
    datasets into the corresponding MySQL tables.

- environment_bd_missing_tables_etl.py
    Loads and verifies selected tables that require separate processing
    after the main ETL process.

Main ETL Process:
1. Extract data from the provided datasets.
2. Clean and standardize the data.
3. Transform data into the required format.
4. Connect to the MySQL database.
5. Load the processed data into the appropriate tables.
6. Verify the number of loaded records.

Technologies:
- Python
- Pandas
- NumPy
- MySQL Connector/Python
- MySQL
