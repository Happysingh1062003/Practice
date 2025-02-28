import pandas as pd
import matplotlib.pyplot as plt
import vectorbt as vbt


data = pd.read_csv("0_backtest.csv")
df = pd.DataFrame(data)
df=df.set_index("Parameter")

df["Score"] = +df["Returns"]

best_params = df.sort_values("Score", ascending=False).head(10)

print("Best Parameters:")
print(best_params)


plt.figure(figsize=(10, 7))
plt.bar(df.index, data["Returns"])
plt.xticks(rotation=90)
plt.title('Returns')
plt.xlabel('Parameters')
plt.ylabel('Total Return')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


