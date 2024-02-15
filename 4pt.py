import os

import PyPDF2
import fitz.fitz
import pandas as pd
import tabula
import camelot
from PyPDF2 import PdfFileReader
import pdfplumber
import csv
import re
import json
import cv2
# File paths
from pdfquery import pdfquery

first_temp_file = 'inputs/4pt Template.pdf'
output_csv = 'outputs/output.csv'


# Getting images of any file
def get_images(file_name):
    pdf_document = fitz.open(file_name)
    # Create a folder to store the images
    image_folder = 'images_' + file_name.replace('inputs/', '')
    os.makedirs(image_folder, exist_ok=True)

    # Loop through all pages of the PDF
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)

        # Loop through the images on the page
        for image_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_data = base_image['image']

            # Save the image to the folder
            image_filename = os.path.join(image_folder, f'page_{page_number}_image_{image_index}.png')
            with open(image_filename, 'wb') as image_file:
                image_file.write(image_data)

    # Close the PDF document
    pdf_document.close()


def format_address(input_address):
    # Split the address into its components based on common delimiters
    address_parts = re.split(r',|(?<=[A-Za-z])(?=\d)|(?<=\d)(?=[A-Za-z])', input_address)

    # Remove any empty or whitespace-only parts
    address_parts = [part.strip() for part in address_parts if part.strip()]

    # Construct the formatted address
    if len(address_parts) == 4:
        street = address_parts[0]
        city = address_parts[1]
        state = address_parts[2]
        zipcode = address_parts[3]
        formatted_address = f"{street} {city}, {state} {zipcode}"
        return formatted_address

    return input_address


def get_checkbox(file_name):
    try:
        checkbox_data = []
        pdf = pdfquery.PDFQuery('file.pdf')
        pdf.load()
        pdf.tree.write('pdfXML.txt', pretty_print=True)
        return checkbox_data
    except Exception as e:
        print(f"Error: {e}")
        return []


def extract_data_to_csv(file_name, output_csv):
    data_list = []
    try:
        with pdfplumber.open(file_name) as pdf:
            extracted_data = []

            for page in pdf.pages:
                checked_boxes = []
                unchecked_boxes = []
                data = page.extract_text()

                # Split the text into lines to process label-value pairs
                lines = data.split('\n')

                # Initialize variables to store label and value
                label = ""
                value = ""

                for line in lines[1:]:
                    parts = line.split(':')
                    if 'Insured/Applicant' in line:
                        name = parts[1].replace(' Application/Policy#', '')
                        policy_num = parts[2]
                        continue
                    elif 'Address' in line:
                        address = format_address(parts[1])
                        continue
                    elif 'ActualYearBuilt' in line:
                        year = parts[1].replace(' DateInspected', '')
                        date = parts[2]
                        continue
                    elif 'Dwelling' in line:
                        checked_boxes = get_checkbox(file_name)

                    if len(parts) > 1:  # Check if the line contains both label and value
                        label = parts[0].strip()
                        value = parts[1].strip()
                        extracted_data.append([label, value])
                    # Define the characters that typically represent checked and unchecked checkboxes
                    checked_char = u'\u2713'  # ✓ (Unicode checkmark symbol)
                    unchecked_char = u'\u2717'  # ✗ (Unicode cross mark symbol)

                    if checked_char in line:
                        checked_boxes.append(line)
                    elif unchecked_char in line:
                        unchecked_boxes.append(line)

                    # Check if the line contains a colon (":") to separate label and value
                    if ":" in line:
                        parts = line.split(":")
                        label = parts[0].strip()
                        value = parts[1].strip()
                    else:
                        # If no colon is found, assume the text continues as the value
                        value += " " + line.strip()

                    # Check if we have both label and value
                    if label and value:
                        extracted_data.append([label, value])
                        label = ""
                        value = ""
                data = {
                    'Insured/ApplicantName': name,
                    'Application/Policy#': policy_num,
                    'AddressInspected': address,
                    'ActualYearBuilt': year,
                    'DateInspected': date,

                }
            data_list.append(data)

        # Write the extracted data to a CSV file
        with open(output_csv, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(extracted_data)

    except Exception as e:
        print(e)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    extract_data_to_csv(first_temp_file, output_csv)
    get_images(first_temp_file)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
