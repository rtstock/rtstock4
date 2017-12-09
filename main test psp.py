#!flask/bin/python
from flask import Flask, jsonify
import pullstackedprices as psp
app = Flask(__name__)

symbols = ['MSFT','AMZN','GOOG']
fromdate,todate = '2017-09-01','2017-09-30'
df_prices = psp.stockpricesstacked(symbols,fromdate,todate)

tasks = df_prices.T.to_dict().values()

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.run(debug=True)
