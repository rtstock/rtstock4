from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def execute():
    #This was up on the server before being pulled via git'
    try:
        
        import pullstackedprices as psp
        symbols = ['MSFT','AMZN','GOOG']
        fromdate,todate = '2017-09-1','2017-09-30'
        df_prices = psp.stockpricesstacked(symbols,fromdate,todate)
        df_prices_end = df_prices[:-1]
        list_of_dicts = df_prices_end.T.to_dict().values()
        ret = jsonify({'prices': list_of_dicts})
    except Exception as inst:
        ret = 'Main.py My error was caught: ' + str(inst)
    return ret

if __name__ == '__main__':
    app.run()
