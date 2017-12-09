import flask
from flask import Flask, jsonify, request, render_template, send_from_directory, make_response, send_file
import datetime
import numpy as np
import pandas as pd
import os
import pullstackedprices as psp
import pullstackedreturns as psr
import pullintradayprices as pid
import time
    

#import requests

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = 'C:/Batches/GitStuff/websites/rtstock4/wwwroot/cache'
#app.config['UPLOAD_FOLDER'] = 'D:/home/site/wwwroot/cache'
#APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 
import pytz
localtz = pytz.timezone('America/New_York')

#@app.route('/index',methods=['POST'])
#def root():
#    return app.send_static_file('index.html')

initial_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <title id="Description">Data Binding to CSV data in jqxDataTable</title>
    <meta name="description" content="This sample demonstrates how we can bind jQWidgets DataTable widget to CSV Data by using jQWidgets DataAdapter plugin.">
    <link rel="stylesheet" href="../../jqwidgets/styles/jqx.base.css" type="text/css" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
    <meta name="viewport" content="width=device-width, initial-scale=1 maximum-scale=1 minimum-scale=1" />	
    <script type="text/javascript" src="../../scripts/jquery-1.12.4.min.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxcore.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxdata.js"></script> 
    <script type="text/javascript" src="../../jqwidgets/jqxbuttons.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxscrollbar.js"></script>
    <script type="text/javascript" src="../../jqwidgets/jqxdatatable.js"></script>
    <script type="text/javascript" src="../../scripts/demos.js"></script>
    <script type="text/javascript">
        $(document).ready(function () {
            var url = '../sampledata/nasdaq_vs_sp500.txt';

            var source =
            {
                dataType: "csv",
                dataFields: [
                    { name: 'Date', type: 'date' },
                    { name: 'S&P 500', type: 'float' },
                    { name: 'NASDAQ', type: 'float' }
                ],
                url: url
            };

            var dataAdapter = new $.jqx.dataAdapter(source);

            $("#table").jqxDataTable(
            {
                width: getWidth("dataTable"),
                pageable: true,
                pagerButtonsCount: 10,
                source: dataAdapter,
                columnsResize: true,
                columns: [
                  { text: 'Date', dataField: 'Date', cellsFormat: 'D', width: 250},
                  { text: 'S&P 500', dataField: 'S&P 500', width: 300, cellsFormat: 'f' },
                  { text: 'NASDAQ', dataField: 'NASDAQ', cellsFormat: 'f' }
                ]
            });
        });
    </script>
</head>
<body class='default'>
    <div id="table"></div>
</body>

</html>

        '''


@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
def getfile():
    try:
        if request.method == 'POST':
            clearcontentsofcache()
            print 'yyyyy'
            date14 = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            feature = request.form['feature']
            tickerstring = request.form['tickerstring']
            
            fromdate = request.form['fromdate']
            todate = request.form['todate']
            tickerstring = "".join(tickerstring.split())
            symbols = tickerstring.split(',')
            feature = feature[:3].lower()
            print 'check',tickerstring,feature
            print symbols
            if feature == 'cov':
                myfilename = covariancematrix(symbols,fromdate,todate)
            elif feature == 'cor':
                myfilename = correlationmatrix(symbols,fromdate,todate)
            elif feature == 'pri':
                myfilename = 'prices_'+date14 + '.csv'
                cachedfilepathname = os.path.join(app.config['UPLOAD_FOLDER'],myfilename)
                df = psp.stockpricesstacked(symbols,fromdate,todate)
                df.to_csv(cachedfilepathname,columns=(list(df.columns.values)))
                time.sleep(1.5)
            elif feature == 'adj':
                myfilename = 'adjclose_'+date14 + '.csv'
                cachedfilepathname = os.path.join(app.config['UPLOAD_FOLDER'],myfilename)
                df = psp.stockpricesstacked(symbols,fromdate,todate,pricechangeortotal='total')
                df.to_csv(cachedfilepathname,columns=(list(df.columns.values)))
                time.sleep(1.5)
            elif feature == 'ret':
                myfilename = 'returns_'+date14 + '.csv'
                cachedfilepathname = os.path.join(app.config['UPLOAD_FOLDER'],myfilename)
                df = psr.stockreturnsstacked(symbols,fromdate,todate)
                df.to_csv(cachedfilepathname,columns=(list(df.columns.values)))
                time.sleep(1.5)
            elif feature == 'int':
                print 'got here xxx'
                myfilename = 'intraday_'+date14 + '.csv'
                cachedfilepathname = os.path.join(app.config['UPLOAD_FOLDER'],myfilename)
                days = request.args.get('days', default = 1, type = int)
                df = pd.DataFrame()
                for symbol in symbols:
                    print 'xx',symbol
                    df_x = pid.intradaystockprices(ticker=symbol,period=60, days=days)
                    if len(df) == 0:
                        df = df_x
                    else:
                        df = df.append(df_x)

                df.to_csv(cachedfilepathname,columns=(list(df.columns.values)))
                time.sleep(1.5)

            ret = 'Successfully executed.'
            return send_file('cache/'+myfilename,
                         mimetype='text/csv',
                         attachment_filename=myfilename,
                         as_attachment=True
                             )
        else:
            #print 'xxx'
            return initial_html
    except Exception as inst:
        ret = 'getfile My error was caught: ' + str(inst)
    return initial_html
@app.route('/prices')
def prices():
    try:
        todatestring = str(datetime.datetime.now().date())
        fromdatestring = todatestring[:-2] + '01'
        tickerstring = request.args.get('tickerstring', default = 'MSFT,AAPL', type = str)
        fromdatestring = request.args.get('fromdate', default = fromdatestring, type = str)
        todatestring = request.args.get('todate', default = todatestring, type = str)
    
        
        import pullstackedprices as psp
        #symbols = ['MSFT','AMZN','GOOG','MS']
        symbols = tickerstring.split(',')
        fromdate,todate = fromdatestring,todatestring
        df = psp.stockpricesstacked(symbols,fromdate,todate)
        df.index = df.index.map(str)
        #df_end = df[:-1]
        list_of_dicts = df.T.to_dict()
        ret = jsonify({'prices': list_of_dicts})            

        #ret = render_template('prices',tables=[df.to_html(classes='prices')]) #, titles = ['na', 'Female surfers', 'Male surfers'])

    except Exception as inst:
        ret = 'Main.py My error was caught: ' + str(inst)
    return ret

@app.route('/adjclose')
def adjclose():
    try:
        todatestring = str(datetime.datetime.now().date())
        fromdatestring = todatestring[:-2] + '01'
        tickerstring = request.args.get('tickerstring', default = 'MSFT,AAPL', type = str)
        fromdatestring = request.args.get('fromdate', default = fromdatestring, type = str)
        todatestring = request.args.get('todate', default = todatestring, type = str)
    
        
        import pullstackedprices as psp
        #symbols = ['MSFT','AMZN','GOOG','MS']
        symbols = tickerstring.split(',')
        fromdate,todate = fromdatestring,todatestring
        df = psp.stockpricesstacked(symbols,fromdate,todate,pricechangeortotal='total')
        df.index = df.index.map(str)
        #df_end = df[:-1]
        list_of_dicts = df.T.to_dict()
        ret = jsonify({'prices': list_of_dicts})            

        #ret = render_template('prices',tables=[df.to_html(classes='prices')]) #, titles = ['na', 'Female surfers', 'Male surfers'])

    except Exception as inst:
        ret = 'Main.py My error was caught: ' + str(inst)
    return ret

@app.route('/returns')
def returns():
    try:
        todatestring = str(datetime.datetime.now().date())
        fromdatestring = todatestring[:-2] + '01'
        tickerstring = request.args.get('tickerstring', default = 'MSFT,AAPL', type = str)
        fromdatestring = request.args.get('fromdate', default = fromdatestring, type = str)
        todatestring = request.args.get('todate', default = todatestring, type = str)
    
        import pullstackedreturns as psp
        #symbols = ['MSFT','AMZN','GOOG','MS']
        symbols = tickerstring.split(',')
        fromdate,todate = fromdatestring,todatestring
        df = psp.stockreturnsstacked(symbols,fromdate,todate,pricechangeortotal='total')
        df.index = df.index.map(str)
        list_of_dicts = df.T.to_dict()
        ret = jsonify({'returns': list_of_dicts})
    except Exception as inst:
        ret = 'Main.py My error was caught: ' + str(inst)
    return ret

@app.route('/cov')
def cov():
    try:
        todatestring = str(datetime.datetime.now().date())
        fromdatestring = todatestring[:-2] + '01'
        tickerstring = request.args.get('tickerstring', default = 'MSFT,AAPL', type = str)
        fromdatestring = request.args.get('fromdate', default = fromdatestring, type = str)
        todatestring = request.args.get('todate', default = todatestring, type = str)
    
        import pullstackedreturns as psp
        #symbols = ['MSFT','AMZN','GOOG','MS']
        symbols = tickerstring.split(',')
        fromdate,todate = fromdatestring,todatestring
        df_returns = psp.stockreturnsstacked(symbols,fromdate,todate,pricechangeortotal='pricechange')

        df_alignedpricechangereturns = df_returns
        df_alignedpricechangereturns = df_alignedpricechangereturns.dropna() #eeee
        
        covmatrix_array = np.cov(df_alignedpricechangereturns,None,0)
        rows = np.array(list(df_alignedpricechangereturns))[: np.newaxis]
        
        df = pd.DataFrame(covmatrix_array, index=rows, columns=list(df_alignedpricechangereturns))
        
        #df.index = df.index.map(str)
        list_of_dicts = df.T.to_dict()
        ret = jsonify({'cov': list_of_dicts})
    except Exception as inst:
        ret = 'Main.py My error was caught: ' + str(inst)
    return ret

@app.route('/cor')
def cor():
    try:
        todatestring = str(datetime.datetime.now().date())
        fromdatestring = todatestring[:-2] + '01'
        tickerstring = request.args.get('tickerstring', default = 'MSFT,AAPL', type = str)
        fromdatestring = request.args.get('fromdate', default = fromdatestring, type = str)
        todatestring = request.args.get('todate', default = todatestring, type = str)
    
        import pullstackedreturns as psp
        #symbols = ['MSFT','AMZN','GOOG','MS']
        symbols = tickerstring.split(',')
        fromdate,todate = fromdatestring,todatestring
        df_returns = psp.stockreturnsstacked(symbols,fromdate,todate,pricechangeortotal='pricechange')


        df_alignedpricechangereturns = df_returns
        df_alignedpricechangereturns = df_alignedpricechangereturns.dropna()
        rows = np.array(list(df_alignedpricechangereturns))[: np.newaxis]
        corrmatrix_array = np.corrcoef(df_alignedpricechangereturns.T.values.tolist())        
        df = pd.DataFrame(corrmatrix_array, index=rows, columns=list(df_alignedpricechangereturns))
        
        #df.index = df.index.map(str)
        list_of_dicts = df.T.to_dict()
        ret = jsonify({'cor': list_of_dicts})
    except Exception as inst:
        ret = 'Main.py My error was caught: ' + str(inst)
    return ret

#df = pid.intradaystockprices(ticker=s,period=60, days=1)
@app.route('/intraday')
def intraday():
    try:
        todatestring = str(datetime.datetime.now().date())
        fromdatestring = todatestring[:-2] + '01'
        tickerstring = request.args.get('tickerstring', default = 'MSFT,AAPL', type = str)
        fromdatestring = request.args.get('fromdate', default = fromdatestring, type = str)
        todatestring = request.args.get('todate', default = todatestring, type = str)
        days = request.args.get('days', default = 1, type = int)
            
        import pullstackedreturns as psp
        
        symbols = tickerstring.split(',')
        
        fromdate,todate = fromdatestring,todatestring
        
        df_final = pd.DataFrame()
        for symbol in symbols:
            df = pid.intradaystockprices(ticker=symbol,period=60, days=days)
            if len(df_final) == 0:
                df_final = df
            else:
                df_final = df_final.append(df,ignore_index = True)
        df_final.index = df_final.index.map(str)
        list_of_dicts = df_final.T.to_dict()
        ret = jsonify({'intraday': list_of_dicts})
    except Exception as inst:
        ret = 'Main.py My error was caught: ' + str(inst)
    return ret

def covariancematrix(symbols,fromdate,todate
             ):
    print 'Running covariancematrix'
    date14 = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    df_alignedpricechangereturns = psr.stockreturnsstacked(symbols,fromdate,todate,pricechangeortotal='pricechange')
    df_alignedpricechangereturns = df_alignedpricechangereturns.dropna() #eeee
    
    
    covmatrix_array = np.cov(df_alignedpricechangereturns,None,0)
    rows = np.array(list(df_alignedpricechangereturns))[: np.newaxis]
    
    df_covariancematrix = pd.DataFrame(covmatrix_array, index=rows, columns=list(df_alignedpricechangereturns))
    #print df_covariancematrix
    #cachedfilepathname = mycachefolder
    myfilename = 'covariance_'+date14 + '.csv'
    cachedfilepathname = os.path.join(app.config['UPLOAD_FOLDER'],myfilename)
    df_covariancematrix.to_csv(cachedfilepathname,columns=(list(df_covariancematrix.columns.values)))
    #import time
    time.sleep(1.5)
    print myfilename
    return myfilename

def correlationmatrix(symbols,fromdate,todate
             ):
    print 'Running correlationmatrix'
    date14 = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    df_alignedpricechangereturns = psr.stockreturnsstacked(symbols,fromdate,todate,pricechangeortotal='pricechange')
    df_alignedpricechangereturns = df_alignedpricechangereturns.dropna() #eeee
    
    
    covmatrix_array = np.cov(df_alignedpricechangereturns,None,0)
    rows = np.array(list(df_alignedpricechangereturns))[: np.newaxis]

    corrmatrix_array = np.corrcoef(df_alignedpricechangereturns.T.values.tolist())    
    df_correlationmatrix = pd.DataFrame(corrmatrix_array, index=rows, columns=list(df_alignedpricechangereturns))
    
    #cachedfilepathname = mycachefolder
    myfilename = 'correlation_'+date14 + '.csv'
    cachedfilepathname = os.path.join(app.config['UPLOAD_FOLDER'],myfilename)
    df_correlationmatrix.to_csv(cachedfilepathname,columns=(list(df_correlationmatrix.columns.values)))
    #import time
    time.sleep(1.5)
    print myfilename
    return myfilename

def clearcontentsofcache():
    import os#, shutil
    folder = app.config['UPLOAD_FOLDER']
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app.run()
