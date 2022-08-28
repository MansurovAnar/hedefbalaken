from PyPDF2 import PdfFileReader, PdfFileWriter
import re

# PDF location
read_source = r"C:\Users\GandA\Documents\GandA\Projects\forHeroku\media\pdf\8.pdf"
write_source = r"C:\Users\GandA\Documents\GandA\Projects\forHeroku\media\pdf\8sum9\{}"

largePdf = PdfFileReader(open(read_source, 'rb'))

# Search regex
regex = '\d+'

for i in range(largePdf.numPages):
    output = PdfFileWriter()
    page = largePdf.getPage(i)
    output.addPage(page)

    # Extract text from page № i
    text_in_page = page.extractText()

    # Find all digits in text_in_page
    match = re.findall(regex, text_in_page)
    print("ALl: ", match)
    # print("Say: ", i)

    ish_nomresi = ""
    for num in match[:10]:
        if "721" in num:
            if len(num) == 7:
                ish_nomresi = num
                print("equal")
            elif len(num) > 7:
                ish_nomresi = num[2:]
                print("not equal")
            print("Ish nomresi", ish_nomresi)

    # Student ID
    # ish_nomresi = match[0][2:]
    # print(match[0][2:])

    with open(write_source.format("%s.pdf" % ish_nomresi), "wb") as outputStream:
        output.write(outputStream)



