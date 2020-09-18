import pandas as pd
import logging
import portfolio as prtf

# lazy import of the configuration
from config.config import stocks, init_balance

# set up logging
# N.B. writing to a trading log, not the console
# Notes: format = Time YYYY-MM-DD HH-MM-SS :: module :: loglevel :: message
logging.basicConfig(level=logging.DEBUG,
                    filename='trading.log',
                    format='%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s')


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

    # loop until all trading decisions are finalized
    for idx, row in df.iterrows():
        # create asset object for this entry
        this_asset = prtf.Asset(name=row['name'], price=row['close'])

        logging.info(f"Price for {this_asset.name}: {this_asset.price}")

        # do the user interaction
        print(f"Price for {this_asset.name}: {this_asset.price}")
        action = str.upper(input("[B]uy, [S]ell, or [Pass]? ")).strip('[]')

        if action not in ['B', 'P', 'S', 'X']:
            logging.error("Unknown action, exiting trading console.")
            raise RuntimeError("Unknown action, exiting trading console. ", action)
        elif action == 'X':
            logging.error("Exiting console.")
            return
        else:
            logging.info(f"Choice made to {action} on {this_asset.name}")

            # attempt buy/sell
            if action == 'B':
                logging.info(f"Buy order placed: ({this_asset.name} x {1})")
                if this_asset.name == "AAPL":
                    logging.critical(f"You made a bad decision to buy AAPL stock!")

                # place order, and catch exception if insufficient balance
                try:
                    p.placeOrder(prtf.Order(asset=this_asset, direction=prtf.Direction.BUY, qty=1))
                except prtf.InsufficientFundsException:
                    logging.warning("Insufficient funds to purchase stock.")

                    # ask if additional balance is to be invested
                    add_balance = str.upper(input("Insufficient funds. Add balance (Y/N)?"))
                    if add_balance == 'Y':
                        topup = float(input("How much balance to add?"))
                        p.invest(topup)
                        logging.info(f"Additional funds invested to portfolio: {topup}.")

                        try:
                            p.placeOrder(prtf.Order(asset=this_asset, direction=prtf.Direction.BUY, qty=1))
                        except prtf.InsufficientFundsException:
                            logging.warning("Still insufficient funds to purchase stock. Abandoning this order.")

            elif action == 'S':
                logging.info(f"Sell order placed: ({this_asset.name} x {1})")

                # try to place the order
                try:
                    p.placeOrder(prtf.Order(asset=this_asset, direction=prtf.Direction.SELL, qty=1))
                except prtf.AssetNotPresentException:
                    logging.warning("Do not have sufficient stock of this asset. Order cancelled.")


if __name__ == "__main__":
    run()
