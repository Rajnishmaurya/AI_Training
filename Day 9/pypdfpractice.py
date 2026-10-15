import fitz
print("\n Exercise 1 — PyMuPDF \n")
# Tasks:
# 1. Open the PDF.
doc=fitz.open("EY_Digital_PDF_Practice.pdf")
# 2. Print the number of pages.
print("Pages: ",len(doc))

# 3. Extract and print text from page 1.
page1_text=doc[0].get_text()
print("Text from page 1: ", page1_text)

# 4. Extract text from all pages.
for page in doc:
    print(page.get_text())

# 5. Search whether the word maintenance appears.
all_text=""
for page in doc:
    all_text+=page.get_text() + "\n"

if "maintenance" in all_text.lower():
    print("Word Maintenance is found in the pdf")
else:
    print("Word Maintenance is not found in the pdf")


# 6. Count how many times V303 appears.
print("\nV303 count: ",all_text.count("V303"))

# 7. Extract only page 2 text.

page2_text=doc[1].get_text()
print("Page 2 content only: ",page2_text)

# 8. Save all extracted text into digital_pdf_text.txt .
with open("digital_pdf_text.txt","w") as f:
    f.write(all_text)

doc.close()

print("\n Exercise 2 — PyPDF \n")

# Tasks:
# 1. Open the PDF using PdfReader .
from pypdf import PdfReader
reader=PdfReader("EY_Digital_PDF_Practice.pdf")

# 2. Print the number of pages.
print("Number of pages: ", len(reader.pages))
# 3. Extract text from the first page.
page1_text=reader.pages[0].extract_text()
print("Text from page 1: \n", page1_text)
# 4. Extract text from the second page.
page2_text=reader.pages[1].extract_text()
print("Text from page 2: \n", page2_text)
# 5. Combine text from both pages into one string.
combined_text=page1_text+page2_text
print("Combined text from page 1 and page 2: \n", combined_text)

# 6. Check whether NorthStar Maintenance exists in the PDF.
all_text=""
for page in reader.pages:
    all_text+=page.extract_text() + "\n"

if "NorthStar Maintenance" in all_text.lower():
    print("\n NorthStar Maintenance is found in the pdf")
else:
    print("NorthStar Maintenance is not found in the pdf")

# 7. Find the number of occurrences of the word vendor .
print("vendor count: ", all_text.count("vendor"))

# 8. Save the extracted content into pypdf_output.txt .
with open("pypdf_output.txt","w") as f:
    f.write(all_text)



print("\n Exercise 3 — Tesseract OCR \n")

import fitz
import pytesseract
from PIL import Image
# Tasks:
# 1. Open the scanned PDF using PyMuPDF.
doc=fitz.open("EY_Scanned_PDF_OCR_Practice.pdf")

# 2. Convert the PDF page into an image.
page=doc[0]
pix=page.get_pixmap()
pix.save("scanned_image.png")
# 3. Run Tesseract OCR on the image.
image=Image.open("scanned_image.png")
text=pytesseract.image_to_string(image)


# 4. Print the extracted text.
print("Extracted text:",text)

# 5. Check whether Forklift FL-17 was detected.

if "Forklift FL-17".lower() in text.lower():
    print("Forklift FL-17 is found in the pdf")
else:
    print("Forklift FL-17 is not found in the pdf")
# 6. Search for the word injuries .
if "injuries" in text.lower():
    print("Injuries are found in the pdf")
else:
    print("Injuries are not found in the pdf")

# 7. Extract lines mentioning inspection .
print("\n Line containing inspection: ")
for line in text.split("\n"):
    if "inspection" in line.lower():
        print(line)

# 8. Save the OCR output into ocr_result.txt .
with open("ocr_result.txt","w") as f:
    f.write(text)

# 9. Count the number of times inspection appears.
print("inspection count: " ,text.count("inspection"))

# 10. Print all lines containing Loading Bay .
print("Lines containing Loading Bay: \n")
for line in text.split("\n"):
    if "Loading Bay".lower() in line.lower():
        print(line)

doc.close()
