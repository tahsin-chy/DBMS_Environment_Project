import os
import zipfile
import shutil
from pathlib import Path

import mysql.connector
import pandas as pd
import numpy as np



# CONFIGURATION
# ----------------------

ZIP_FILE = r"C:\Users\User\Downloads\NEW_dataset.zip"

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "sanjida"
DB_PASSWORD = "*****"
DB_NAME = "environment_bd"

BATCH_SIZE = 1000


# HELPER FUNCTIONS
# --------------------

def norm_text(x):
    if pd.isna(x):
        return None

    x = str(x).strip()

    if x == "":
        return None

    return x


def clean_df(df):
    df = df.copy()

    # Clean column names
    df.columns = [
        str(c).strip()
        for c in df.columns
    ]

    # Clean text values
    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].map(norm_text)

    return df


def clean_num(s):
    return pd.to_numeric(
        s.astype(str)
        .str.replace(",", "", regex=False)
        .replace({
            "nan": np.nan,
            "None": np.nan,
            "": np.nan
        }),
        errors="coerce"
    )


def clean_date(s):
    return pd.to_datetime(
        s,
        errors="coerce"
    ).dt.date


def read_csv(root, filename):

    path = root / filename

    if not path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {path}"
        )

    df = pd.read_csv(
        path,
        low_memory=False
    )

    df = clean_df(df)

    print(
        f"Reading {filename:45} "
        f"Rows = {len(df)}"
    )

    return df



# INSERT FUNCTION
# ---------------

def insert_df(conn, table, columns, df):

    if df.empty:

        print(
            f"{table:40} "
            f"CSV=0 "
            f"INSERTED=0 "
            f"FAILED=0"
        )

        return 0, 0

    # Check missing columns
    missing = [
        c for c in columns
        if c not in df.columns
    ]

    if missing:

        print(
            f"\nERROR in {table}"
        )

        print(
            "Missing columns:",
            missing
        )

        print(
            "Available columns:",
            list(df.columns)
        )

        return 0, len(df)

    # Keep required columns only
    work = df[columns].copy()

    # Remove exact duplicate rows
    work = work.drop_duplicates()

    placeholders = ",".join(
        ["%s"] * len(columns)
    )

    col_sql = ",".join(
        f"`{c}`" for c in columns
    )

    sql = (
        f"INSERT IGNORE INTO `{table}` "
        f"({col_sql}) "
        f"VALUES ({placeholders})"
    )

    cur = conn.cursor()

    inserted = 0
    failed = 0

    for start in range(
        0,
        len(work),
        BATCH_SIZE
    ):

        batch = work.iloc[
            start:start + BATCH_SIZE
        ]

        values = []

        for row in batch.itertuples(
            index=False,
            name=None
        ):

            values.append(
                tuple(
                    None if pd.isna(v)
                    else v
                    for v in row
                )
            )

    
        # Try batch insert
        # ----------------------------------------------------

        try:

            cur.executemany(
                sql,
                values
            )

            conn.commit()

            inserted += cur.rowcount

        except Exception as e:

            conn.rollback()

            
            # Retry row-by-row
            # ------------------------------------------------

            for row in values:

                try:

                    cur.execute(
                        sql,
                        row
                    )

                    inserted += cur.rowcount

                except Exception as row_error:

                    failed += 1

            conn.commit()

    cur.close()

    print(
        f"{table:40} "
        f"CSV={len(df):8} "
        f"INSERTED={inserted:8} "
        f"FAILED={failed:8}"
    )

    return inserted, failed



# DATABASE ROW COUNT
# ---------------------

def get_row_count(conn, table):

    cur = conn.cursor()

    cur.execute(
        f"SELECT COUNT(*) FROM `{table}`"
    )

    count = cur.fetchone()[0]

    cur.close()

    return count


# MAIN
# ------------

def main():

    print(
        "\n======"
    )
    print(
        "      ENVIRONMENT BD - MISSING TABLE ETL"
    )
    print(
        "=========\n"
    )

    
    # Check ZIP
    # -------------

    zip_path = Path(ZIP_FILE)

    if not zip_path.exists():

        raise FileNotFoundError(
            f"ZIP file not found:\n{zip_path}"
        )


    # Extract ZIP
    # -----------------------

    extract_dir = (
        zip_path.parent /
        "environment_data_extracted_missing"
    )

    if extract_dir.exists():
        shutil.rmtree(extract_dir)

    extract_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    with zipfile.ZipFile(
        zip_path,
        "r"
    ) as z:

        z.extractall(extract_dir)

    
    # Find CSV directory
    # ---------------------

    csv_files = list(
        extract_dir.rglob("*.csv")
    )

    if not csv_files:

        raise FileNotFoundError(
            "No CSV files found inside ZIP."
        )

    root = csv_files[0].parent

    print(
        "CSV directory:"
    )

    print(root)

    print(
        "\nCSV files found:",
        len(csv_files)
    )

    # Connect MySQL
    # ------------------
    conn = mysql.connector.connect(

        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        autocommit=False
    )

    print(
        "\nMySQL connection successful."
    )

    print(
        "Database:",
        DB_NAME
    )

    
    # 1. SURFACE AIR TEMPERATURE
    #---------------------------------


    print(
        "\n-------"
    )
    print(
        "1. SURFACE AIR TEMPERATURE"
    )
    print(
        "----------"
    )

    df = read_csv(
        root,
        "surface_air_temp.csv"
    )

    df = df.rename(
        columns={

            "mean_sur_temp_cel":
                "mean_sur_temp_cel",

            "5year_gaussian_smooth_mean":
                "five_year_gaussian_smooth_mean",

            "max _sur_temp_cel":
                "max_sur_temp_cel",

            "5year_gaussian_smooth_max":
                "five_year_gaussian_smooth_max",

            "min_sur_temp_cel":
                "min_sur_temp_cel",

            "5year_gaussian_smooth_min":
                "five_year_gaussian_smooth_min",

            "Country_name":
                "country_name"
        }
    )

    df["year"] = pd.to_numeric(
        df["year"],
        errors="coerce"
    )

    numeric_cols = [

        "mean_sur_temp_cel",

        "five_year_gaussian_smooth_mean",

        "max_sur_temp_cel",

        "five_year_gaussian_smooth_max",

        "min_sur_temp_cel",

        "five_year_gaussian_smooth_min"
    ]

    for c in numeric_cols:
        df[c] = clean_num(df[c])

    # Remove rows without primary key
    df = df[
        df["year"].notna()
    ]

    ins, fail = insert_df(

        conn,

        "surface_air_temp",

        [
            "year",
            "mean_sur_temp_cel",
            "five_year_gaussian_smooth_mean",
            "max_sur_temp_cel",
            "five_year_gaussian_smooth_max",
            "min_sur_temp_cel",
            "five_year_gaussian_smooth_min",
            "country_name"
        ],

        df
    )

    print(
        "Current DB rows:",
        get_row_count(
            conn,
            "surface_air_temp"
        )
    )


    
    # 2. RIVER MORPHOLOGY
    # ---------------------

    print(
        "\n-----"
    )
    print(
        "2. RIVER MORPHOLOGY"
    )
    print(
        "-----------"
    )

    df = read_csv(
        root,
        "river_morphology.csv"
    )

    df = df.rename(
        columns={

            "River_Station_ID":
                "river_station_id",

            "River_Name":
                "river_name",

            "Rotation_of_river_survey":
                "rotation_of_river_survey",

            "District":
                "district",

            "Upazila":
                "upazila",

            "Latitude":
                "latitude",

            "Longitude":
                "longitude",

            "start_date":
                "start_date",

            "last_date":
                "last_date"
        }
    )

    df["latitude"] = clean_num(
        df["latitude"]
    )

    df["longitude"] = clean_num(
        df["longitude"]
    )

    df["start_date"] = clean_date(
        df["start_date"]
    )

    df["last_date"] = clean_date(
        df["last_date"]
    )

    df = df[
        df["river_station_id"].notna()
    ]

    ins, fail = insert_df(

        conn,

        "river_morphology",

        [
            "river_station_id",
            "river_name",
            "rotation_of_river_survey",
            "district",
            "upazila",
            "latitude",
            "longitude",
            "start_date",
            "last_date"
        ],

        df
    )

    print(
        "Current DB rows:",
        get_row_count(
            conn,
            "river_morphology"
        )
    )


    # 3. COUNTRY LEVEL GAS EMISSION
    # ------------------------------

    print(
        "\n-----"
    )
    print(
        "3. COUNTRY LEVEL GAS EMISSION"
    )
    print(
        "----------------------------------------------------"
    )

    df = read_csv(
        root,
        "country_level_gas_emission.csv"
    )

    df = df.rename(
        columns={

            "Source_Code":
                "source_code",

            "Source":
                "source",

            "Year":
                "year",

            "Unit":
                "unit",

            "Emissions_Quantity":
                "emissions_quantity",

            "Gas_Name":
                "gas_name",

            "Type_of_Emissions":
                "type_of_emissions"
        }
    )

    df["source_code"] = clean_num(
        df["source_code"]
    )

    df["year"] = clean_num(
        df["year"]
    )

    df["emissions_quantity"] = clean_num(
        df["emissions_quantity"]
    )

    df = df[
        df["country_name"].notna() &
        df["source_code"].notna() &
        df["year"].notna() &
        df["gas_name"].notna() &
        df["type_of_emissions"].notna()
    ]

    ins, fail = insert_df(

        conn,

        "country_level_gas_emission",

        [
            "country_name",
            "source_code",
            "source",
            "year",
            "unit",
            "emissions_quantity",
            "gas_name",
            "type_of_emissions"
        ],

        df
    )

    print(
        "Current DB rows:",
        get_row_count(
            conn,
            "country_level_gas_emission"
        )
    )


    
    # 4. NATIONAL SECTORAL EMISSIONS
    # -------------------------------

    print(
        "\n-----"
    )
    print(
        "4. NATIONAL SECTORAL EMISSIONS"
    )
    print(
        "-----"
    )

    df = read_csv(
        root,
        "national_sectoral_emissions.csv"
    )

    df = df.rename(
        columns={

            "Country_name":
                "country_name",

            "Source_ID":
                "source_id",

            "Source":
                "source",

            "Year":
                "year",

            "Unit":
                "unit",

            "Emissions_Quantity":
                "emissions_quantity",

            "Gas_Name":
                "gas_name",

            "Type_of_Emission":
                "type_of_emission"
        }
    )

    df["source_id"] = clean_num(
        df["source_id"]
    )

    df["year"] = clean_num(
        df["year"]
    )

    df["emissions_quantity"] = clean_num(
        df["emissions_quantity"]
    )

    df = df[
        df["country_name"].notna() &
        df["source_id"].notna() &
        df["year"].notna() &
        df["gas_name"].notna() &
        df["type_of_emission"].notna()
    ]

    ins, fail = insert_df(

        conn,

        "national_sectoral_emissions",

        [
            "country_name",
            "source_id",
            "source",
            "year",
            "unit",
            "emissions_quantity",
            "gas_name",
            "type_of_emission"
        ],

        df
    )

    print(
        "Current DB rows:",
        get_row_count(
            conn,
            "national_sectoral_emissions"
        )
    )

    # 5. PRE/POST AGRICULTURAL EMISSION
    # ---------------------------------

    print(
        "\n-----"
    )
    print(
        "5. PRE/POST AGRICULTURAL EMISSION"
    )
    print(
        "-----"
    )

    df = read_csv(
        root,
        "emission_from_pre_post_agri.csv"
    )

    df = df.rename(
        columns={

            "Type_of_Emission":
                "type_of_emission"
        }
    )

    df["source_id"] = clean_num(
        df["source_id"]
    )

    df["year"] = clean_num(
        df["year"]
    )

    df["emissions_quantity"] = clean_num(
        df["emissions_quantity"]
    )

    df = df[
        df["country_name"].notna() &
        df["source_id"].notna() &
        df["year"].notna() &
        df["gas_name"].notna() &
        df["type_of_emission"].notna()
    ]

    ins, fail = insert_df(

        conn,

        "emission_from_pre_post_agri",

        [
            "country_name",
            "source_id",
            "source",
            "year",
            "unit",
            "emissions_quantity",
            "gas_name",
            "type_of_emission"
        ],

        df
    )

    print(
        "Current DB rows:",
        get_row_count(
            conn,
            "emission_from_pre_post_agri"
        )
    )



    # 6. CITY LEVEL GAS EMISSIONS
    # ---------------------------

    print(
        "\n-----"
    )
    print(
        "6. CITY LEVEL GAS EMISSIONS"
    )
    print(
        "----------------------------------------------------"
    )

    df = read_csv(
        root,
        "city_level_gas_emissions.csv"
    )

    df = df.rename(
        columns={

            "Type_of_Emissions":
                "type_of_emissions"
        }
    )

    df["year"] = clean_num(
        df["year"]
    )

    df["month"] = clean_num(
        df["month"]
    )

    df["emissions_quantity"] = clean_num(
        df["emissions_quantity"]
    )

    # Clean city names
    df["city_name"] = df[
        "city_name"
    ].map(norm_text)

    df["sector_name"] = df[
        "sector_name"
    ].map(norm_text)

    df["gas_name"] = df[
        "gas_name"
    ].map(norm_text)

    df["type_of_emissions"] = df[
        "type_of_emissions"
    ].map(norm_text)

    # Required PK columns
    df = df[
        df["city_name"].notna() &
        df["year"].notna() &
        df["month"].notna() &
        df["sector_name"].notna() &
        df["gas_name"].notna() &
        df["type_of_emissions"].notna()
    ]

    ins, fail = insert_df(

        conn,

        "city_level_gas_emissions",

        [
            "city_name",
            "year",
            "month",
            "sector_name",
            "gas_name",
            "emissions_quantity",
            "type_of_emissions"
        ],

        df
    )

    print(
        "Current DB rows:",
        get_row_count(
            conn,
            "city_level_gas_emissions"
        )
    )


    # 7. SOURCE LEVEL GAS EMISSION
    # ----------------------------

    print(
        "\n----------------"
    )
    print(
        "7. SOURCE LEVEL GAS EMISSION"
    )
    print(
        "-------------------"
    )

    df = read_csv(
        root,
        "source_level_gas_emission.csv"
    )

    df = df.rename(
        columns={

            "subsector name":
                "subsector_name",

            "Type of Emission":
                "type_of_emission"
        }
    )

    df["longitude"] = clean_num(
        df["longitude"]
    )

    df["latitude"] = clean_num(
        df["latitude"]
    )

    df["emissions_quantity"] = clean_num(
        df["emissions_quantity"]
    )

    df["emissions_factor"] = clean_num(
        df["emissions_factor"]
    )

    df["year"] = clean_num(
        df["year"]
    )

    df["city_name"] = df[
        "city_name"
    ].map(norm_text)

    df["sector_name"] = df[
        "sector_name"
    ].map(norm_text)

    df["subsector_name"] = df[
        "subsector_name"
    ].map(norm_text)

    df["gas_name"] = df[
        "gas_name"
    ].map(norm_text)

    df["type_of_emission"] = df[
        "type_of_emission"
    ].map(norm_text)

    df = df[
        df["city_name"].notna() &
        df["sector_name"].notna() &
        df["subsector_name"].notna() &
        df["gas_name"].notna() &
        df["year"].notna() &
        df["type_of_emission"].notna()
    ]

    ins, fail = insert_df(

        conn,

        "source_level_gas_emission",

        [
            "city_name",
            "sector_name",
            "subsector_name",
            "longitude",
            "latitude",
            "gas_name",
            "emissions_quantity",
            "emissions_factor",
            "units",
            "year",
            "type_of_emission"
        ],

        df
    )

    print(
        "Current DB rows:",
        get_row_count(
            conn,
            "source_level_gas_emission"
        )
    )



    # FINAL CHECK
    #-------------------
    

    conn.commit()

    print(
        "\n\n====="
    )

    print(
        "             FINAL TABLE CHECK"
    )

    print(
        "=====\n"
    )

    target_tables = [

        "surface_air_temp",

        "river_morphology",

        "country_level_gas_emission",

        "national_sectoral_emissions",

        "emission_from_pre_post_agri",

        "city_level_gas_emissions",

        "source_level_gas_emission"
    ]

    cur = conn.cursor()

    for table in target_tables:

        cur.execute(
            f"SELECT COUNT(*) FROM `{table}`"
        )

        count = cur.fetchone()[0]

        print(
            f"{table:45} : {count} rows"
        )

    cur.close()

    conn.close()

    print(
        "\n====="
    )

    print(
        "             ETL COMPLETED"
    )

    print(
        "======"
    )


# RUN


if __name__ == "__main__":
    main()