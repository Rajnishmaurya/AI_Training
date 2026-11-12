import pandas as pd
# 1. Load the CSV into a DataFrame.
df=pd.read_csv("structured_data.csv")
# 2. Display only:
# Shipment_ID
# Origin
# Destination
# Cost
print(df[["Shipment_ID","Origin","Destination","Cost"]])
# 3. Show all shipments where Mode is Road .
print("Shipment where mode is Road:\n", df[df["Mode"]=="Road"])

# 4. Show shipments with Weight_Kg greater than 150.
print("Shipment where weight greater than 50\n", df[df["Weight_Kg"]>50])

# 5. Create a new column:
# Cost_Per_Km = Cost / Distance_Km

df["Cost_Per_Km"]=df["Cost"]/df["Distance_Km"]
print("Cost Per KM")
print(df.head())
# 6. Find:
# average shipment cost
# highest shipment cost
# lowest shipment cost
print("Average Shipment cost:\n",df["Cost"].mean())

print("Highest shipment cose:\n",df["Cost"].max())
print("Lowest shipment cose:\n",df["Cost"].min())


# 7. Group by Mode and calculate total cost.
print("Question 7: \n", df.groupby("Mode")["Cost"].sum())

# 8. Group by Mode and calculate average weight.
print("Question 8: \n", df.groupby("Mode")["Weight_Kg"].mean())
# 9. Sort shipments from highest to lowest cost.
print("Question 9 Shipment cost from highest to lowest: \n", df.sort_values("Cost",ascending=False))

# 10. Display shipments where:
# Delivery_Days <= 1
# and Cost < 5000

print("Question 10: \n", df[(df["Delivery_Days"]<=1) & (df["Cost"]<5000)])