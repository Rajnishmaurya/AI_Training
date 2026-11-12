import json
import pandas as pd
with open("incident_notes.txt") as file:
    text=file.read()
print(text)
words=text.split()

print(len(words))

# Search
if "vibration" in text.lower():
    print("vibration found")
print(text.lower().count("vibration"))


