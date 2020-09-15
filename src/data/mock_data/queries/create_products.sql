CREATE TABLE IF NOT EXISTS products (
    product_id serial PRIMARY KEY,
    product_name VARCHAR (50) UNIQUE NOT NULL,
    gross_price FLOAT,
    color VARCHAR (50),
    supplier VARCHAR (50)
)
