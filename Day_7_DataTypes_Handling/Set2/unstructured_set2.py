import keyword

with open("airport_operations_report.txt","r") as f:
    text=f.read()
# 1. Read the complete report.
print(text)
# 2. Count:
# total words
# total lines
# total characters
words=text.split()
lines=text.split('\n')
print("Count total words, total line, total characters respectively:",len(words),",", len(lines),",",len(text))
# 3. Count how many times the words below occur:
# flight
# runway
# operations
# reported
keywords=["flight","runway","operations","reported"]
print("Count occurrences of words flight,runway,operations,reported:")

for keyword in keywords:
    print(keyword,":" ,words.count(keyword))

# 4. Print only lines containing the word:
# runway

lines=text.split('\n')
print("Printing lines that that contain word runway: ")
for line in lines:
    if "runway" in line:
        print(line)
# 5. Print only lines containing either:
# delay
# delayed
# delays
print("Printing lines that contain words either delay,delayed,delays: ")
lines=text.split('\n')
for line in lines:
  if "delay" in line or "delayed" in line or "delays" in line:
      print(line)



# 6. Extract all lines that mention something being reported .
lines=text.split('\n')
print("Printing lines that mention something being reported: ")
for line in lines:
    if "reported" in line:
        print(line)

# 7. Check whether these words appear:
# emergency
# inspection
# weather
# passengers
# maintenance
words=["emergency","inspection","weather","passengers","maintenance"]
print("Word present or not: ")
word=text.split()
for w in words:
    if w in word:
        print(w,":", "found")
    else:
        print(w,":", "not found")
# 8. Create a dictionary like:
# {
# }
# "flight": count,
# "runway": count,
# "operations": count
word_count={}
word=["flight","runway","operations"]
words=text.split()
for w in word:
    word_count[w]=words.count(w)
print("Word count: ",word_count)
# 9. Find the longest line in the report.
longest_line=""
lines=text.split('\n')
for line in lines:
    if len(line)>len(longest_line):
        longest_line=line
print("Longest line:",longest_line)
# 10. Save only the lines related to delays or weather into:
# filtered_airport_report.txt
lines=text.split('\n')
with open("filtered_airport_report.txt","w") as f:
    for line in lines:
        if "delays" in line or "weather" in line:
            f.write(line)
