
import json
import datetime
import numpy as np
import pandas as pd



def getjson_intraday(tickerstring='AAPL', fromdate = '2017-07-01', todate = '2017-08-17',days = 1):
    try:
##        todatestring = str(datetime.datetime.now().date())
##        fromdatestring = todatestring[:-2] + '01'
##        tickerstring = request.args.get('tickerstring', default = 'MSFT-AAPL', type = str)
##        fromdatestring = request.args.get('fromdate', default = fromdatestring, type = str)
##        todatestring = request.args.get('todate', default = todatestring, type = str)
##        days = request.args.get('days', default = 1, type = int)
            
        import pullstackedreturns as psp
        #symbols = ['MSFT','AMZN','GOOG','MS']
        symbols = tickerstring.split('-')
        symbol = symbols[0]
        print symbol
##        fromdate,todate = fromdatestring,todatestring
        import pullintradayprices as pid
        df = pid.intradaystockprices(ticker=symbol,period=60, days=days)
        df.index = df.index.map(str)
        list_of_dicts = df.T.to_dict()
        #ret = jsonify({'intraday': list_of_dicts})
        ret = json.dumps(list_of_dicts)
        #print ret
    except Exception as inst:
        ret = 'Main.py My error was caught: ' + str(inst)
    return ret

def chartintraday():
    json_data = getjson_intraday()
    df = pd.read_json(json_data, orient='list').T
    #print df
    labels = list(df.index) # ["January","February","March","April","May","June","July","August"]
    values = df['Close'].tolist() #[10,9,8,7,6,4,7,8]
    return values

if __name__ == '__main__':
    print chartintraday()
    #app.run()

