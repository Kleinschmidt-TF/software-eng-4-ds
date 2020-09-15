CREATE TABLE IF NOT EXISTS stores (
    store_id serial PRIMARY KEY,
    city VARCHAR (50) UNIQUE,
    surface_area FLOAT
)
