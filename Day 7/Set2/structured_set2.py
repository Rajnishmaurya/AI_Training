import pandas as pd
# 1. Load the CSV into a Pandas DataFrame.
df=pd.read_csv("renewable_energy.csv")
print(df.head())
# 2. Display plants where Energy_Type is either Solar or Wind .
results=df[df["Energy_Type"].isin(["Solar","Wind]"])]
print("Plants where Energy_type is either solar or wind.\n",results)
# 3. Create a new column:
# Efficiency_Percent =
# Actual_Output_MW / Capacity_MW * 100

df["Efficiency_Percent"]=(df["Actual_Output_MW"]/df["Capacity_MW"])*100
print("Added a new column Efficiency_Percent: \n",df.head())
# 4. Display only plants with efficiency above 85%.
print("Plants where Efficiency_Percent is greater than 85: \n", df[df["Efficiency_Percent"]>85])
# 5. Find the average efficiency for each energy type.
print("Average efficiency for each energy type: \n",df.groupby("Energy_Type")["Efficiency_Percent"].mean())
# 6. Find the total maintenance cost for each energy type.
print("Total maintenance cost for each energy type: \n", df.groupby("Energy_Type")["Maintenance_Cost"].sum())
# 7. Display the plant with the highest Actual_Output_MW .
print("Plant with highest Actual_Output_MW: ", df.loc[df["Actual_Output_MW"].idxmax()])
# 8. Create a new column:
# Cost_Per_MW =
# Maintenance_Cost / Actual_Output_MW
df["Cost_Per_MW"]=df["Maintenance_Cost"]/df["Capacity_MW"]
print("Cost_Per_MW",df["Cost_Per_MW"])
# 9. Sort plants by Cost_Per_MW from lowest to highest.
print("Cost_Per_MW from lowest to highest: \n",df.sort_values("Cost_Per_MW"))
# 10. Display only those plants where:
# efficiency is above 80%
# maintenance cost is below 70000

print("Efficiency is above 80 and maintenance cost is below 70000: \n", df[(df["Efficiency_Percent"]>80) & (df["Maintenance_Cost"]<70000)])
# Extra challenge
# Create a bar chart showing:
# Plant_Name vs Efficiency_Percent

import matplotlib.pyplot as plt
plt.bar(df["Plant_Name"],df["Efficiency_Percent"])
plt.xlabel("Plant Name")
plt.ylabel("Efficiency (%)")
plt.title("Efficiency vs Plant Name")
plt.show()