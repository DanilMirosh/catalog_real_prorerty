CREATE DATABASE realestate_catalog;

CREATE TABLE properties (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    address VARCHAR(255),
    floor INTEGER,
    area FLOAT,
    type VARCHAR(255),
    metro_stations VARCHAR(255)
);
