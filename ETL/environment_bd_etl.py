import os
import zipfile
from pathlib import Path

import mysql.connector
import pandas as pd
import numpy as np

# CONFIGURATION
# -------------------------------
ZIP_FILE = r"C:\Users\User\Downloads\NEW_dataset.zip"
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "******"
DB_PASSWORD = "******"
DB_NAME = "environment_bd"

BATCH_SIZE = 1000

# The ZIP must contain:
# Datasets(Updated)/Country.csv
# Datasets(Updated)/Division.csv
# ...
# Datasets(Updated)/daily_sunshine.csv

# HELPERS
# ------------------------------
def norm_text(x):
    if pd.isna(x):
        return None
    x = str(x).strip()
    return x if x else None


def clean_df(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    for c in df.columns:
        if df[c].dtype == "object":
            df[c] = df[c].map(norm_text)
    return df


def clean_num(s):
    return pd.to_numeric(
        s.astype(str).str.replace(",", "", regex=False).replace(
            {"nan": np.nan, "None": np.nan, "": np.nan}
        ),
        errors="coerce"
    )


def clean_date(s):
    return pd.to_datetime(s, errors="coerce").dt.date


def read_csv(root, filename):
    path = root / filename
    df = pd.read_csv(path, low_memory=False)
    return clean_df(df)


def insert_df(conn, table, columns, df):
    if df.empty:
        print(f"{table:40} CSV=0  INSERTED=0")
        return 0, 0

    # Remove duplicate rows according to the DataFrame's complete columns.
    work = df[columns].copy()
    work = work.drop_duplicates()

    placeholders = ",".join(["%s"] * len(columns))
    col_sql = ",".join(f"`{c}`" for c in columns)

    # REPLACE/UPDATE behavior is intentionally avoided.
    # INSERT IGNORE lets duplicate PK rows be skipped without stopping ETL.
    sql = f"INSERT IGNORE INTO `{table}` ({col_sql}) VALUES ({placeholders})"

    cur = conn.cursor()
    inserted = 0
    failed = 0

    for start in range(0, len(work), BATCH_SIZE):
        batch = work.iloc[start:start+BATCH_SIZE]
        values = []
        for row in batch.itertuples(index=False, name=None):
            values.append(tuple(None if pd.isna(v) else v for v in row))

        try:
            cur.executemany(sql, values)
            conn.commit()
            inserted += cur.rowcount
        except Exception as e:
            conn.rollback()
            # Retry row-by-row so one bad record does not hide valid records.
            for row in values:
                try:
                    cur.execute(sql, row)
                    inserted += cur.rowcount
                except Exception:
                    failed += 1
            conn.commit()

    cur.close()
    print(f"{table:40} CSV={len(df):8} INSERTED={inserted:8} FAILED={failed:8}")
    return inserted, failed


def write_log(conn, table, csv_rows, inserted, failed):
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO daily_data_load_log
           (table_name, csv_rows, inserted_rows, failed_rows)
           VALUES (%s,%s,%s,%s)
           ON DUPLICATE KEY UPDATE
           csv_rows=VALUES(csv_rows),
           inserted_rows=VALUES(inserted_rows),
           failed_rows=VALUES(failed_rows),
           load_time=CURRENT_TIMESTAMP""",
        (table, int(csv_rows), int(inserted), int(failed))
    )
    conn.commit()
    cur.close()


# MAIN
# -----------------------------
def main():
    zip_path = Path(ZIP_FILE)

    if not zip_path.exists():
        raise FileNotFoundError(f"ZIP file not found: {zip_path}")

    extract_dir = zip_path.parent / "environment_data_extracted"

    if extract_dir.exists():
        import shutil
        shutil.rmtree(extract_dir)

    extract_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_dir)

    # Find the directory containing the CSVs.
    csv_files = list(extract_dir.rglob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CSV files were found inside the ZIP.")

    root = csv_files[0].parent
    print("CSV directory:", root)
    print("CSV files found:", len(csv_files))

    if len(csv_files) != 29:
        print("WARNING: Expected 29 CSV files.")

    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        autocommit=False
    )

    # 1. COUNTRY
    # --------------------------------------------------------
    df = read_csv(root, "Country.csv")
    ins, fail = insert_df(conn, "country",
                          ["country_name"], df)
    write_log(conn, "country", len(df), ins, fail)

    # 2. DIVISION
    # --------------------------------------------------------
    df = read_csv(root, "Division.csv")
    df = df.rename(columns={"country": "country_name"})
    ins, fail = insert_df(conn, "division",
                          ["division_id", "division_name", "country_name"], df)
    write_log(conn, "division", len(df), ins, fail)

    # 3. DISTRICT
    # --------------------------------------------------------
    df = read_csv(root, "District.csv")
    ins, fail = insert_df(conn, "district",
                          ["district_id", "district_name", "division_id"], df)
    write_log(conn, "district", len(df), ins, fail)

    # 4. UPAZILA
    # --------------------------------------------------------
    df = read_csv(root, "Upazila.csv")
    ins, fail = insert_df(conn, "upazila",
                          ["upazila_name", "district_id"], df)
    write_log(conn, "upazila", len(df), ins, fail)

    # 5. THANA
    # --------------------------------------------------------
    df = read_csv(root, "Thana.csv")
    df = df.rename(columns={"upzila_name": "upzila_name"})
    ins, fail = insert_df(conn, "thana",
                          ["thana_name", "upzila_name"], df)
    write_log(conn, "thana", len(df), ins, fail)

    # 6. UNION
    # --------------------------------------------------------
    df = read_csv(root, "Union.csv")
    df = df.rename(columns={"Union_name": "union_name"})
    ins, fail = insert_df(conn, "union_area",
                          ["union_name", "thana_name"], df)
    write_log(conn, "union_area", len(df), ins, fail)


    # 7. MOUZA
    # --------------------------------------------------------
    df = read_csv(root, "Mouza.csv")
    df = df.rename(columns={"Union_name": "union_name",
                            "Mouza_name": "mouza_name"})
    ins, fail = insert_df(conn, "mouza",
                          ["mouza_name", "union_name"], df)
    write_log(conn, "mouza", len(df), ins, fail)

    # 8. CITY
    # --------------------------------------------------------
    df = read_csv(root, "city.csv")
    df = df.rename(columns={
        "City Name": "city_name",
        "District Name": "district_name",
        "District ID": "district_id"
    })
    ins, fail = insert_df(conn, "city",
                          ["city_name", "district_name", "district_id"], df)
    write_log(conn, "city", len(df), ins, fail)

    
    # 9-11. WEATHER STATIONS
    # --------------------------------------------------------
    station_specs = [
        ("temp_station.csv", "temp_station",
         ["temp_station_name", "district_id"]),
        ("humidity_station.csv", "humidity_station",
         ["humidity_station_name", "district_id"]),
        ("sunshine_station.csv", "sunshine_station",
         ["sunshine_station_name", "district_id"]),
    ]

    for filename, table, cols in station_specs:
        df = read_csv(root, filename)
        ins, fail = insert_df(conn, table, cols, df)
        write_log(conn, table, len(df), ins, fail)

  
    # 12. RIVER STATION
    # --------------------------------------------------------
    df = read_csv(root, "river_station.csv")
    df = df.rename(columns={
        "River_Station_ID": "river_station_id",
        "River_Station_Name": "river_station_name",
        "River_Name": "river_name",
        "upazila_name": "upazila_name",
        "latitude": "latitude",
        "longitude": "longitude"
    })
    df["latitude"] = clean_num(df["latitude"])
    df["longitude"] = clean_num(df["longitude"])
    ins, fail = insert_df(conn, "river_station",
                          ["river_station_id", "river_station_name",
                           "river_name", "upazila_name",
                           "latitude", "longitude"], df)
    write_log(conn, "river_station", len(df), ins, fail)

    # 13. ENVIRONMENT INDICATOR
    # --------------------------------------------------------
    df = read_csv(root, "Environment_Indicator.csv")
    df = df.rename(columns={
        "indicator's_value": "indicator_value",
        "Country": "country_name"
    })
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["indicator_value"] = clean_num(df["indicator_value"])
    ins, fail = insert_df(conn, "environment_indicator",
                          ["year", "indicator_name", "indicator_code",
                           "indicator_value", "country_name"], df)
    write_log(conn, "environment_indicator", len(df), ins, fail)


    # 14. RAINFALL
    # --------------------------------------------------------
    df = read_csv(root, "Rainfall.csv")
    df = df.rename(columns={
        "10_day_rainfall_mm": "ten_day_rainfall_mm",
        "1 month_aggregation_mm": "one_month_aggregation_mm",
        "1 month_aggregation_long_term_avg_mm":
            "one_month_aggregation_long_term_avg_mm",
        "3 month_aggregation_mm": "three_month_aggregation_mm",
        "3 month_aggregation_mm.1":
            "three_month_aggregation_long_term_avg_mm",
        "anomaly": "anomaly",
        "1 month_anomaly": "one_month_anomaly",
        "3 month_anomaly": "three_month_anomaly"
    })
    df["date"] = clean_date(df["date"])
    numeric_cols = [
        "ten_day_rainfall_mm", "long_term_avg_mm",
        "one_month_aggregation_mm",
        "one_month_aggregation_long_term_avg_mm",
        "three_month_aggregation_mm",
        "three_month_aggregation_long_term_avg_mm",
        "anomaly", "one_month_anomaly", "three_month_anomaly"
    ]
    for c in numeric_cols:
        df[c] = clean_num(df[c])

    ins, fail = insert_df(conn, "rainfall",
                          ["date", "district_id"] + numeric_cols, df)
    write_log(conn, "rainfall", len(df), ins, fail)

   
    # 15. FLOOD
    # --------------------------------------------------------
    df = read_csv(root, "Flood.csv")
    df = df.rename(columns={
        "Division": "division_name",
        "District_id": "district_id",
        "district": "district_name",
        "Last date": "last_date",
        "pct_of_cropland_flooded": "pct_of_cropland_flooded",
        "pct_of_total_area_flooded": "pct_of_total_area_flooded"
    })
    df["start_date"] = clean_date(df["start_date"])
    df["last_date"] = clean_date(df["last_date"])
    num_cols = [
        "cropland_flooded_sq_km", "cropland_flooded_ha",
        "total_area_flooded_sq_km", "total_area_flooded_ha",
        "pct_of_cropland_flooded", "pct_of_total_area_flooded",
        "population_exposed"
    ]
    for c in num_cols:
        df[c] = clean_num(df[c])
    ins, fail = insert_df(conn, "flood",
                          ["division_id", "division_name", "district_id",
                           "district_name", "period_number", "start_date",
                           "last_date"] + num_cols, df)
    write_log(conn, "flood", len(df), ins, fail)

    # 16. SEDIMENT
    # --------------------------------------------------------
    df = read_csv(root, "Sediment.csv")
    df = df.rename(columns={
        "River_Station_ID": "river_station_id",
        "River_Station Name": "river_station_name",
        "River_Name": "river_name",
        "district": "district_name",
        "upazila": "upazila_name",
        "start_date": "start_date",
        "Last_date": "last_date"
    })
    df["start_date"] = clean_date(df["start_date"])
    df["last_date"] = clean_date(df["last_date"])
    df["latitude"] = clean_num(df["latitude"])
    df["longitude"] = clean_num(df["longitude"])
    ins, fail = insert_df(conn, "sediment",
                          ["river_station_id", "river_station_name",
                           "river_name", "district_name", "upazila_name",
                           "latitude", "longitude", "start_date",
                           "last_date"], df)
    write_log(conn, "sediment", len(df), ins, fail)

    # 17. LAND USE
    # --------------------------------------------------------
    df = read_csv(root, "land_use.csv")
    df = df.rename(columns={
        "Country_name": "country_name",
        "Land_category_code": "land_category_code",
        "Land_category": "land_category",
        "Year": "year",
        "Unit": "unit",
        "Value": "value"
    })
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["land_category_code"] = pd.to_numeric(
        df["land_category_code"], errors="coerce"
    )
    df["value"] = clean_num(df["value"])
    ins, fail = insert_df(conn, "land_use",
                          ["country_name", "land_category_code",
                           "land_category", "year", "unit", "value"], df)
    write_log(conn, "land_use", len(df), ins, fail)


    # 18. ARSENIC
    # --------------------------------------------------------
    df = read_csv(root, "arsenic_contamination.csv")
    df = df.rename(columns={
        "Sample_ID": "sample_id",
        "Sample_Field_ID": "sample_field_id",
        "Date": "sample_date",
        "Lat_Deg": "lat_deg",
        "Long_Deg": "long_deg",
        "Well_Type": "well_type",
        "Well_Depth_m": "well_depth_m",
        "Division": "division",
        "District": "district",
        "Thana": "thana",
        "Union": "union_name",
        "Mouza": "mouza",
        "element_symbol": "element_symbol",
        "element_unit": "element_unit",
        "measured_value": "measured_value"
    })
    df["sample_date"] = clean_date(df["sample_date"])
    for c in ["lat_deg", "long_deg", "well_depth_m", "measured_value"]:
        df[c] = clean_num(df[c])
    ins, fail = insert_df(conn, "arsenic_contamination",
                          ["sample_id", "sample_field_id", "sample_date",
                           "lat_deg", "long_deg", "well_type", "well_depth_m",
                           "division", "district", "thana", "union_name",
                           "mouza", "element_symbol", "element_unit",
                           "measured_value"], df)
    write_log(conn, "arsenic_contamination", len(df), ins, fail)

    
    # 19-21. DAILY WEATHER
    # --------------------------------------------------------
    daily_specs = [
        ("daily_temp_change.csv", "daily_temp_change",
         {"temp_station_name": "temp_station_name",
          "record_date": "record_date", "temp_value": "temp_value"},
         ["temp_station_name", "record_date", "temp_value"]),
        ("daily_humidity.csv", "daily_humidity",
         {"humidity_station_name": "humidity_station_name",
          "record_date": "record_date", "humidity_value": "humidity_value"},
         ["humidity_station_name", "record_date", "humidity_value"]),
        ("Daily_sunshine.csv", "daily_sunshine",
         {"sunshine_station_name": "sunshine_station_name",
          "record_date": "record_date", "sunshine_hours": "sunshine_hours"},
         ["sunshine_station_name", "record_date", "sunshine_hours"])
    ]

    for filename, table, mapping, cols in daily_specs:
        df = read_csv(root, filename)
        df = df.rename(columns=mapping)
        df["record_date"] = clean_date(df["record_date"])

        value_col = cols[2]
        df[value_col] = clean_num(df[value_col])

        # Remove extra spaces from station names, e.g. " Bogura  ".
        df[cols[0]] = df[cols[0]].map(norm_text)

        # Keep only rows that have a valid station name and date.
        df = df[df[cols[0]].notna() & df["record_date"].notna()]

        ins, fail = insert_df(conn, table, cols, df)
        write_log(conn, table, len(df), ins, fail)

    # 22. PRECIPITATION
    # --------------------------------------------------------
    df = read_csv(root, "precipitation.csv")
    df = df.rename(columns={
        "5year_gaussian_smooth_precipitation":
            "five_year_gaussian_smooth_precipitation",
        "Country": "country_name"
    })
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["precipitation_mm"] = clean_num(df["precipitation_mm"])
    df["five_year_gaussian_smooth_precipitation"] = clean_num(
        df["five_year_gaussian_smooth_precipitation"]
    )
    ins, fail = insert_df(conn, "precipitation",
                          ["year", "precipitation_mm",
                           "five_year_gaussian_smooth_precipitation",
                           "country_name"], df)
    write_log(conn, "precipitation", len(df), ins, fail)

    
    # 23. SURFACE AIR TEMP
    # --------------------------------------------------------
    df = read_csv(root, "surface_air_temp.csv")
    df = df.rename(columns={
        "max _sur_temp_cel": "max_sur_temp_cel",
        "Country_name": "country_name"
    })
    for c in ["year"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    for c in [
        "mean_sur_temp_cel", "five_year_gaussian_smooth_mean",
        "max_sur_temp_cel", "five_year_gaussian_smooth_max",
        "min_sur_temp_cel", "five_year_gaussian_smooth_min"
    ]:
        df[c] = clean_num(df[c])
    ins, fail = insert_df(conn, "surface_air_temp",
                          ["year", "mean_sur_temp_cel",
                           "five_year_gaussian_smooth_mean",
                           "max_sur_temp_cel",
                           "five_year_gaussian_smooth_max",
                           "min_sur_temp_cel",
                           "five_year_gaussian_smooth_min",
                           "country_name"], df)
    write_log(conn, "surface_air_temp", len(df), ins, fail)

    
    # 24. RIVER MORPHOLOGY
    # --------------------------------------------------------
    df = read_csv(root, "river_morphology.csv")
    df = df.rename(columns={
        "River_Station_ID": "river_station_id",
        "River_Name": "river_name",
        "Rotation_of_river_survey": "rotation_of_river_survey",
        "District": "district",
        "Upazila": "upazila",
        "Latitude": "latitude",
        "Longitude": "longitude",
        "start_date": "start_date",
        "last_date": "last_date"
    })
    df["latitude"] = clean_num(df["latitude"])
    df["longitude"] = clean_num(df["longitude"])
    df["start_date"] = clean_date(df["start_date"])
    df["last_date"] = clean_date(df["last_date"])
    ins, fail = insert_df(conn, "river_morphology",
                          ["river_station_id", "river_name",
                           "rotation_of_river_survey", "district",
                           "upazila", "latitude", "longitude",
                           "start_date", "last_date"], df)
    write_log(conn, "river_morphology", len(df), ins, fail)

    
    # 25. COUNTRY-LEVEL GAS EMISSION
    # --------------------------------------------------------
    df = read_csv(root, "country_level_gas_emission.csv")
    df = df.rename(columns={
        "Source_Code": "source_code",
        "Source": "source",
        "Year": "year",
        "Unit": "unit",
        "Emissions_Quantity": "emissions_quantity",
        "Gas_Name": "gas_name",
        "Type_of_Emissions": "type_of_emissions"
    })
    df["source_code"] = pd.to_numeric(df["source_code"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["emissions_quantity"] = clean_num(df["emissions_quantity"])
    ins, fail = insert_df(conn, "country_level_gas_emission",
                          ["country_name", "source_code", "source", "year",
                           "unit", "emissions_quantity", "gas_name",
                           "type_of_emissions"], df)
    write_log(conn, "country_level_gas_emission", len(df), ins, fail)

    
    # 26. NATIONAL SECTORAL EMISSIONS
    # --------------------------------------------------------
    df = read_csv(root, "national_sectoral_emissions.csv")
    df = df.rename(columns={
        "Country_name": "country_name",
        "Source_ID": "source_id",
        "Source": "source",
        "Year": "year",
        "Unit": "unit",
        "Emissions_Quantity": "emissions_quantity",
        "Gas_Name": "gas_name",
        "Type_of_Emission": "type_of_emission"
    })
    df["source_id"] = pd.to_numeric(df["source_id"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["emissions_quantity"] = clean_num(df["emissions_quantity"])
    ins, fail = insert_df(conn, "national_sectoral_emissions",
                          ["country_name", "source_id", "source", "year",
                           "unit", "emissions_quantity", "gas_name",
                           "type_of_emission"], df)
    write_log(conn, "national_sectoral_emissions", len(df), ins, fail)

    # 27. PRE/POST AGRICULTURAL EMISSION
    # --------------------------------------------------------
    df = read_csv(root, "emission_from_pre_post_agri.csv")
    df = df.rename(columns={
        "source_id": "source_id",
        "emissions_quantity": "emissions_quantity",
        "Type_of_Emission": "type_of_emission"
    })
    df["source_id"] = pd.to_numeric(df["source_id"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["emissions_quantity"] = clean_num(df["emissions_quantity"])
    ins, fail = insert_df(conn, "emission_from_pre_post_agri",
                          ["country_name", "source_id", "source", "year",
                           "unit", "emissions_quantity", "gas_name",
                           "type_of_emission"], df)
    write_log(conn, "emission_from_pre_post_agri", len(df), ins, fail)

    
    # 28. CITY-LEVEL GAS EMISSIONS
    # --------------------------------------------------------
    df = read_csv(root, "city_level_gas_emissions.csv")
    df = df.rename(columns={
        "Type_of_Emissions": "type_of_emissions"
    })
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["month"] = pd.to_numeric(df["month"], errors="coerce")
    df["emissions_quantity"] = clean_num(df["emissions_quantity"])
    ins, fail = insert_df(conn, "city_level_gas_emissions",
                          ["city_name", "year", "month", "sector_name",
                           "gas_name", "emissions_quantity",
                           "type_of_emissions"], df)
    write_log(conn, "city_level_gas_emissions", len(df), ins, fail)

    
    # 29. SOURCE-LEVEL GAS EMISSION
    # --------------------------------------------------------
    df = read_csv(root, "source_level_gas_emission.csv")
    df = df.rename(columns={
        "subsector name": "subsector_name",
        "Type of Emission": "type_of_emission"
    })
    df["longitude"] = clean_num(df["longitude"])
    df["latitude"] = clean_num(df["latitude"])
    df["emissions_quantity"] = clean_num(df["emissions_quantity"])
    df["emissions_factor"] = clean_num(df["emissions_factor"])
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    ins, fail = insert_df(conn, "source_level_gas_emission",
                          ["city_name", "sector_name", "subsector_name",
                           "longitude", "latitude", "gas_name",
                           "emissions_quantity", "emissions_factor",
                           "units", "year", "type_of_emission"], df)
    write_log(conn, "source_level_gas_emission", len(df), ins, fail)

    
    # FINAL
    # --------------------------------------------------------
    conn.commit()

    print("\n==== FINAL ROW COUNTS ===")
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name, csv_rows, inserted_rows, failed_rows
        FROM daily_data_load_log
        ORDER BY table_name
    """)
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()

    print("\nETL COMPLETED.")


if __name__ == "__main__":
    main()