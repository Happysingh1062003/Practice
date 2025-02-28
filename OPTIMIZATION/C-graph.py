import pandas as pd
import matplotlib.pyplot as plt
import vectorbt as vbt

equity_dict = {}
overfitt={}

solusdt=pd.read_csv("../CRYPTO DATA/SOLUSDT.csv")
solusdt['Time'] = pd.to_datetime(solusdt['Time'])
solusdt.set_index('Time', inplace=True)
solusdt = solusdt.resample('3min').agg({
    'Open': 'first',
    'High': 'max',
    'Low': 'min',        
    'Close': 'last',
    'Volume': 'sum'   
})

'''========================================================================================================================================================================'''

#PARAMETER 
bb_window = [50,20,30,40,10]
rsi_window=[21,20,16,18,22]

for bb,rsi in zip(bb_window,rsi_window):


    '''==============================================================================================================================================='''
    #INDICATORS AND PARAMETER
    BB=vbt.IndicatorFactory.from_talib("BBANDS")
    RSI=vbt.IndicatorFactory.from_talib("RSI")
    upperband=BB.run(solusdt["Close"],bb).upperband.to_numpy()
    lowerband=BB.run(solusdt["Close"],bb).lowerband.to_numpy()
    rsivalue=RSI.run(solusdt["Close"],rsi).real.to_numpy()

    #LOGIC
    entry=(solusdt["Close"]< lowerband) & (rsivalue < 30)
    exits=(solusdt["Close"] > upperband) & (rsivalue > 70)

    '''==============================================================================================================================================='''

                
    #BACKTEST ENGINE
    strategy = vbt.Portfolio.from_signals(solusdt["Close"], entry, exits,freq="3min",fees=0.001,size=1)
    curve_name = f'BB_{bb}_RSI_{rsi}' #CHANGE THE NAME 
    equity_dict[curve_name] = strategy.value()

    trade_records = strategy.trades.records_readable
    overfitt[curve_name]=trade_records["PnL"]


#EQUITY CURVE 
equity = pd.DataFrame(equity_dict)
for column in equity.columns:
    plt.plot(equity[column], label=column)
plt.legend()
plt.grid(True)
plt.show()



#SEPERATE GRAPH FOR EACH EQUITY CURVE 
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.ravel() # Flatten axes array
for idx, column in enumerate(equity.columns):
   axes[idx].plot(equity[column])
   axes[idx].set_title(column)
   axes[idx].grid(True)
plt.tight_layout()
plt.show()



#OVERFITTING GRAPH ALL IN ONE
overfit = pd.DataFrame(overfitt)
sorted_df = overfit.apply(lambda col: col.sort_values(ascending=False).reset_index(drop=True))

plt.figure(figsize=(12, 8))  
for col_name in sorted_df.columns:
    x_values = range(1, len(sorted_df[col_name]) + 1)
    plt.scatter(x_values, sorted_df[col_name], alpha=0.7, label=f'{col_name}')

plt.xlabel("Trade Number (Sorted by Return)", fontsize=12)
plt.ylabel("Return (%)", fontsize=12)
plt.title("Scatter Plot of Trade Returns for All Columns", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(title="Columns", loc='upper right')
plt.show()




#OVERFITTING GRAPH SEPERATLY
num_columns = len(sorted_df.columns)  
rows = (num_columns + 2) // 3  
cols = min(3, num_columns)    
fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
axes = axes.ravel()  
for idx, column in enumerate(sorted_df.columns):
    axes[idx].plot(sorted_df[column], marker='o', linestyle='-', alpha=0.7)
    axes[idx].set_title(f'{column}', fontsize=12)
    axes[idx].set_xlabel("Trade Number (Sorted by Return)", fontsize=10)
    axes[idx].set_ylabel("Return (%)", fontsize=10)
    axes[idx].grid(True, linestyle='--', alpha=0.6)
for i in range(len(axes)):
    if i >= num_columns:
        axes[i].axis('off') 
plt.tight_layout()
plt.show()