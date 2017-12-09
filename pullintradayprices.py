#!/usr/bin/env python 
"""
Retrieve intraday stock data from Google Finance.
"""

import csv
import datetime
import re

import pandas as pd
import requests

def intradaystockprices(ticker, period=60, days=1):
    """
    Retrieve intraday stock data from Google Finance.

    Parameters
    ----------
    ticker : str
        Company ticker symbol.
    period : int
        Interval between stock values in seconds.
    days : int
        Number of days of data to retrieve.

    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing the opening price, high price, low price,
        closing price, and volume. The index contains the times associated with
        the retrieved price values.
    """
    #import pytz
    #localtz = pytz.timezone('America/Los_Angeles')
    uri = 'https://finance.google.com/finance/getprices?q={ticker}&x=&p={days}d&i={period}&f=d,c,o,h,l,v'.format(
                                                                            ticker=ticker,
                                                                            period=str(period),
                                                                            days=str(days)
                                                                            )
    
##    uri = 'http://www.google.com/finance/getprices?i={period}&p={days}d&f=d,o,h,l,c,v&df=cpct&q={ticker}'.format(
##                                                                            ticker=ticker,
##                                                                            period=period,
##                                                                            days=days
##                                                                            )
    
    #uri= 'http://www.google.com/finance/getprices?q=GOOG&x=NASD&i=86400&p=40Y&f=d,c,v,k,o,h,l&df=cpct&auto=0&ei=Ef6XUYDfCqSTiAKEMg'
    #uri= 'http://www.google.com/finance/getprices?q=MSFT&x=&i=86400&p=3d&f=d,c,v,k,o,h,l&df=cpct&auto=0&ei=Ef6XUYDfCqSTiAKEMg'
    #uri = 'https://finance.google.com/finance/getprices?q=BX&x=&p=1d&i=60&f=d,c,o,h,l,v'
    page = requests.get(uri)
    #print uri
    reader = csv.reader(page.content.splitlines())
    
    columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    rows = []
    times = []
    for row in reader:
        #print row
        if re.match('^[a\d]', row[0]):
            if row[0].startswith('a'):
                start = datetime.datetime.fromtimestamp(int(row[0][1:]))
                times.append(start)
            else:
                times.append(start+datetime.timedelta(seconds=period*int(row[0])))
            rows.append(map(float, row[1:]))
    
    if len(rows):
        df_final = pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'),columns=columns)
        #return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'),columns=columns)
    else:
        df_final = pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'))
        #return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'))
    df_final['Ticker']=ticker
    df_final.sort_index(inplace=True)
    return df_final

if __name__=='__main__':
    df = intradaystockprices(ticker='BX',period=60, days=1)
    print df
