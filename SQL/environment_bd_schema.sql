DROP DATABASE IF EXISTS environment_bd;
CREATE DATABASE environment_bd CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE environment_bd;

CREATE TABLE country (
    country_name VARCHAR(100) PRIMARY KEY
);

CREATE TABLE division (
    division_id VARCHAR(20) PRIMARY KEY,
    division_name VARCHAR(100) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (country_name) REFERENCES country(country_name)
);

CREATE TABLE district (
    district_id VARCHAR(20) PRIMARY KEY,
    district_name VARCHAR(100) NOT NULL,
    division_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (division_id) REFERENCES division(division_id)
);

CREATE TABLE upazila (
    upazila_name VARCHAR(150) PRIMARY KEY,
    district_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (district_id) REFERENCES district(district_id)
);

CREATE TABLE thana (
    thana_name VARCHAR(150) PRIMARY KEY,
    upzila_name VARCHAR(150) NOT NULL,
    FOREIGN KEY (upzila_name) REFERENCES upazila(upazila_name)
);

CREATE TABLE union_area (
    union_name VARCHAR(150) PRIMARY KEY,
    thana_name VARCHAR(150) NOT NULL,
    FOREIGN KEY (thana_name) REFERENCES thana(thana_name)
);

CREATE TABLE mouza (
    mouza_name VARCHAR(150) PRIMARY KEY,
    union_name VARCHAR(150) NOT NULL,
    FOREIGN KEY (union_name) REFERENCES union_area(union_name)
);

CREATE TABLE city (
    city_name VARCHAR(150) PRIMARY KEY,
    district_name VARCHAR(100),
    district_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (district_id) REFERENCES district(district_id)
);

CREATE TABLE temp_station (
    temp_station_name VARCHAR(150) PRIMARY KEY,
    district_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (district_id) REFERENCES district(district_id)
);

CREATE TABLE humidity_station (
    humidity_station_name VARCHAR(150) PRIMARY KEY,
    district_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (district_id) REFERENCES district(district_id)
);

CREATE TABLE sunshine_station (
    sunshine_station_name VARCHAR(150) PRIMARY KEY,
    district_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (district_id) REFERENCES district(district_id)
);

CREATE TABLE river_station (
    river_station_id VARCHAR(50) PRIMARY KEY,
    river_station_name VARCHAR(200) NOT NULL,
    river_name VARCHAR(200) NOT NULL,
    upazila_name VARCHAR(150),
    latitude DECIMAL(12,6),
    longitude DECIMAL(12,6),
    FOREIGN KEY (upazila_name) REFERENCES upazila(upazila_name)
);

CREATE TABLE environment_indicator (
    year INT NOT NULL,
    indicator_name VARCHAR(255) NOT NULL,
    indicator_code VARCHAR(100) NOT NULL,
    indicator_value DECIMAL(20,8),
    country_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (year, indicator_code, country_name),
    FOREIGN KEY (country_name) REFERENCES country(country_name)
);

CREATE TABLE rainfall (
    date DATE NOT NULL,
    district_id VARCHAR(20) NOT NULL,
    ten_day_rainfall_mm DECIMAL(20,8),
    long_term_avg_mm DECIMAL(20,8),
    one_month_aggregation_mm DECIMAL(20,8),
    one_month_aggregation_long_term_avg_mm DECIMAL(20,8),
    three_month_aggregation_mm DECIMAL(20,8),
    three_month_aggregation_long_term_avg_mm DECIMAL(20,8),
    anomaly DECIMAL(20,8),
    one_month_anomaly DECIMAL(20,8),
    three_month_anomaly DECIMAL(20,8),
    PRIMARY KEY (district_id, date),
    FOREIGN KEY (district_id) REFERENCES district(district_id)
);

CREATE TABLE flood (
    division_id VARCHAR(20),
    division_name VARCHAR(100),
    district_id VARCHAR(20) NOT NULL,
    district_name VARCHAR(100),
    period_number INT NOT NULL,
    start_date DATE,
    last_date DATE,
    cropland_flooded_sq_km DECIMAL(20,8),
    cropland_flooded_ha DECIMAL(20,8),
    total_area_flooded_sq_km DECIMAL(20,8),
    total_area_flooded_ha DECIMAL(20,8),
    pct_of_cropland_flooded DECIMAL(20,8),
    pct_of_total_area_flooded DECIMAL(20,8),
    population_exposed BIGINT,
    PRIMARY KEY (district_id, period_number),
    FOREIGN KEY (district_id) REFERENCES district(district_id)
);

CREATE TABLE sediment (
    river_station_id VARCHAR(50) NOT NULL,
    river_station_name VARCHAR(200),
    river_name VARCHAR(200),
    district_name VARCHAR(100),
    upazila_name VARCHAR(150),
    latitude DECIMAL(12,6),
    longitude DECIMAL(12,6),
    start_date DATE,
    last_date DATE,
    PRIMARY KEY (river_station_id, start_date, last_date),
    FOREIGN KEY (river_station_id) REFERENCES river_station(river_station_id)
);

CREATE TABLE land_use (
    country_name VARCHAR(100) NOT NULL,
    land_category_code INT,
    land_category VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    unit VARCHAR(50),
    value DECIMAL(20,8),
    PRIMARY KEY (country_name, land_category_code, land_category, year, unit),
    FOREIGN KEY (country_name) REFERENCES country(country_name)
);

CREATE TABLE arsenic_contamination (
    sample_id VARCHAR(100) PRIMARY KEY,
    sample_field_id VARCHAR(100),
    sample_date DATE,
    lat_deg DECIMAL(12,6),
    long_deg DECIMAL(12,6),
    well_type VARCHAR(100),
    well_depth_m DECIMAL(12,4),
    division VARCHAR(100),
    district VARCHAR(100),
    thana VARCHAR(150),
    union_name VARCHAR(150),
    mouza VARCHAR(150),
    element_symbol VARCHAR(20),
    element_unit VARCHAR(50),
    measured_value DECIMAL(20,8)
);

CREATE TABLE daily_temp_change (
    temp_station_name VARCHAR(150) NOT NULL,
    record_date DATE NOT NULL,
    temp_value DECIMAL(12,4),
    PRIMARY KEY (temp_station_name, record_date),
    FOREIGN KEY (temp_station_name) REFERENCES temp_station(temp_station_name)
);

CREATE TABLE daily_humidity (
    humidity_station_name VARCHAR(150) NOT NULL,
    record_date DATE NOT NULL,
    humidity_value DECIMAL(12,4),
    PRIMARY KEY (humidity_station_name, record_date),
    FOREIGN KEY (humidity_station_name) REFERENCES humidity_station(humidity_station_name)
);

CREATE TABLE daily_sunshine (
    sunshine_station_name VARCHAR(150) NOT NULL,
    record_date DATE NOT NULL,
    sunshine_hours DECIMAL(12,4),
    PRIMARY KEY (sunshine_station_name, record_date),
    FOREIGN KEY (sunshine_station_name) REFERENCES sunshine_station(sunshine_station_name)
);

CREATE TABLE precipitation (
    year INT PRIMARY KEY,
    precipitation_mm DECIMAL(20,8),
    five_year_gaussian_smooth_precipitation DECIMAL(20,8),
    country_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (country_name) REFERENCES country(country_name)
);

CREATE TABLE surface_air_temp (
    year INT PRIMARY KEY,
    mean_sur_temp_cel DECIMAL(12,6),
    five_year_gaussian_smooth_mean DECIMAL(12,6),
    max_sur_temp_cel DECIMAL(12,6),
    five_year_gaussian_smooth_max DECIMAL(12,6),
    min_sur_temp_cel DECIMAL(12,6),
    five_year_gaussian_smooth_min DECIMAL(12,6),
    country_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (country_name) REFERENCES country(country_name)
);

CREATE TABLE river_morphology (
    river_station_id VARCHAR(50) PRIMARY KEY,
    river_name VARCHAR(200),
    rotation_of_river_survey VARCHAR(100),
    district VARCHAR(100),
    upazila VARCHAR(150),
    latitude DECIMAL(12,6),
    longitude DECIMAL(12,6),
    start_date DATE,
    last_date DATE
);

CREATE TABLE country_level_gas_emission (
    country_name VARCHAR(100) NOT NULL,
    source_code INT NOT NULL,
    source VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    unit VARCHAR(50),
    emissions_quantity DECIMAL(20,8),
    gas_name VARCHAR(50) NOT NULL,
    type_of_emissions VARCHAR(100),
    PRIMARY KEY (country_name, source_code, year, gas_name, type_of_emissions),
    FOREIGN KEY (country_name) REFERENCES country(country_name)
);

CREATE TABLE national_sectoral_emissions (
    country_name VARCHAR(100) NOT NULL,
    source_id INT NOT NULL,
    source VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    unit VARCHAR(50),
    emissions_quantity DECIMAL(20,8),
    gas_name VARCHAR(50) NOT NULL,
    type_of_emission VARCHAR(100),
    PRIMARY KEY (country_name, source_id, year, gas_name, type_of_emission),
    FOREIGN KEY (country_name) REFERENCES country(country_name)
);

CREATE TABLE emission_from_pre_post_agri (
    country_name VARCHAR(100) NOT NULL,
    source_id INT NOT NULL,
    source VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    unit VARCHAR(50),
    emissions_quantity DECIMAL(20,8),
    gas_name VARCHAR(50) NOT NULL,
    type_of_emission VARCHAR(100),
    PRIMARY KEY (country_name, source_id, year, gas_name, type_of_emission),
    FOREIGN KEY (country_name) REFERENCES country(country_name)
);

CREATE TABLE city_level_gas_emissions (
    city_name VARCHAR(150) NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    sector_name VARCHAR(150) NOT NULL,
    gas_name VARCHAR(50) NOT NULL,
    emissions_quantity DECIMAL(20,8),
    type_of_emissions VARCHAR(100),
    PRIMARY KEY (city_name, year, month, sector_name, gas_name, type_of_emissions),
    FOREIGN KEY (city_name) REFERENCES city(city_name)
);

CREATE TABLE source_level_gas_emission (
    city_name VARCHAR(150) NOT NULL,
    sector_name VARCHAR(150) NOT NULL,
    subsector_name VARCHAR(255) NOT NULL,
    longitude DECIMAL(12,6),
    latitude DECIMAL(12,6),
    gas_name VARCHAR(50) NOT NULL,
    emissions_quantity DECIMAL(20,8),
    emissions_factor DECIMAL(20,12),
    units VARCHAR(100),
    year INT NOT NULL,
    type_of_emission VARCHAR(100),
    PRIMARY KEY (city_name, sector_name, subsector_name, gas_name, year, type_of_emission),
    FOREIGN KEY (city_name) REFERENCES city(city_name)
);

CREATE TABLE daily_data_load_log (
    table_name VARCHAR(100) PRIMARY KEY,
    csv_rows BIGINT,
    inserted_rows BIGINT,
    failed_rows BIGINT,
    load_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);