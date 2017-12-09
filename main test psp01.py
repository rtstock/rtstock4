#!flask/bin/python
from flask import Flask, jsonify
import pullstackedprices as psp
app = Flask(__name__)

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    symbols = ['MSFT','AMZN','GOOG','CRM']
    fromdate,todate = '2017-09-01','2017-09-30'
    df_prices = psp.stockpricesstacked(symbols,fromdate,todate)
    list_of_dicts = df_prices.T.to_dict().values()

    return jsonify(list_of_dicts)

if __name__ == '__main__':
    app.run(debug=True)
