import vectorbt as vbt 

def entry_signals(close,fast_window, slow_window):
    EMA=vbt.IndicatorFactory.from_talib("EMA")
    fastsema=EMA.run(close,fast_window).real
    slowsema=EMA.run(close,slow_window).real
    enter = (fastsema > slowsema) 
    return enter

def exit_signals(close,  fast_window, slow_window):
    EMA=vbt.IndicatorFactory.from_talib("EMA")
    fastsema=EMA.run(close,fast_window).real
    slowsema=EMA.run(close,slow_window).real
    exit = (fastsema < slowsema)
    return exit