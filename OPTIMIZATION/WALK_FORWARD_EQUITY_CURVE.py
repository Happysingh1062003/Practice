import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd 

a = pd.read_csv("WALK_FORWARD_EQUITY_CURVE.csv")
print(a)


def format_func(value, _):
    return f"{value:.7f}"
formatter = FuncFormatter(format_func)
plt.figure(figsize=(8, 5))
plt.plot(a)
plt.gca().yaxis.set_major_formatter(formatter)

plt.xlabel('Index')
plt.ylabel('Value')
plt.title('Plot with High Precision Y-Axis')
plt.grid(True)
plt.show()
