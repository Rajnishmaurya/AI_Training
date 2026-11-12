import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Section A - Data Handling and Data Types
# use: urban_mobility.csv, "uipment_events.json, and
# A1. Load urban_mobility.csv into a Pandas DataFrame and display the first five rows
df=pd.read_csv("urban_mobility.csv")
print("First 5 rows:",df.head(5))
# A2. Create a new column Energy_Per_Km = Energy_used kWh / Distance_Km.
df["Energy_Per_KM"]=df["Energy_Used_kWh"]/df["Distance_Km"]
print("Question 2: ",df["Energy_Per_KM"])
# A3. Display only Electric Van records where Maintenance Flag is Yes.
print("Question 3: ",df[(df["Vehicle_Type"]=="Electric Van") & (df["Maintenance_Flag"]=="Yes")])
# A4. Group by Vehide Tm and display average Distance Km and total
print("Question 4: ", df.groupby("Vehicle_Type").agg({"Distance_Km":"mean","Trips_Count":"sum"}))
# A5. Use NumPy to czlculate the mean, maximum and minimum of Energy_Used kWh
energy=df["Energy_Used_kWh"].to_numpy()
print("Question 5: ", np.mean(energy),np.max(energy),np.min(energy))
# A6. Create one bar chart showing Energy_Used_kWh by Vehicle_Type using Matplotlib or Seaborn
print("Question 6:")
df.groupby("Vehicle_Type")["Energy_Used_kWh"].mean().plot(kind="bar")
plt.show()
# A7. Load equipment_events.json and print event_id, asset type, site and severity for every event.
with open("equipment_events.json","r") as f:
    data=json.load(f)
print("Question 7:")
for event in data:
    print("event_id:",event["event_id"], "  asset_type:",event["asset"]["type"],"   site: ",event["asset"]["site"],"   severity: ",event["severity"])


# A8. Display JSON records with temperature above 70. If actions is missing, display 'No actions recorded'
print("Question 8:")
for event in data:
    temperature=event.get("temperature")
    if temperature is not None and temperature>70:
        print("Event ID: ", event["event_id"], " temperature: ", temperature)
        print("Actions:", event.get("actions") or "No actions recorded")

# A9. Read monitoring_log.txt and count total words and the number of times the word 'inspection'
print("Question 9:")

with open("coastal_monitoring_log.txt","r") as f:
    text=f.read()

word=text.split()
print("total words:",len(word))
print("inspection count:", word.count("inspection"))
#A10. Print only the lines containing either 'boardwalk', 'maintenance', or 'wind'.
print("Question 10: ")
keywords=["boardwalk","maintenance","wind"]
lines=text.split("\n")
for keyword in keywords:
    for line in lines:
        if keyword in line:
            print(f"line containing {keyword} :  ", line)

# Short concept: State which of the three supplied files is structured, semi-structured and unstructured, and give
# one reason for each



