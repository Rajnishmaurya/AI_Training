# 1. Read the complete text file.
# 2. Count the total number of words.
# 3. Check whether the word elephant appears in the report.
# 4. Count how many times elephant appears.
# 5. Print only the lines containing the word trail .
# 6. Print only the lines containing the word animal

import pandas as pd

with open("wildlife_report.txt") as file:
    text=file.read()
print(text)

words=text.split()
print("Total number of words:", len(words))

if "elephent" in text.lower():
    print("Elephent found")

print("Elephent Count:", text.lower().count("elephent"))

lines=text.strip().split("\n")
for line in lines:
    if "trail" in line.lower():
        print(line)
for line in lines:
    if "animal" in line.lower():
        print(line)