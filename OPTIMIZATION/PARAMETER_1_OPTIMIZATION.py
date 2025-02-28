import vectorbt as vbt
import pandas as pd
import numpy as np
from STRATEGY_1_PARAM import entry_signals , exit_signals


def backtest_and_analyze(data, entry_signals_func, exit_signals_func, parameter_1,name_param_1, freq='15min', fees=0.001):
    # Initialize storage for metrics
    metrics = {
        f'{name_param_1}_Window': [],
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

    for param_1 in parameter_1: #here
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
        metrics[f'{name_param_1}_Window'].append(param_1)  
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
    result_df['Parameter'] = f'{name_param_1}_' + result_df[f'{name_param_1}_Window'].astype(str) 
    return result_df


'''====================================================================================================================================='''


# Example usage
if __name__ == "__main__":

    print("On which symbol you want to test the IN-SAMPLE PARAMETER")
    name = str(input("\nSYMBOL >>> "))

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
    print("You can divide data in 2 , 4 , 6 , 8 , 10 and 12")
    Number_of_Stage=int(input("\nENTER THE NUMBER OF STAGES >>> "))    # we can divide the stages into 2 , 4 , 6 , 8 , 10 , 12
    window_len , set_len=stages_walkforward(Number_of_Stage , datausdt)
    
    (datausdt_in_sample,datausdt_in_sample_date),(datausdt_out_sample,datausdt_out_sample_dates) = datausdt.vbt.rolling_split(n=Number_of_Stage,window_len=window_len,
                                                                                            set_lens=(set_len,),left_to_right=False)

    print("\nOn which stage optimization you want perform ")
    stage = int(input("\nIN WHICH STAGE OPTIMIZATION YOU WANT TO PERFORM >>> "))

    '''================================================================================================================================================================================================'''

    fast_window = np.arange(10, 200)

    results = backtest_and_analyze(
        datausdt_in_sample[stage],   #CHNAGE TO DATAUSDT IN YOU WANT TO OPTIMIZEW THE STRATEGY ON WHOLE DATA 
        entry_signals_func=entry_signals,
        exit_signals_func=exit_signals,
        parameter_1=fast_window,
        name_param_1='almawindow',
    )

    '''================================================================================================================================================================================================='''

    print(results)

    top_10_by_returns = results.nlargest(10, 'Returns')

    # Display the top 10 results
    print("Top 10 Results by Returns:")
    print(top_10_by_returns)