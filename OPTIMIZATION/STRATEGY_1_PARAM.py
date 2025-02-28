import vectorbt as vbt 

# Example entry and exit signal functions
def entry_signals(close, window):
    ALMA=vbt.IndicatorFactory.from_pandas_ta("alma")
    alma=ALMA.run(close,window,6,0.55).alma
    enter =  (close > alma) 
    return enter

def exit_signals(close,  window):
    ALMA=vbt.IndicatorFactory.from_pandas_ta("alma")
    alma=ALMA.run(close,window,6,0.55).alma
    exit =  (close < alma)
    return exit
