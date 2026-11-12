import json
with open("festival_events.json") as f:
    events=json.load(f)

for event in events:
    print(event["name"])

for event in events:
    print(event["location"]["city"])

for event in events:
    if event["visitors"]>700:
        print(event)

for event in events:
    features=event.get("features","No features listed")
    if isinstance(features,list):
        features=",".join(features)
    print(f"{event['name']}: {features}")

import pandas as pd

df=pd.json_normalize(events)

print(df)