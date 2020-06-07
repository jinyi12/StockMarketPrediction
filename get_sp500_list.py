#%%

import requests
import bs4 as bs
import pickle
import time
import datetime as dt
import pandas_datareader.data as web
import yfinance as yf
import numpy as np
import os

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})

    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    return tickers 


def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
        tickers = [ticker.replace('.', '-',) for ticker in tickers]
        tickers = [ticker.rstrip() for ticker in tickers]
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
            tickers = [ticker.replace('.', '-') for ticker in tickers]
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2019, 1, 1)
    end = dt.datetime.now
    
    ticker_three = ['MSFT', 'JPM', 'JNJ']
    for ticker in ticker_three:
    # for ticker in tickers:
        # save progress just in case connection breaks
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = yf.download(ticker, period='2y')
            print(df.head())
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))
        
        time.sleep(0.5)

if __name__ == "__main__":
    get_data_from_yahoo(reload_sp500=True)
