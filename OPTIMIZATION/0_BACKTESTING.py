import vectorbt as vbt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

metrics = {
    'SYMBOL' :[],
    'Timeframe' : [],
    'Returns': [],
    'Sharpe_Ratio': [],
    'Number_of_Trade':[],
    'Max_Drawdown': [],
}
#'1min','3min','5min',
times=['15min','30min','1h','2h','4h','6h','8h','12h']

for time in times:
    if time == '1min':
        ofset = None
    if time == '3min':
        ofset = None
    if time == '5min':
        ofset = None
    if time == '15min':
        ofset = None
    if time == '30min':
        ofset = None
    if time == '1h':
        ofset = "30min"
    if time == '2h':
        ofset = '90min'
    if time == '4h':
        ofset = '90min'
    if time == '6h':
        ofset = '-30min'
    if time == '8h':
        ofset = '330min'
    if time == '12h':
        ofset = '330min'

    # DATA 

    #BTC
    btcusdt=pd.read_csv("../CRYPTO DATA/BTCUSDT.csv")
    btcusdt['Time'] = pd.to_datetime(btcusdt['Time'])
    btcusdt.set_index('Time', inplace=True)
    btcusdt = btcusdt.resample(time,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })


    #ETH
    ethusdt=pd.read_csv("../CRYPTO DATA/ETHUSDT.csv")
    ethusdt['Time'] = pd.to_datetime(ethusdt['Time'])
    ethusdt.set_index('Time', inplace=True)
    ethusdt = ethusdt.resample(time,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })

    #DOGE
    dogeusdt=pd.read_csv("../CRYPTO DATA/DOGEUSDT.csv")
    dogeusdt['Time'] = pd.to_datetime(dogeusdt['Time'])
    dogeusdt.set_index('Time', inplace=True)
    dogeusdt = dogeusdt.resample(time,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })

    #TRX
    trxusdt=pd.read_csv("../CRYPTO DATA/TRXUSDT.csv")
    trxusdt['Time'] = pd.to_datetime(trxusdt['Time'])
    trxusdt.set_index('Time', inplace=True)
    trxusdt = trxusdt.resample(time,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })

    #PEPE
    pepeusdt=pd.read_csv("../CRYPTO DATA/PEPEUSDT.csv")
    pepeusdt['Time'] = pd.to_datetime(pepeusdt['Time'])
    pepeusdt.set_index('Time', inplace=True)
    pepeusdt = pepeusdt.resample(time,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })

    #HBAR
    hbarusdt=pd.read_csv("../CRYPTO DATA/HBARUSDT.csv")
    hbarusdt['Time'] = pd.to_datetime(hbarusdt['Time'])
    hbarusdt.set_index('Time', inplace=True)
    hbarusdt = hbarusdt.resample(time,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })

    #LTC
    ltcusdt=pd.read_csv("../CRYPTO DATA/LTCUSDT.csv")
    ltcusdt['Time'] = pd.to_datetime(ltcusdt['Time'])
    ltcusdt.set_index('Time', inplace=True)
    ltcusdt = ltcusdt.resample(time,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })

    #XLM
    xlmusdt=pd.read_csv("../CRYPTO DATA/XLMUSDT.csv")
    xlmusdt['Time'] = pd.to_datetime(xlmusdt['Time'])
    xlmusdt.set_index('Time', inplace=True)
    xlmusdt = xlmusdt.resample(time,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })

    #SUI
    suiusdt=pd.read_csv("../CRYPTO DATA/SUIUSDT.csv")
    suiusdt['Time'] = pd.to_datetime(suiusdt['Time'])
    suiusdt.set_index('Time', inplace=True)
    suiusdt = suiusdt.resample(time,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })

    #DOT
    dotusdt=pd.read_csv("../CRYPTO DATA/DOTUSDT.csv")
    dotusdt['Time'] = pd.to_datetime(dotusdt['Time'])
    dotusdt.set_index('Time', inplace=True)
    dotusdt = dotusdt.resample(time,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })

    #ALGO
    algousdt=pd.read_csv("../CRYPTO DATA/ALGOUSDT.csv")
    algousdt['Time'] = pd.to_datetime(algousdt['Time'])
    algousdt.set_index('Time', inplace=True)
    algousdt = algousdt.resample(time,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })

    #ATOM
    atomusdt=pd.read_csv("../CRYPTO DATA/ATOMUSDT.csv")
    atomusdt['Time'] = pd.to_datetime(atomusdt['Time'])
    atomusdt.set_index('Time', inplace=True)
    atomusdt = atomusdt.resample(time,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })


    #LUNC
    luncusdt=pd.read_csv("../CRYPTO DATA/LUNCUSDT.csv")
    luncusdt['Time'] = pd.to_datetime(luncusdt['Time'])
    luncusdt.set_index('Time', inplace=True)
    luncusdt = luncusdt.resample(time,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })

    #OM
    omusdt=pd.read_csv("../CRYPTO DATA/OMUSDT.csv")
    omusdt['Time'] = pd.to_datetime(omusdt['Time'])
    omusdt.set_index('Time', inplace=True)
    omusdt = omusdt.resample(time,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })

    #APT
    aptusdt=pd.read_csv("../CRYPTO DATA/APTUSDT.csv")
    aptusdt['Time'] = pd.to_datetime(aptusdt['Time'])
    aptusdt.set_index('Time', inplace=True)
    aptusdt = aptusdt.resample(time,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })

    #NEAR
    nearusdt=pd.read_csv("../CRYPTO DATA/NEARUSDT.csv")
    nearusdt['Time'] = pd.to_datetime(nearusdt['Time'])
    nearusdt.set_index('Time', inplace=True)
    nearusdt = nearusdt.resample(time,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })

    #ZEN
    zenusdt=pd.read_csv("../CRYPTO DATA/ZENUSDT.csv")
    zenusdt['Time'] = pd.to_datetime(zenusdt['Time'])
    zenusdt.set_index('Time', inplace=True)
    zenusdt = zenusdt.resample(time,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })

    #BNB
    bnbusdt=pd.read_csv("../CRYPTO DATA/BNBUSDT.csv")
    bnbusdt['Time'] = pd.to_datetime(bnbusdt['Time'])
    bnbusdt.set_index('Time', inplace=True)
    bnbusdt = bnbusdt.resample(time,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })

    #SOL
    solusdt=pd.read_csv("../CRYPTO DATA/SOLUSDT.csv")
    solusdt['Time'] = pd.to_datetime(solusdt['Time'])
    solusdt.set_index('Time', inplace=True)
    solusdt = solusdt.resample(time,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })


    # DATA PROCESSING 
    close_data=[btcusdt["Close"],dogeusdt["Close"],ethusdt["Close"],ltcusdt["Close"],luncusdt["Close"],
                hbarusdt["Close"],omusdt["Close"],bnbusdt["Close"],solusdt["Close"],
                zenusdt["Close"],nearusdt["Close"],aptusdt["Close"],atomusdt["Close"],algousdt["Close"],
                suiusdt["Close"],dotusdt["Close"],xlmusdt["Close"],trxusdt["Close"],pepeusdt["Close"]]


    asset_names = [
        "BTCUSDT", "DOGEUSDT", "ETHUSDT", "LTCUSDT", "LUNCUSDT", "HBARUSDT", 
        "OMUSDT", "BNBUSDT", "SOLUSDT", "ZENUSDT", "NEARUSDT", "APTUSDT", "ATOMUSDT","ALGOUSDT",
        "SUIUSDT", "DOTUSDT", "XLMUSDT", "TRXUSDT", "PEPEUSDT"
    ]

    close_data_df = pd.concat(close_data, axis=1)
    close_data_df.columns = asset_names
    data = close_data_df.ffill().bfill()


    for i in data.columns:

        #STRATEGY SECTIION :
        '''============================================================================================================================================================'''
        # INDICATOR INITIALIZATION
        ALMA = vbt.IndicatorFactory.from_pandas_ta("alma")
        slowalma=ALMA.run(data[i],100,6,0.55).alma
        fastalma=ALMA.run(data[i],50,6,0.55).alma
        #slowalma=ALMA.run(btcusdt['Close'],200,6,0.85).alma


        #LOGIC
        entry=(fastalma > slowalma) 
        exits=(fastalma < slowalma)
        '''============================================================================================================================================================='''

        # BACKTEST ENGINE
        strategy = vbt.Portfolio.from_signals(data[i],entry,exits,fees=0.001,freq=time,size=1)
        trade_records = strategy.trades.records_readable
        pnl = strategy.trades.records_readable["PnL"]
        totoal_returns=strategy.total_return()*100
        sharpe_ratio = strategy.sharpe_ratio()
        drawdowns = strategy.drawdowns.max_drawdown()*100
        metrics['SYMBOL'].append(i)
        metrics['Returns'].append(totoal_returns)
        metrics['Sharpe_Ratio'].append(sharpe_ratio)
        metrics['Timeframe'].append(time)
        metrics['Max_Drawdown'].append(drawdowns)
        metrics['Number_of_Trade'].append(len(pnl))



result_df = pd.DataFrame(metrics)
result_df['Parameter'] = result_df['SYMBOL'].astype(str) + '_'+result_df['Timeframe'].astype(str)
result_df.to_csv('0_backtest.csv', index=False)
print(result_df) 