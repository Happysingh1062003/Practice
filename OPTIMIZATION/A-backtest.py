import vectorbt as vbt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


print("\nOn which symbol you want to test the IN-SAMPLE PARAMETER")
name = str(input("\nSYMBOL >>> "))

print("\nAvailable TimeFrame is 1min , 3min , 5min , 15min , 30min , 1h , 2h , 4h , 6h , 8h and 12h ")
timeframe = str(input("\nENTER THE TIMEFRAME >>> "))
if timeframe == '1min':
    ofset = None
if timeframe == '3min':
    ofset = None
if timeframe == '5min':
    ofset = None
if timeframe == '15min':
    ofset = None
if timeframe == '30min':
    ofset = None
if timeframe == '1h':
    ofset = "30min"
if timeframe == '2h':
    ofset = '90min'
if timeframe == '4h':
    ofset = '90min'
if timeframe == '6h':
    ofset = '-30min'
if timeframe == '8h':
    ofset = '330min'
if timeframe == '12h':
    ofset = '330min'


datausdt=pd.read_csv(f"../CRYPTO DATA/{name}USDT.csv")
datausdt['Time'] = pd.to_datetime(datausdt['Time'])
datausdt.set_index('Time', inplace=True)
datausdt = datausdt.resample(timeframe,offset=ofset).agg({
    'Open': 'first',
    'High': 'max',
    'Low': 'min',        
    'Close': 'last',
    'Volume': 'sum'   
})
datausdt=datausdt['Close']

'''================================================================================================================================================================='''
#INDICATOR AND PAREAMETER
ALMA = vbt.IndicatorFactory.from_pandas_ta("alma")
alma=ALMA.run(datausdt,100,6,0.55).alma


# print(help(BB.run))

#LOGIC
entry= (datausdt > alma) 
exits = (datausdt < alma)

'''================================================================================================================================================================'''

#BACKTEST ENGINE
strategy = vbt.Portfolio.from_signals(datausdt, entry, exits,freq=timeframe,fees=0.001,size=1,init_cash=10000)
print(strategy.stats())

fig=strategy.plot(subplots=[
    'orders',
    'trade_pnl',
    'cum_returns',
    'drawdowns',
    'trades',
    'value'])

fig.show()


