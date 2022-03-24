#  Copyright (c) 2022 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import json
import requests
import ssl
import sys

from datetime import datetime

from Toolbox.Formatting_Tools import change_day


def obtain_equity_prices(asset_type: str, credentials: list, targetDate: str, symbols: dict):

    if asset_type == "Equity":
        # Currently, using Tiingo but may expand to others if requested or just because.
        if credentials[0] == "Tiingo":
            targetDate = datetime.strptime(targetDate, '%Y/%m/%d')
            targetDate = datetime.strftime(targetDate, '%Y-%m-%d')
            symbols = pull_tiingo(targetDate, symbols, credentials[1])
            return symbols
        else:
            pass

    elif asset_type == "Crypto":
        pass

    else:
        # Leaving room in case of new asset category.
        pass


def pull_tiingo(targetDate: str, symbols: dict, token: str):
    # Free Equity API Source
    # For ignoring SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # NYSE isn't open on weekends. So just push the date back to Friday.
    startDate = change_day(targetDate, '%Y-%m-%d')

    updated_container = {}

    for ticker in symbols:
        url = f'https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={startDate}&endDate={targetDate}&token={token}'
        headers = {
            'Content-Type': 'application/json'
        }
        # I fully realize after the fact, that I could have just adjusted the active date by like -5 days and done raw_data[-1]
        try:
            req = requests.get(url, headers=headers)

        except requests.exceptions.RequestException:
            # error catch but no need to change value. Keeping value as zero acts as a note to skip updating balance.
            pass

        else:
            raw_data = json.loads(req.text)
            if len(raw_data) == 0:
                ticker_price = 0
            elif type(raw_data) != list:
                ticker_price = 0
            else:
                ticker_price = raw_data[-1]['close']

                # This is a nice visual for debugging however, it doesn't really help
                # if len(ticker) <= 5:
                #     mod_ticker = ticker + " "*(5-len(ticker))
                #     print(f'[{mod_ticker}] -- ' + str(raw_data[-1]['date'][:10]) + " -- " + str(raw_data[-1]['close']))

            updated_container[ticker] = ticker_price

    return updated_container


def pull_coingecko():
    # Free Crypto API Source
    pass


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
