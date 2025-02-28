import vectorbt as vbt 
import pandas_ta as ta
import pandas as pd 
import matplotlib.pyplot as plt

btcusdt=pd.read_csv("../CRYPTO DATA/BTCUSDT.csv")
btcusdt['Time'] = pd.to_datetime(btcusdt['Time'])
btcusdt.set_index('Time', inplace=True)
btcusdt = btcusdt.resample("1h",offset='30min').agg({
    'Open': 'first',
    'High': 'max',
    'Low': 'min',        
    'Close': 'last',
    'Volume': 'sum'   
})


alma = vbt.IndicatorFactory.from_pandas_ta("alma")
ema = vbt.IndicatorFactory.from_talib('ema')

fastalma=alma.run(btcusdt["Close"],50,6,0.55,0).alma
ema=ema.run(btcusdt['Close'],50).real

plt.plot(btcusdt['Close'])
plt.plot(alma)
plt.plot(ema)
plt.plot(fastalma)
plt.show()