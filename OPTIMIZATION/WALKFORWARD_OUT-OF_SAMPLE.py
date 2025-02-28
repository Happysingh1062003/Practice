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
data=datausdt['Close']

def stages_walkforward(stage , data):
    length=len(data)
    if stage == 2 :
        window_len=round(length*0.8)
        set_len=round(length*0.2)
        return window_len , set_len
    if stage == 4 :
        window_len=round(length*0.6)
        set_len=round(window_len*0.22)
        return window_len , set_len
    if stage == 6 :
        window_len=round(length*0.5)
        set_len=round(window_len*0.2)
        return window_len , set_len
    if stage == 8 :
        window_len=round(length*0.5)
        set_len=round(window_len*0.14)
        return window_len , set_len
    if stage == 10 :
        window_len=round(length*0.4)
        set_len=round(window_len*0.165)
        return window_len , set_len
    if stage == 12 :
        window_len=round(length*0.4)
        set_len=round(window_len*0.135)
        return window_len , set_len

#TAKING INPUT FOR THE NUMBER OF STAGE IN WHICH DATA DIVIDED FOR WALKFORWARD ANALYSIS
print("\nNumber of Stage is How many Stages Data you need to divide : ")
print("You can divide data in 2 , 4 , 6 , 8 , 10 and 12")
Number_of_Stage=int(input("\nENTER THE NUMBER OF STAGES >>> "))
window_len , set_len=stages_walkforward(Number_of_Stage , data)

(data_in_sample,data_in_sample_date),(data_out_sample,data_out_sample_dates) = datausdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                            set_lens=(set_len,),left_to_right=False)
#TAKING INPUT  FOR IN WHICH STAGE OPTIMIZATION NEED TO APPLY
print("\nOn which stage optimization you want perform ")
stage = int(input("\nIN WHICH STAGE BACKTEST YOU WANT TO PERFORM >>> "))



'''========================================================================================================================================================================'''
#INDICATORS 
SMA=vbt.IndicatorFactory.from_talib("EMA")
fastsma=SMA.run(data_out_sample[stage],80).real.to_numpy()
slowsma=SMA.run(data_out_sample[stage],190).real.to_numpy()

# print(help(BB.run))

#LOGIC
entry=  (fastsma > slowsma)
exits = (fastsma < slowsma)

'''========================================================================================================================================================================'''
      
#BACKTEST ENGINE
strategy = vbt.Portfolio.from_signals(data_out_sample[stage], entry, exits,freq=timeframe,fees=0.001,size=1,init_cash= 100) #init_cash should be last number of csv file
print(strategy.stats())
equity_curve = strategy.value()

equity_curve.to_csv('WALK_FORWARD_EQUITY_CURVE.csv', mode='a', header=False, index=False)






