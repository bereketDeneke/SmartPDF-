'''
    Author: Bereket Deneke
    Date: 11/06/2022 (MM/DD/YYYY)
    Description: Transcribe scanned pdf files
'''
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from backend.processing import *
import cv2 
from reportlab.lib.colors import PCMYKColor, PCMYKColorSep, Color, black, blue, red

### Configuration ###

page_separator = "" # serparate between the transcriptions per page
fully_transparent = Color(0, 0, 0, 0) # I use alpha value of zero to hide the transcription behind the image/orginal text

LEVEL = 11 # Level of transcription detail
FONTSIZE = 9 # change as neede: 12 | 8
# OCR alphabetic characters only
# OPTIONAL = "-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
OPTIONAL = ""


def config(inputFileName, pdf, type, LANGUAGE):
    try:
        if LANGUAGE == "amh":
            # page_separator = "================================\n"
            pdfmetrics.registerFont(
            TTFont('ancient', './fonts/washrab.ttf')
            )
        else:
            pdfmetrics.registerFont(
            TTFont('ancient', './fonts/El Franco W00 Regular.ttf')
            )

        OrgImg = cv2.imread(inputFileName) # orginal Image object
        img = OrgImg #floodFill(OrgImg)

        if type == 'transcription':
            # pdf.setAuthor('Public')
            # pdf.setSubject('Fairy tales, Arabs, Folklore, Fairy tales, Arabs, Folklore')
            pdf.setCreator('Scan2PDF+')
            # pdf.setProducer('Kerven, Rosalind; Mistry, Nilesh, ill')
            pdf.setKeywords("transcriped, Scan2 pdf+, pdf+")
            pdf.setTitle('Scan2 PDF+')
            pdf.setFont("ancient", FONTSIZE)

        return img, OrgImg, f'--oem 3 --psm {LEVEL} {OPTIONAL}'
    except Exception as e: 
        raise Exception(e)