import datetime as dt
import statsmodels.tsa.stattools as ts
import statsmodels.api as sm
import numpy as np

def initialize(context):
    # Initialize stock universe with the following stocks:

    # Coca-Cola (KO) and Pepsi (PEP)
    # Wal-Mart (WMT) and Target Corporation (TGT)
    # Exxon Mobil (XOM) and Chevron Corporation (CVX)
    # BHP Billiton Limited (BHP) and BHP Billiton plc (BBL)
    
    #1. Identification of security (stocks, bonds, futures etc.)  pairs.  Essentially, first create a short list of related securities (we’ll be using equities via Quantopian).
   
    context.stocks = [[sid(4283), sid(5885)],
                      [sid(8229), sid(21090)],
                      [sid(8347), sid(23112)]]
                      #[sid(863), sid(25165)]]

    # Declare lag value/flag
    context.warmupDays = 60
    context.warmedUp = False

    # Initialize ratio (for the current ratio), historical (historical prices), and current holdings
    lenCon = len(context.stocks)
    context.ratio = [[]] * lenCon
    context.historical = [[[],[]]] * lenCon
    context.currDays = 0
    
    # Used later to test for cointegration
    context.cointegrated = []
    
    # The amount of standard deviations that causes a buy
    context.SDDiff = 1
    
    # Mean the stock was last bought at
    context.limits = [False] * lenCon
    
    context.spread = [[]] * lenCon
    
    context.amountStock = [[0,0]] * lenCon
    
def handle_data(context, data):
    # Check bool flag for 60 day lag
    if context.warmedUp == False:
        for pair in range(len(context.stocks)):
            currPair = context.stocks[pair]
            context.ratio[pair].append(data[currPair[0]].price/data[currPair[1]].price)
            context.historical[pair][0].append(data[currPair[0]].price)
            context.historical[pair][1].append(data[currPair[1]].price)
            context.spread[pair].append(data[currPair[0]].price - data[currPair[1]].price)

        if len(context.ratio[0]) >= 60:
            context.warmedUp = True
            for pair in range(len(context.stocks)):
            #2. Relationship testing.  There are many ways to test of this relationship.  We will be using cointegration.  Two time series are cointegrated if they share the same stochastic drift (the change of average value over time).  There are a couple of video on cointegration, and we’ll go over some examples.
                context.cointegrated.append(test_coint(context.historical[pair]))
            if False in context.cointegrated:
                print("First pair that is not cointegrated:")
                # This could be built out to iterate if we are searching for pairs, but all of the pairs I have chosen cointegrate
                print(context.stocks[np.where([not i for i in context.cointegrated])[0][0]])
    else:
        #3. Building the trade.  Using the historical data we have available, establish baseline values that create rules for buying and selling the securities.  At the core, this is simple.  When the pair is out of line, we buy one and sell the other (other variations exist).  When the pair comes back in line, we exit the trade and capture the profit.
        for pair in range(len(context.stocks)):
            currPair = context.stocks[pair]
    
            currX = currPair[0]
            currY = currPair[1]
            
            currXPrice = data[currX].price
            currYPrice = data[currY].price
            
            spreadMean = np.mean(context.spread[pair])
            spreadSD = np.std(context.spread[pair])
            currSpread = currXPrice - currYPrice
            context.spread[pair].append(currSpread)
            
            currRatio = currXPrice/currYPrice

            #figure out how many stocks
            stocksToOrderX = 1.5 * currRatio
            stocksToOrderY = 1.5 
            
            # amount of stocks owned
            currOwnedX = context.portfolio.positions[currPair[0]]['amount']
            currOwnedY = context.portfolio.positions[currPair[1]]['amount']
       
            # Attempting to resolve initial state
            
            # if not all(i == False for i in context.limits):
            toCheck = [i for i, j in enumerate(context.limits) if j != False]
            if pair in toCheck:
                #pair, spreadMean, 'long'/'short'
                lim = context.limits[pair]
                if lim[2] == 'long':
                    if currSpread <= spreadMean:
                        order(currX, -currOwnedX)
                        order(currY, -currOwnedY)
                        context.limits[pair] = False
                else:
                    if currSpread >= spreadMean:
                        order(currX, -currOwnedX)
                        order(currY, -currOwnedY)
                        context.limits[pair] = False
            
            #  Trade Initialization
            lowerLim = -10000
            # currOwnedX < upperLim and and currOwnedY < upperLim
            if currOwnedX > lowerLim  and currOwnedY > lowerLim:          
                if currSpread > spreadMean + context.SDDiff * spreadSD:
                        order(currX, -stocksToOrderX)
                        order(currY, stocksToOrderY)
                        print("Bought " + str(stocksToOrderY) + " stocks of " + str(currY))
                        print("Shorted " + str(stocksToOrderX) + " stocks of " + str(currX))
                        context.limits[pair] = [pair, spreadMean, 'long']
                elif currSpread < spreadMean - context.SDDiff * spreadSD:
                        order(currX, stocksToOrderX)
                        order(currY, -stocksToOrderY)
                        print("Bought " + str(stocksToOrderX) + " stocks of " + str(currX))
                        print("Shorted " + str(stocksToOrderY) + " stocks of " + str(currY))
                        context.limits[pair] = [pair, spreadMean, 'long']

            # Logging data
            context.historical[pair][0].append(data[currPair[0]].price)
            context.historical[pair][1].append(data[currPair[1]].price)

            
def test_coint(pair):
    result = sm.OLS(pair[1], pair[0]).fit()   #Ordinary Least Squares
    dfResult =  ts.adfuller(result.resid)  #Dickey-Fuller Cointegration test( check wikipedia)
    return dfResult[0] >= dfResult[4]['10%'] #at least 10% cointegrated
