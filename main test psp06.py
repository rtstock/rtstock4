from flask import Flask, jsonify, request
import datetime
#import requests

app = Flask(__name__)

@app.route('/prices')
def prices():
    try:
        todatestring = str(datetime.datetime.now().date())
        fromdatestring = todatestring[:-2] + '01'
        tickerstring = request.args.get('tickerstring', default = 'MSFT-AAPL', type = str)
        fromdatestring = request.args.get('fromdate', default = fromdatestring, type = str)
        todatestring = request.args.get('todate', default = todatestring, type = str)
    
        
        import pullstackedprices as psp
        #symbols = ['MSFT','AMZN','GOOG','MS']
        symbols = tickerstring.split('-')
        fromdate,todate = fromdatestring,todatestring
        df = psp.stockpricesstacked(symbols,fromdate,todate)
        df.index = df.index.map(str)
        #df_end = df[:-1]
        list_of_dicts = df.T.to_dict()
        ret = jsonify({'prices': list_of_dicts})
    except Exception as inst:
        ret = 'Main.py My error was caught: ' + str(inst)
    return ret

@app.route('/returns')
def returns():
    try:
        todatestring = str(datetime.datetime.now().date())
        fromdatestring = todatestring[:-2] + '01'
        tickerstring = request.args.get('tickerstring', default = 'MSFT-AAPL', type = str)
        fromdatestring = request.args.get('fromdate', default = fromdatestring, type = str)
        todatestring = request.args.get('todate', default = todatestring, type = str)
    
        
        import pullstackedreturns as psp
        #symbols = ['MSFT','AMZN','GOOG','MS']
        symbols = tickerstring.split('-')
        fromdate,todate = fromdatestring,todatestring
        df = psp.stockreturnsstacked(symbols,fromdate,todate)
        df.index = df.index.map(str)
        list_of_dicts = df.T.to_dict()
        ret = jsonify({'returns': list_of_dicts})
    except Exception as inst:
        ret = 'Main.py My error was caught: ' + str(inst)
    return ret

if __name__ == '__main__':
    app.run()
