import json
import pandas as pd
with open("support_teckets.json") as file:
    tickets=json.load(file)
print(tickets)
print(tickets[0])
print(tickets[0]["issue"])
print(tickets[0]["customer"]["name"])


for ticket in tickets:
    print(ticket["ticket_id"],ticket["issue"])
# convert the json data to csv format
df=pd.json_normalize(tickets)
print(df)