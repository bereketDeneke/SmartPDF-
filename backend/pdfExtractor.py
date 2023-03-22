'''
    Author: Bereket Deneke
    Date: 11/06/2022 (MM/DD/YYYY)
    Description: Transcribe scanned pdf files
'''
# from pdf2image import convert_from_path
from pdf2image import convert_from_bytes

poppler_path  = r"C:\poppler-22.04.0\Library\bin"
def extract(file):
    try:   
        images = convert_from_bytes(pdf_file = file, fmt="png")
        return images
    except Exception as e:
        raise Exception(e)