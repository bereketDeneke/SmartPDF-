'''
    Author: Bereket Deneke
    Date: 11/06/2022 (MM/DD/YYYY)
    Description: Transcribe scanned pdf files
'''
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from backend.processing import *
from reportlab.lib.colors import PCMYKColor, PCMYKColorSep, Color, black, blue, red

### Configuration ###
page_separator = "" # serparate between the transcriptions per page
fully_transparent = Color(0, 0, 0, 0) # I use alpha value of zero to hide the transcription behind the image/orginal text

LEVEL = 11 # Level of transcription detail
FONTSIZE = 9 # change as neede: 12 | 8
# OCR alphabetic characters only
# OPTIONAL = "-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
OPTIONAL = ""

def config(inputImage, pdf, type, LANGUAGE):
    pdfmetrics.registerFont(TTFont('amh', './fonts/washrab.ttf'))
    pdfmetrics.registerFont(TTFont('eng', './fonts/El Franco W00 Regular.ttf'))
    pdfmetrics.registerFont(TTFont('ara', './fonts/(A) Arslan Wessam A (A) Arslan Wessam A.ttf'))
    pdfmetrics.registerFont(TTFont('spa', './fonts/Merienda-Regular.ttf'))

    try:
        img = np.array(inputImage) 
        if LANGUAGE == 'amh':
            img = treshInversion(img)

        if type == 'transcription':
            pdf.setCreator('Scan2PDF+')
            pdf.setKeywords("transcriped, Scan2 pdf+, pdf+")
            pdf.setTitle('Scan2 PDF+')
            pdf.setFont(LANGUAGE, FONTSIZE)

        return img, f'--oem 3 --psm {LEVEL} {OPTIONAL}'
    except Exception as e: 
        raise Exception(e)