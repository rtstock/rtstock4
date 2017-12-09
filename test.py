try:
	import pullstackedprices as psp
	symbols = ['MSFT','AMZN','GOOG']
	fromdate,todate = '2017-09-01','2017-09-30'
	prices = psp.stockpricesstacked(symbols,fromdate,todate)
	ret = str(prices[:-1])
except (RuntimeError, TypeError, NameError):
	ret = 'My error was caught: ' + str(NameError)
print ret
