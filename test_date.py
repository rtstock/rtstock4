import datetime
nowstring = str(datetime.datetime.now().date())
print nowstring[:-2] + '01'
print nowstring

