#import sys
#import pandas as pd
import numpy as np
#import config
#import os
#import mytools

def stockhistory(symbols,fromdate,todate):
    from pandas_datareader import data, wb

    try:
        hist = data.DataReader(symbols,  "yahoo", fromdate, todate)
        print hist
        return hist
    except Exception as e: 
        print 'there was an error:', e
        return None
    
def test():
    return ' test success real'

def stockpricesstacked(symbols,fromdate,todate,pricechangeortotal='pricechange'):
    df_good,df_missing = stockhistoryasdataframe(symbols,fromdate,todate)
    if not pricechangeortotal=='pricechange':
        df_final = df_good.pivot(index='Date', columns='Ticker', values='Adj Close')
    else:
        df_final = df_good.pivot(index='Date', columns='Ticker', values='Close')
    return df_final

def stockhistoryasdataframe(symbols,fromdate,todate):
    #import numpy as np
    #import pandas as pd
    chunks = [symbols[x:x+100] for x in xrange(0, len(symbols), 100)]
    #chunks = [symbols[x:x+5] for x in xrange(0, len(symbols), 5)]
    print 'pulling prices for chunk', 0, chunks[0]
    df_good,df_missing = stockhistoryasdataframeindividual(chunks[0],fromdate,todate)
    df_good.reindex()

    on = False
    i = 0
    for c in chunks:
        i +=1
        if on == True:
            print 'pulling prices for chunk',i, 'total of', len(c), 'symbol'
            h_good,h_missing = stockhistoryasdataframeindividual(c,fromdate,todate)
            #print 'h_good',h_good
            df_good = df_good.append(h_good, ignore_index=True)
            df_missing = df_missing.append(h_missing, ignore_index=True)
        on = True
    print '--- df_good ----'
    print 'length of pricespulled',len(df_good)
    print 'length of pricespulled missing',len(df_missing)
    return df_good,df_missing
    
def stockhistoryasdataframeindividual(symbols,fromdate,todate):
    #import numpy as np
    import pullintradayprices as pid
    import pandas as pd
    p = stockhistory(symbols,fromdate,todate)
    list_of_dicts = []
    list_of_missing = []
    try:
        for d, item in p.swapaxes(0, 1).iteritems():
            for t,x in item.iteritems():
                        if np.isnan(x['Adj Close']) == True:
                            list_of_missing.append({'Date':d, 'Ticker':t,'Adj Close':x['Adj Close'],'Close':x['Close']})
            else:
                list_of_dicts.append({'Date':d, 'Ticker':t,'Adj Close':x['Adj Close'],'Close':x['Close']})
                
        # Append intraday price
        #list_of_dicts = []
        for s in symbols:
            df = pid.intradaystockprices(ticker=s,period=60, days=1)
            d = df.tail(1).index[0]
            myvalue = df.tail(1)['Close'][0]
            list_of_dicts.append({'Date':d, 'Ticker':s,'Adj Close':myvalue,'Close':myvalue})


    except Exception as e:
        print(e)
    df_good = pd.DataFrame(list_of_dicts)
    df_missing = pd.DataFrame(list_of_missing)
    return df_good, df_missing

def stockcurrentasdataframe(symbols,):
    import pullintradayprices as pid
    list_of_dicts = []
    for s in symbols:
        df = pid.intradaystockprices(ticker=s,period=60, days=1)
        d = df.tail(1).index[0]
        myvalue = df.tail(1)['Close'][0]
        list_of_dicts.append({'Date':d, 'Ticker':s,'Adj Close':myvalue,'Close':myvalue})
    print list_of_dicts
    return df

if __name__=='__main__':

    #symbols = ['MAR', 'MON', 'NOV', 'A', 'AAL', 'AAP', 'AAPL', ]
    symbols = ['GOOG', 'BX']
    print symbols
    df = stockpricesstacked(symbols,'2017-07-01','2017-08-05')
    #df = stockcurrentasdataframe(symbols)
    print df
        
