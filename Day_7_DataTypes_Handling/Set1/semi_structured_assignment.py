# Assignments
import pandas as pd
import json

# 1. Load the JSON file using Python.

with open("semi_structured_data.json", "r") as read_file:
    data = json.load(read_file)

print(data)
# 2. Print all incident IDs.
print("Question 2: \n")
for incident in data:
    print(incident["incident_id"])
# 3. Print the city of each incident.
print("City of each incident: \n")
for incident in data:
    print(incident["location"]["city"])

# 4. Display incidents where severity is High .
print("Incident where severity is hgh \n")

for incident in data:
    if incident["severity"] == "High":
        print(incident)

# 5. Display incidents where category is Safety .

print("Incidents where category is safety \n")
for incident in data:
    if incident["category"] == "Safety":
        print(incident)
# 6. Some incidents do not contain actions . Print:
# No actions recorded
# when the field is missing.
print("Incidents where actions is missing \n")
for incident in data:
    actions=incident.get("actions")

    if actions:
        print("Actions:",",".join(actions))
    else:
        print("No Actions recorded")
# 7. Count how many incidents belong to each severity level.
print("Severity Count ")

severity_count = {}

for incident in data:
    severity=incident["severity"]
    if severity in severity_count:
        severity_count[severity] += 1
    else:
        severity_count[severity] = 1
print(severity_count)
# 8. Add a new field:
# status = "Open"
# to every incident.
print("adding status as open")
for incident in data:
    incident["status"]="Open"
print(data)
# 9. Save the updated records to:
# updated_incidents.json

with open("updated_incident.json","w") as file:
    json.dump(data,file)
# 10. Convert the JSON into a Pandas DataFrame using:
# pd.json_normalize()
# and display:
# incident_id
# severity
# category
# location.city
# location.site

df=pd.json_normalize(data)

results=df[["incident_id","severity","category","location.city","location.site"]]
print(results)