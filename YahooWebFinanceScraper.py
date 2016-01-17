#Scrapes stock data from Yahoo Finance
import datetime
import pandas as pd
import csv
import os.path
import statsmodels.tsa.stattools as ts
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas import DataFrame
from pandas.io.data import DataReader
from pyalgotrade.barfeed import yahoofeed
#NYSE TOP 40 Stocks
#Read 2 stocks
f = open('stock.txt', 'r')
symbols_list = [f.readline()[:-1],f.readline()]#['AAPL', 'TSLA']brevity, 'YHOO','MSFT','ALTR','WDC','KLAC', 'BAC', 'KMI' ,'SUNE', 'HPQ', 'FCX', 'GE', 'PBR', 'BABA', 'ITUB', 'XOM', 'C', 'EMC', 'MPLX', 'CNX' ,'NRG', 'S', 'EPD', 'WMT', 'ORCL']
#120MB of test data for classifiers! 
print symbols_list
if os.path.isfile(symbols_list[0]+'-'+symbols_list[1]+'.csv')==False: 
    symbols=[]
    for ticker in symbols_list:
        print ticker
        i,j = 1,1
        for i in range (1,13):
            print i
            for j in range(1,21):
                print j
                r = DataReader(ticker, "yahoo", start=datetime.datetime(2014, i, j))
                # add a symbol column
                r['Symbol'] = ticker 
                symbols.append(r)
                j += 1
    
            i += 1
    # concatenate all the dataframes
    df = pd.concat(symbols)
    # create an organized cell from the new dataframe
    cell= df[['Symbol','Open','High','Low','Adj Close','Volume']]
    
    cell.reset_index().sort(['Symbol', 'Date'], ascending=[1,0]).set_index('Symbol').to_csv(symbols_list[0]+'-'+symbols_list[1]+'.csv', date_format='%d/%m/%Y')
    print "Finished writing"

# Load the CSV
#[0:94332] are stockA

#print df[1:5]
df = pd.DataFrame.from_csv(symbols_list[0]+'-'+symbols_list[1]+'.csv', parse_dates=False)
#df.b.plot(color='g',lw=1.3)
#df.c.plot(color='r',lw=1.3)
df1=df[:94333 ]
df2=df[94333:] 
fig = plt.figure()
fig.suptitle('Adjusted Close Over Time', fontsize=20)
plt.xlabel('xlabel', fontsize=9)
df1.plot('Date','Adj Close')
df2.plot('Date', 'Adj Close')
plt.savefig(symbols_list[0]+'-'+symbols_list[1]+'.png')

#df1['Date','Adj Close'].plot()
#df2['Date','Adj Close'].plot()
#plt.show()