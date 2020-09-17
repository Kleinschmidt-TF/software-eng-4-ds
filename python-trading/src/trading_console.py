import pandas as pd
import logging
import portfolio as prtf

# TODO: move to config
stocks = ["IBM", "AAPL", "AMZN", "GOOG", "MSFT"]
init_balance = 1000

# set up logging
# N.B. writing to a trading log, not the console
logging.basicConfig(level=logging.DEBUG,
                    filename='trading.log',
                    format='%(asctime)s :: %(levelname)s :: %(message)s')


def run():
    # TODO: convert to multi-stock option
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
            raise RuntimeError("Unknown action: ", action)
        elif action == 'X':
            return
        else:
            logging.info(f"Choice is to {action} on {this_asset.name}")

            # attempt buy/sell
            if action == 'B':
                # TODO: implement the exception so you can ask user to add funds
                p.placeOrder(prtf.Order(asset=this_asset, direction=prtf.Direction.BUY, qty=1))

                logging.info(f"Buy order placed: ({this_asset.name} x {1})")

                if this_asset.name == "AAPL":
                    logging.info(f"You made a bad decision to buy AAPL stock!")

            elif action == 'S':
                p.placeOrder(prtf.Order(asset=this_asset, direction=prtf.Direction.SELL, qty=1))
                logging.info(f"Sell order placed: ({this_asset.name} x {1})")


if __name__ == "__main__":
    run()
