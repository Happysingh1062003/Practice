import vectorbt as vbt 

def entry_signals(close, bb_window, rsi_window,std_dev):
    BB=vbt.IndicatorFactory.from_talib("BBANDS")
    RSI=vbt.IndicatorFactory.from_talib("RSI")
    lowerband=BB.run(close,bb_window,std_dev,std_dev).lowerband.to_numpy()
    rsivalue=RSI.run(close,rsi_window).real.to_numpy()
    enter = (close < lowerband) & (rsivalue < 30) 
    return enter

def exit_signals(close, bb_window, rsi_window,std_dev):
    BB=vbt.IndicatorFactory.from_talib("BBANDS")
    RSI=vbt.IndicatorFactory.from_talib("RSI")
    upperband=BB.run(close,bb_window,std_dev,std_dev).upperband.to_numpy()
    rsivalue=RSI.run(close,rsi_window).real.to_numpy()
    exit = (close > upperband) & (rsivalue > 70)
    return exit