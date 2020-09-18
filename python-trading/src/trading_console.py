import pandas as pd
import logging
import portfolio as prtf

# lazy import of the configuration
from config.config import stocks, init_balance

# set up logging
# N.B. writing to a trading log, not the console
# Notes: format = Time YYYY-MM-DD HH-MM-SS :: module :: loglevel :: message
logging.basicConfig(level=logging.DEBUG,
                    filename='trading.log', filemode='w',
                    format='%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s')
logger = logging.getLogger()

# establish a stream logger as well
formatter = logging.Formatter('%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
ch.setFormatter(formatter)
logger.addHandler(ch)


def run():
    dfs = []
    for ticker in stocks:
        # read in the stocks to a DF, add to list
        file = f"C:/Repos/python-trading/data/daily_{ticker}.csv"

        df = pd.read_csv(file)
        df['name'] = ticker
        dfs.append(df)

    # merge into a single dataframe
    df = pd.concat(dfs)
    df.sort_values(by='timestamp', inplace=True)
    df.set_index('timestamp', inplace=True)

    # initialize the portfolio
    p = prtf.Portfolio(name="My Portfolio", balance=init_balance)
    print("Press [X] at any stage to exit trading console.")

    # loop until all trading decisions are finalized
    for idx, row in df.iterrows():
        # create asset object for this entry
        this_asset = prtf.Asset(name=row['name'], price=row['close'])

        logger.info(f"Price for {this_asset.name}: {this_asset.price}")

        # do the user interaction
        print(f"Price for {this_asset.name}: {this_asset.price}")
        action = str.upper(input("[B]uy, [S]ell, or [Pass]? ")).strip('[]')

        if action not in ['B', 'P', 'S', 'X']:
            logger.error("Unknown action, exiting trading console.")
            raise RuntimeError("Unknown action, exiting trading console. ", action)
        elif action == 'X':
            logger.info("Exiting console.")
            return
        else:
            logger.info(f"Choice made to {action} on {this_asset.name}")

            # attempt buy/sell
            if action == 'B':
                logger.info(f"Buy order placed: ({this_asset.name} x {1})")
                if this_asset.name == "AAPL":
                    logger.critical(f"You made a bad decision to buy AAPL stock!")

                # place order, and catch exception if insufficient balance
                try:
                    p.placeOrder(prtf.Order(asset=this_asset, direction=prtf.Direction.BUY, qty=1))
                except prtf.InsufficientFundsException:
                    logger.warning("Insufficient funds to purchase stock.")

                    # ask if additional balance is to be invested
                    add_balance = str.upper(input("Insufficient funds. Add balance (Y/N)?"))
                    if add_balance == 'Y':
                        topup = float(input("How much balance to add?"))
                        p.invest(topup)
                        logger.info(f"Additional funds invested to portfolio: {topup}.")

                        try:
                            p.placeOrder(prtf.Order(asset=this_asset, direction=prtf.Direction.BUY, qty=1))
                        except prtf.InsufficientFundsException:
                            logger.warning("Still insufficient funds to purchase stock. Abandoning this order.")

            elif action == 'S':
                logger.info(f"Sell order placed: ({this_asset.name} x {1})")

                # try to place the order
                try:
                    p.placeOrder(prtf.Order(asset=this_asset, direction=prtf.Direction.SELL, qty=1))
                except prtf.AssetNotPresentException:
                    logger.warning("Do not have sufficient stock of this asset. Order cancelled.")


if __name__ == "__main__":
    run()
