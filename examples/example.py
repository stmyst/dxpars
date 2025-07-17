from dxpars.document import Document

document = Document('example.docx')

# document text
print(document.text)

# show document structure
print(document.body.show)

# document parts
print(document.parts)

# text of each paragraph
for paragraph in document.paragraphs:
    if paragraph.text:
        print(paragraph.text)

# each docx object has main properties
print(document.paragraphs[0].properties)

# other properties can be found in object formatting part
print(document.paragraphs[0].formatting.properties)

# paragraphs with bullet
for paragraph in document.paragraphs:
    if paragraph.bullet:
        print(paragraph.text)

# select paragraph runs by format
for paragraph in document.paragraphs:
    for run in paragraph.parts:
        if run.bold:
            print(f'bold text: {run.text}')
        if run.italic:
            print(f'italic text: {run.text}')
        if run.underline:
            print(f'underline text: {run.text}')

# show document table structure
print(document.tables[0].show)

# for tables with merged cells
print(document.tables[1].expand)

# dict representation (can be json serialized)
print(document.to_dict)
