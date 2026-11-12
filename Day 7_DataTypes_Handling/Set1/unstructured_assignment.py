# 1. Read and print the complete text file.

with open("unstructured_data.txt") as file:
    text=file.read()
print(text)

# 2. Count the total number of words.

words=text.split()
print("Number of words:",len(words))
# 3. Count the total number of lines.
lines=text.splitlines()
print("Number of lines:",len(lines))


# 4. Check whether the word:
# maintenance
# appears in the report.
if "maintenance" in text:
    print("Maintenance word is presents")
else:
    print("Maintenance word is not presents")
# 5. Count how many times the word:
# conveyor
# appears.
words=text.split()
print("Count of word conveyor: ",words.count("conveyor"))
# 6. Print only lines containing:
# team
print("Line containing team:")
lines=text.splitlines()

for line in lines:
    if "team" in line:
        print(line)
# 7. Print only lines containing:
# incident
print("Line containing incident:")
lines=text.splitlines()
for line in lines:
    if "incident" in line:
        print(line)
# 8. Find and print the sentence that mentions the damaged component.
print("Sentence that mentions the words damaged component")
sentence=text.split(".")

for sentence in sentence:
    if "damaged component" in sentence.lower():
        print(sentence.strip())

# 9. Convert the complete text to lowercase and save it as:
# lowercase_report.txt
text=text.lower()

with open("lowercase_report",'w') as file:
    file.write(text)
# 10. Create a simple summary showing whether these keywords appear:
# maintenance
# injuries
# inspection
# replacement
# operations
# Expected format:
# maintenance : Found
# injuries    : Found
# inspection  : Found
# replacement : Found
# operations  : Found

keywords=["maintenance","injuries","replacement","operations"]

for keyword in keywords:
    if keyword in text.lower():
        print(f"{keyword}:Found")
    else:
        print(f"{keyword}:Not Found")