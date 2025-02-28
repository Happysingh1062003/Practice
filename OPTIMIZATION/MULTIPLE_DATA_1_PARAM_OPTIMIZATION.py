import vectorbt as vbt
import pandas as pd
import numpy as np
from STRATEGY_1_PARAM import entry_signals , exit_signals

def backtest_and_analyze(data,symbol_name, entry_signals_func, exit_signals_func, parameter,param_name, freq, fees):
    # Initialize storage for metrics
    metrics = {
        'SYMBOL' :[],
        f'{param_name}_Window': [],
        'Returns': [],
        'Sharpe_Ratio': [],
        'Profit_Factor': [],
        'Win_Rate' : [],
        'Number_of_Trade':[],
        'Max_Drawdown': [],
        'Mean_DrawDown': [],
        'Recovery_Factor': [],
        'R_Squared': [],
        'Event_Over_Fitting': []
    }

    def calculate_profit_factor(trade_records):
        profit = trade_records[trade_records["PnL"] > 0]["PnL"]
        loss = trade_records[trade_records["PnL"] < 0]["PnL"]
        sum_profit = abs(profit.sum())
        sum_loss = abs(loss.sum())
        return sum_profit / sum_loss if sum_loss > 0 else float('inf')

    def recovery_factor(total_net_profit, max_drawdown):
        return total_net_profit / max_drawdown if max_drawdown != 0 else float('inf')

    def mean_drawdown(all_drawdowns):
        return all_drawdowns.sum() / len(all_drawdowns) * 100

    def R_squared(x, y):
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        numerator = sum((x - x_mean) * (y - y_mean))
        denominator = sum((x - x_mean) ** 2)
        if denominator != 0 and sum((y - y_mean) ** 2) != 0:
            m = numerator / denominator
            b = y_mean - m * x_mean
            y_pred = m * x + b
            result = 1 - (sum((y - y_pred) ** 2) / sum((y - y_mean) ** 2))
        else:
            result = float('inf')
        return result

    def overfitting_score_2_percent(trade_records):
        data = trade_records["PnL"]
        sorted_series = data.sort_values(ascending=False).reset_index(drop=True)
        top = round(len(sorted_series) / 50)
        upper = sorted_series.head(top).mean()
        lower = sorted_series.mean()
        return upper / lower

    for param_1 in parameter: #here
        # Generate entry and exit signals
        entry_signals = entry_signals_func(data, param_1) 
        exit_signals = exit_signals_func(data, param_1) 

        # Run backtest
        strategy = vbt.Portfolio.from_signals(data, entry_signals, exit_signals, freq=freq, fees=fees, size=1)

        # Metrics calculation
        trade_records = strategy.trades.records_readable
        total_return = strategy.total_return()
        all_drawdowns = strategy.drawdown()
        total_net_profit = abs(strategy.total_profit())
        sharpe_ratio = strategy.sharpe_ratio()
        max_drawdown = abs(strategy.max_drawdown() * 100)
        pnl = strategy.trades.records_readable["PnL"]
        win_rate = (pnl[pnl > 0].count() / len(pnl)) * 100 if len(pnl) > 0 else 0

        y = strategy.value().to_numpy()
        x = np.arange(0, len(y))
        r_square = R_squared(x, y)

        overfit_score = overfitting_score_2_percent(trade_records)
        recover_fact = recovery_factor(total_net_profit, max_drawdown)
        avg_draw = mean_drawdown(all_drawdowns)
        profit_factor = calculate_profit_factor(trade_records)

        # Store metrics
        metrics['SYMBOL'].append(symbol_name)
        metrics[f'{param_name}_Window'].append(param_1)  
        metrics['Returns'].append(total_return)
        metrics['Sharpe_Ratio'].append(sharpe_ratio)
        metrics['Profit_Factor'].append(profit_factor)
        metrics['Win_Rate'].append(win_rate)
        metrics['Number_of_Trade'].append(len(pnl))
        metrics['Max_Drawdown'].append(max_drawdown)
        metrics['Mean_DrawDown'].append(avg_draw)
        metrics['Recovery_Factor'].append(recover_fact)
        metrics['R_Squared'].append(r_square)
        metrics['Event_Over_Fitting'].append(overfit_score)

    # Convert metrics to DataFrame
    result_df = pd.DataFrame(metrics)
    result_df['Parameter'] = f'{param_name}_' + result_df[f'{param_name}_Window'].astype(str) 
    return result_df



if __name__ == "__main__":
    all_results = pd.DataFrame()

    # DATA DIVIDING FOR WALK-FORWARD OPTIMIZATION

    print("Available TimeFrame is 1min , 3min , 5min , 15min , 30min , 1h , 2h , 4h , 6h , 8h and 12h ")
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

    btcusdt=pd.read_csv("../CRYPTO DATA/BTCUSDT.csv")
    btcusdt['Time'] = pd.to_datetime(btcusdt['Time'])
    btcusdt.set_index('Time', inplace=True)
    btcusdt = btcusdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    data=btcusdt['Close']


    def stages_walkforward(Number_of_Stage , data):
        length=len(data)
        if Number_of_Stage == 2 :
            window_len=round(length*0.8)
            set_len=round(length*0.2)
            return window_len , set_len
        if Number_of_Stage == 4 :
            window_len=round(length*0.6)
            set_len=round(window_len*0.22)
            return window_len , set_len
        if Number_of_Stage == 6 :
            window_len=round(length*0.5)
            set_len=round(window_len*0.2)
            return window_len , set_len
        if Number_of_Stage == 8 :
            window_len=round(length*0.5)
            set_len=round(window_len*0.14)
            return window_len , set_len
        if Number_of_Stage == 10 :
            window_len=round(length*0.4)
            set_len=round(window_len*0.165)
            return window_len , set_len
        if Number_of_Stage == 12 :
            window_len=round(length*0.4)
            set_len=round(window_len*0.135)
            return window_len , set_len
        

    #TAKING INPUT FOR THE NUMBER OF STAGE IN WHICH DATA DIVIDED FOR WALKFORWARD ANALYSIS
    print("\nNumber of Stage is How many Stages Data you need to divide : ")
    print("You can divide data in 2 , 4 , 8 , 10 and 12")
    Number_of_Stage=int(input("\nENTER THE NUMBER OF STAGES >>> "))    # we can divide the stages into 2 , 4 , 6 , 8 , 10 , 12
    window_len , set_len=stages_walkforward(Number_of_Stage , data)


    # DATA CENETER

    #BTC
    btcusdt=pd.read_csv("../CRYPTO DATA/BTCUSDT.csv")
    btcusdt['Time'] = pd.to_datetime(btcusdt['Time'])
    btcusdt.set_index('Time', inplace=True)
    btcusdt = btcusdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    (btc_in_sample,btc_in_sample_date),(btc_out_sample,btc_out_sample_dates) = btcusdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                              set_lens=(set_len,),left_to_right=False)


    #ETH
    ethusdt=pd.read_csv("../CRYPTO DATA/ETHUSDT.csv")
    ethusdt['Time'] = pd.to_datetime(ethusdt['Time'])
    ethusdt.set_index('Time', inplace=True)
    ethusdt = ethusdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    (eth_in_sample,eth_in_sample_date),(eth_out_sample,eth_out_sample_dates) = ethusdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                              set_lens=(set_len,),left_to_right=False)

    #DOGE
    dogeusdt=pd.read_csv("../CRYPTO DATA/DOGEUSDT.csv")
    dogeusdt['Time'] = pd.to_datetime(dogeusdt['Time'])
    dogeusdt.set_index('Time', inplace=True)
    dogeusdt = dogeusdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    (doge_in_sample,doge_in_sample_date),(doge_out_sample,doge_out_sample_dates) = dogeusdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                              set_lens=(set_len,),left_to_right=False)

    #TRX
    trxusdt=pd.read_csv("../CRYPTO DATA/TRXUSDT.csv")
    trxusdt['Time'] = pd.to_datetime(trxusdt['Time'])
    trxusdt.set_index('Time', inplace=True)
    trxusdt = trxusdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    (trx_in_sample,trx_in_sample_date),(trx_out_sample,trx_out_sample_dates) = trxusdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                              set_lens=(set_len,),left_to_right=False)



    #PEPE
    pepeusdt=pd.read_csv("../CRYPTO DATA/PEPEUSDT.csv")
    pepeusdt['Time'] = pd.to_datetime(pepeusdt['Time'])
    pepeusdt.set_index('Time', inplace=True)
    pepeusdt = pepeusdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    (pepe_in_sample,pepe_in_sample_date),(pepe_out_sample,pepe_out_sample_dates) = pepeusdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                              set_lens=(set_len,),left_to_right=False)


    #HBAR
    hbarusdt=pd.read_csv("../CRYPTO DATA/HBARUSDT.csv")
    hbarusdt['Time'] = pd.to_datetime(hbarusdt['Time'])
    hbarusdt.set_index('Time', inplace=True)
    hbarusdt = hbarusdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    (hbar_in_sample,hbar_in_sample_date),(hbar_out_sample,hbar_out_sample_dates) = hbarusdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                              set_lens=(set_len,),left_to_right=False)


    #LTC
    ltcusdt=pd.read_csv("../CRYPTO DATA/LTCUSDT.csv")
    ltcusdt['Time'] = pd.to_datetime(ltcusdt['Time'])
    ltcusdt.set_index('Time', inplace=True)
    ltcusdt = ltcusdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    (ltc_in_sample,ltc_in_sample_date),(ltc_out_sample,ltc_out_sample_dates) = ltcusdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                              set_lens=(set_len,),left_to_right=False)


    #XLM
    xlmusdt=pd.read_csv("../CRYPTO DATA/XLMUSDT.csv")
    xlmusdt['Time'] = pd.to_datetime(xlmusdt['Time'])
    xlmusdt.set_index('Time', inplace=True)
    xlmusdt = xlmusdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    (xlm_in_sample,xlm_in_sample_date),(xlm_out_sample,xlm_out_sample_dates) = xlmusdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                              set_lens=(set_len,),left_to_right=False)


    #SUI
    suiusdt=pd.read_csv("../CRYPTO DATA/SUIUSDT.csv")
    suiusdt['Time'] = pd.to_datetime(suiusdt['Time'])
    suiusdt.set_index('Time', inplace=True)
    suiusdt = suiusdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    (sui_in_sample,sui_in_sample_date),(sui_out_sample,sui_out_sample_dates) = suiusdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                              set_lens=(set_len,),left_to_right=False)


    #DOT
    dotusdt=pd.read_csv("../CRYPTO DATA/DOTUSDT.csv")
    dotusdt['Time'] = pd.to_datetime(dotusdt['Time'])
    dotusdt.set_index('Time', inplace=True)
    dotusdt = dotusdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    (dot_in_sample,dot_in_sample_date),(dot_out_sample,dot_out_sample_dates) = dotusdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                              set_lens=(set_len,),left_to_right=False)


    #ALGO
    algousdt=pd.read_csv("../CRYPTO DATA/ALGOUSDT.csv")
    algousdt['Time'] = pd.to_datetime(algousdt['Time'])
    algousdt.set_index('Time', inplace=True)
    algousdt = algousdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    (algo_in_sample,algo_in_sample_date),(algo_out_sample,algo_out_sample_dates) = algousdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                              set_lens=(set_len,),left_to_right=False)


    #ATOM
    atomusdt=pd.read_csv("../CRYPTO DATA/ATOMUSDT.csv")
    atomusdt['Time'] = pd.to_datetime(atomusdt['Time'])
    atomusdt.set_index('Time', inplace=True)
    atomusdt = atomusdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    (atom_in_sample,atom_in_sample_date),(atom_out_sample,atom_out_sample_dates) = atomusdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                              set_lens=(set_len,),left_to_right=False)



    #LUNC
    luncusdt=pd.read_csv("../CRYPTO DATA/LUNCUSDT.csv")
    luncusdt['Time'] = pd.to_datetime(luncusdt['Time'])
    luncusdt.set_index('Time', inplace=True)
    luncusdt = luncusdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    (lunc_in_sample,lunc_in_sample_date),(lunc_out_sample,lunc_out_sample_dates) = luncusdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                              set_lens=(set_len,),left_to_right=False)


    #OM
    omusdt=pd.read_csv("../CRYPTO DATA/OMUSDT.csv")
    omusdt['Time'] = pd.to_datetime(omusdt['Time'])
    omusdt.set_index('Time', inplace=True)
    omusdt = omusdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    (om_in_sample,om_in_sample_date),(om_out_sample,om_out_sample_dates) = omusdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                              set_lens=(set_len,),left_to_right=False)


    #APT
    aptusdt=pd.read_csv("../CRYPTO DATA/APTUSDT.csv")
    aptusdt['Time'] = pd.to_datetime(aptusdt['Time'])
    aptusdt.set_index('Time', inplace=True)
    aptusdt = aptusdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    (apt_in_sample,apt_in_sample_date),(apt_out_sample,apt_out_sample_dates) = aptusdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                              set_lens=(set_len,),left_to_right=False)


    #NEAR
    nearusdt=pd.read_csv("../CRYPTO DATA/NEARUSDT.csv")
    nearusdt['Time'] = pd.to_datetime(nearusdt['Time'])
    nearusdt.set_index('Time', inplace=True)
    nearusdt = nearusdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    (near_in_sample,near_in_sample_date),(near_out_sample,near_out_sample_dates) = nearusdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                              set_lens=(set_len,),left_to_right=False)


    #ZEN
    zenusdt=pd.read_csv("../CRYPTO DATA/ZENUSDT.csv")
    zenusdt['Time'] = pd.to_datetime(zenusdt['Time'])
    zenusdt.set_index('Time', inplace=True)
    zenusdt = zenusdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    (zen_in_sample,zen_in_sample_date),(zen_out_sample,zen_out_sample_dates) = zenusdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                              set_lens=(set_len,),left_to_right=False)


    #BNB
    bnbusdt=pd.read_csv("../CRYPTO DATA/BNBUSDT.csv")
    bnbusdt['Time'] = pd.to_datetime(bnbusdt['Time'])
    bnbusdt.set_index('Time', inplace=True)
    bnbusdt = bnbusdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    (bnb_in_sample,bnb_in_sample_date),(bnb_out_sample,bnb_out_sample_dates) = bnbusdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                              set_lens=(set_len,),left_to_right=False)


    #SOL
    solusdt=pd.read_csv("../CRYPTO DATA/SOLUSDT.csv")
    solusdt['Time'] = pd.to_datetime(solusdt['Time'])
    solusdt.set_index('Time', inplace=True)
    solusdt = solusdt.resample(timeframe,offset=ofset).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',        
        'Close': 'last',
        'Volume': 'sum'   
    })
    (sol_in_sample,sol_in_sample_date),(sol_out_sample,sol_out_sample_dates) = solusdt["Close"].vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                              set_lens=(set_len,),left_to_right=False)
    
    #TAKING INPUT  FOR IN WHICH STAGE OPTIMIZATION NEED TO APPLY
    print("\nOn which stage optimization you want perform ")
    stage = int(input("\nIN WHICH STAGE OPTIMIZATION YOU WANT TO PERFORM >>> "))

    in_sample_symbol = [
    btc_in_sample[stage], eth_in_sample[stage], doge_in_sample[stage], trx_in_sample[stage], pepe_in_sample[stage], hbar_in_sample[stage],
    ltc_in_sample[stage], xlm_in_sample[stage], sui_in_sample[stage], dot_in_sample[stage], algo_in_sample[stage], atom_in_sample[stage],
    lunc_in_sample[stage], om_in_sample[stage], apt_in_sample[stage], near_in_sample[stage], zen_in_sample[stage], bnb_in_sample[stage],
    sol_in_sample[stage],
    ]

    symbol = [
        btcusdt["Close"], ethusdt["Close"], dogeusdt["Close"], trxusdt["Close"], pepeusdt["Close"], 
        hbarusdt["Close"], ltcusdt["Close"], xlmusdt["Close"], suiusdt["Close"], dotusdt["Close"], 
        algousdt["Close"], atomusdt["Close"], luncusdt["Close"], omusdt["Close"], aptusdt["Close"], 
        nearusdt["Close"], zenusdt["Close"], bnbusdt["Close"], solusdt["Close"]
    ]


    symbol_name = [
    'BTCUSDT', 'ETHUSDT', 'DOGEUSDT', 'TRXUSDT', 'PEPEUSDT',
    'HBARUSDT', 'LTCUSDT', 'XLMUSDT', 'SUIUSDT', 'DOTUSDT',
    'ALGOUSDT', 'ATOMUSDT', 'LUNCUSDT', 'OMUSDT', 'APTUSDT',
    'NEARUSDT', 'ZENUSDT', 'BNBUSDT', 'SOLUSDT'
    ]




    '''============================================================================================================================================================'''

    window = np.arange(10,200)

    #ENGINE 
    for data , name in zip(in_sample_symbol,symbol_name): #CHANGE THE IN_SAMPLE_SYMBOL TO SYMBOL IF REQUIRED
        results = backtest_and_analyze(
        data=data,
        symbol_name=name,
        entry_signals_func=entry_signals,
        exit_signals_func=exit_signals,
        parameter=window,
        param_name='window', #Change the Name of Parameter
        freq=timeframe,
        fees=0.001
        )
        all_results = pd.concat([all_results, results], ignore_index=True)

    '''=================================================================================================================================================================='''

all_results.to_csv('1_param.csv', index=False)
