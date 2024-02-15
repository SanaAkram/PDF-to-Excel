import pdfminer
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import XMLConverter
from io import BytesIO


def extract_text_and_layout(pdf_path):
    # Create a BytesIO object to hold the XML output
    output = BytesIO()

    with open(pdf_path, 'rb') as fp:
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = XMLConverter(rsrcmgr, output, codec='utf-8', laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # Process each page
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    # Get the XML content from the BytesIO object
    xml_content = output.getvalue().decode('utf-8')

    # Save the XML content to a file
    with open('output.xml', 'w', encoding='utf-8') as xml_file:
        xml_file.write(xml_content)


if __name__ == "__main__":
    pdf_file = 'inputs/4pt Template.pdf'
    extract_text_and_layout(pdf_file)



# import fitz  # PyMuPDF
# import cv2
# import numpy as np
#
# def locate_checkboxes(pdf_file):
#     doc = fitz.open(pdf_file)
#     page = doc[0]  # Assuming you want to process the first page
#
#     # Extract images and text from the page
#     images = page.get_images(full=True)
#     page_text = page.get_text()
#
#     checkbox_data = []
#
#     for image in images:
#         x0, y0, x1, y1, z, b, d, c, e, a = image
#
#         # Extract text near the checkbox based on coordinates
#         nearby_text = extract_text_near_checkbox(page_text, x0, y0, x1, y1)
#
#         # Check if the image is checked
#         is_checked = is_checkbox_checked(image)
#
#         # Record checkbox data (position, text, and value)
#         checkbox_data.append({
#             "x0": x0,
#             "y0": y0,
#             "x1": x1,
#             "y1": y1,
#             "text": nearby_text,
#             "is_checked": is_checked
#         })
#
#     return checkbox_data
#
# def extract_text_near_checkbox(page_text, x0, y0, x1, y1, margin=10):
#     # Extract text within a specified region near the checkbox coordinates
#     text_near_checkbox = ""
#
#     for line in page_text.split('\n'):
#         # Check if the line's bounding box intersects with the checkbox region
#         if (
#             float(line['x1']) > x0 - margin and
#             float(line['x0']) < x1 + margin and
#             float(line['y1']) > y0 - margin and
#             float(line['y0']) < y1 + margin
#         ):
#             # Concatenate the line's text within the region
#             text_near_checkbox += line['text'] + ' '
#
#     return text_near_checkbox.strip()
#
# def is_checkbox_checked(image, threshold=10000):
#     # Implement image processing to check if the image contains a checkmark
#     _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
#     checked_pixels = cv2.countNonZero(binary_image)
#
#     return checked_pixels > threshold
#
# if __name__ == "__main":
#     pdf_file = 'sample.pdf'
#     checkbox_data = locate_checkboxes(pdf_file)
#
#     for checkbox in checkbox_data:
#         print(f"Checkbox at ({checkbox['x0']}, {checkbox['y0']}) - Text: {checkbox['text']} - Checked: {checkbox['is_checked']}")
