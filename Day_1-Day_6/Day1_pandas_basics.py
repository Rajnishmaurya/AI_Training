import pandas as pd

data = {
    "Product": ["Laptop", "Mouse", "Keyboard", "Laptop", "Mouse"],
    "City": ["Hyderabad", "Mumbai", "Delhi", "Hyderabad", "Delhi"],
    "Quantity": [2, 5, 3, 1, 4],
    "Price": [60000, 800, 1500, 60000, 800]
}

df = pd.DataFrame(data)

# print(df)
# print(df.head())
# print(df.shape)
df["Total"]=df["Quantity"]*df["Price"]
# print(df)
# print(df.groupby("Product")["Total"].sum())

# print(df.sort_values(by="Total", ascending=False))


# import matplotlib.pyplot as plt
# sales=df.groupby("Product")["Total"].sum()
# sales.plot(kind="bar")
# plt.xlabel("Product")
# plt.ylabel("Total Sales")
# plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

sns.barplot(data=df, x="Product", y="Total")

plt.title("Sales by Product")
plt.show()