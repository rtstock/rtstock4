from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def execute():
    #This was up on the server before being pulled via git'
    try:
        
        import pullstackedprices as psp
        symbols = ['MSFT','AMZN','GOOG']
        fromdate,todate = '2017-09-01','2017-09-30'
        prices = psp.stockpricesstacked(symbols,fromdate,todate)
        ret = str(prices[:-1])
        
    except Exception as inst:
        ret = 'Main.py My error was caught: ' + str(inst)
    return ret

if __name__ == '__main__':
    app.run()
