# 1. Load the JSON file.
import json
import pandas as pd
with open("smart_home_devices.json", "r") as f:
    data=json.load(f)
# 2. Print:
# device_id
# device_type
# room
print("Printing device_id,device_type and room: ")
for device in data:
    print(device["device_id"], device["device_type"], device["room"])
# 3. Display only devices whose status is Active .
print("Printing only devices whose status is Active: ")
for device in data:
    if device["status"] == "Active":
        print(device)
# 4. Display devices whose battery level is below 60.
print("Printing devices whose battery level is below 60: ")
for device in data:
    if device["metrics"]["battery"] < 60:
        print(device)
# 5. Print the temperature only for devices that actually contain a temperature field.
print("Printing the temperature only for devices that actually contains a temperature: ")

for device in data:
    if "temperature" in device["metrics"]:
        print(device["metrics"]["temperature"])

# 6. Display devices that contain an alerts field.
print("Printing devices that contain an alerts field: ")
for device in data:
    alert=device.get("alerts")
    if alert:
        print(device)
# 7. Count how many devices exist for each device_type .
print("Count how many devices exist for each device_type")
device_count={}
for device in data:
    if device["device_type"] in device_count:
        device_count[device["device_type"]] += 1
    else:
        device_count[device["device_type"]] = 1
print(device_count)
# 8. Add a new field:
# health
# Rule:
# battery >= 70 → Good
# battery 50–69 → Moderate
# battery < 50 → Low

for device in data:
    if device["metrics"]["battery"]>=70:
        device["health"]="Good"
    elif device["metrics"]["battery"]>=50:
        device["health"]="Moderate"
    else:
        device["health"]="Low"
print(data)
# 9. Save the updated JSON into:
# device_health_report.json

with open("device_health_report.json","w") as f:
    json.dump(data,f)

# 10. Convert the JSON into a DataFrame using pd.json_normalize() and display:
# device_id
# device_type
# room
# status
# metrics.battery
# health
print("Convert json to DataFrame")
df=pd.json_normalize(data)
print(df[["device_type","device_type","room","status","metrics.battery","health"]])

# Extra challenge
# Display only:
# Active devices with battery below 70
print("Active devices with battery below 70:\n",df[df["metrics.battery"]<70])
