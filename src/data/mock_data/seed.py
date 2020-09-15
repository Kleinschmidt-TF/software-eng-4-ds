import numpy as np
import pandas as pd
import yaml
from box import Box

from src.services.constant.fields import Fields
from src.services.service_provider import ServiceProviderHandler

SERVICE = ServiceProviderHandler()


def seed_product_table():

    SERVICE.log.info('Create SQL product table')

    # 1. create table
    with open('src/data/mock_data/queries/create_products.sql', 'r') as file:
        query = ''.join(file.readlines())
    SERVICE.db.execute(query)

    # 2. fill the table with data
    df = pd.read_csv('src/data/mock_data/mock_data/product_mock.csv')
    df["gross_price"] = df.gross_price.apply(
        lambda x: float(x[1:].replace(',', '.')))
    SERVICE.db.write(df, Fields.PRODUCT_TABLE, if_exists='replace', index=False)


def seed_store_table():

    SERVICE.log.info('Create SQL store table')

    # 1. create table
    with open('src/data/mock_data/queries/create_stores.sql', 'r') as file:
        query = ''.join(file.readlines())
    SERVICE.db.execute(query)

    # 2. fill the table with data
    df = pd.read_csv('src/data/mock_data/mock_data/store_mock.csv')
    SERVICE.db.write(df, Fields.STORE_TABLE, if_exists='replace', index=False)


def seed_transactions():

    SERVICE.log.info('Create SQL transactions table')

    # read saved data
    products = SERVICE.db.read("""SELECT * FROM products""")

    stores = SERVICE.db.read("""SELECT * FROM stores""")

    # read config to generate data
    with open(
        "src/data/mock_data/mock_data/transactions_mock_config.yaml", "r"
    ) as stream:
        config = Box(yaml.load(stream, yaml.SafeLoader))

    # Sales for each product will be generated using a poisson distribution
    # The parameter of the poisson distribution is given randomly generated
    np.random.seed(42)
    products['poisson_parameter'] = np.random.uniform(
        low=0,
        high=5,
        size=len(products)
    )

    # For each day, product sample from the given distribution
    transactions = []
    products = products.to_dict('records')
    stores = stores.to_dict('records')
    dates = pd.date_range(start=config.start_date, end=config.end_date)

    SERVICE.log.info(f"Creating data for {len(products)} products")
    for product in products:
        SERVICE.log.debug(f"Creating data for product {product['product_name']}")
        for store in stores:
            transactions.append(
                pd.DataFrame({
                    Fields.PRODUCT_ID: product[Fields.PRODUCT_ID],
                    Fields.STORE_ID: store[Fields.STORE_ID],
                    Fields.DATE: dates.copy(),
                    Fields.NB_SOLD_PIECES: np.random.poisson(
                        lam=product["poisson_parameter"], size=len(dates))
                })
            )
    transactions = pd.concat(transactions)

    # Save the table using odo (adapted to large size tables)
    SERVICE.log.info(f"Transactions table contains {len(transactions)} entries")
    SERVICE.log.info("Saving transaction table")

    SERVICE.db.write(transactions, Fields.TRANSACTION_TABLE, if_exists='replace', index=False)


def seed_tables():
    """
    Main method to fill DataBase with mock_data
    """

    # 1. seed product table
    try:
        _ = SERVICE.db.read(sql="SELECT * FROM products LIMIT 1;")
    except Exception as _:
        SERVICE.log.info(f"Product table is not seeded, creating mock data...")
        seed_product_table()
        SERVICE.log.info(f"Product table seeded successfully !")

    # 2. seed store table
    try:
        _ = SERVICE.db.read(sql="SELECT * FROM stores LIMIT 1;")
    except Exception as _:
        SERVICE.log.info(f"Store table is not seeded, creating mock data...")
        seed_store_table()
        SERVICE.log.info(f"Store table seeded successfully !")

    # 3. seed transactions
    try:
        _ = SERVICE.db.read(sql="SELECT * FROM transactions LIMIT 1;")
    except Exception as _:
        SERVICE.log.info(f"Transaction table is not seeded, creating mock data...")
        seed_transactions()
        SERVICE.log.info(f"Transaction table seeded successfully !")
