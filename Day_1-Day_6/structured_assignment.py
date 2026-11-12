import pandas as pd

df=pd.read_csv("library_loans.csv")
print(df)
print(df[["Member_Name","Book_Category","Fine"]])

print("Filtered Data:", df[df["Fine"]>50])


# 4. Create a new column called Status :
# No Fine if Fine = 0
# Fine Due otherwise
df["Status"]=df["Fine"].apply(lambda fine:"No Fine" if fine==0 else "Fine DUe")
print(df)

# Find the average number of days borrowed.
print("Average number of days borrowed:", df["Days_Borrowed"].mean())

# Find the total fine collected by Book_Category.
print("Total fine collected by book category:", df.groupby("Book_Category")["Fine"].sum().reset_index())