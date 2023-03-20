'''
    Author: Bereket Deneke
    Date: 11/06/2022 (MM/DD/YYYY)
    Description: Transcribe scanned pdf files
'''
from reportlab.pdfgen import canvas
from reportlab.lib.colors import PCMYKColor, PCMYKColorSep, Color, black, blue, red
from config import *

FILE_NAME = './Result/Scan2pdf+_transcribed.pdf'
pdf = canvas.Canvas(FILE_NAME)

def drawOnCanvas(Info, ImagePath, height, width):
    ImageWidth = width #1476
    ImageHeight = height #1982

    # Standard letter size pdf document dimensions
    PdfWidth = 612
    PdfHeight = 792

    pdf.drawImage(ImagePath, 0, 0, width =  PdfWidth, height= PdfHeight)# ,preserveAspectRatio=True)
    
    for data in Info:
        content = data['text']
        X = (int(data['left']) * PdfWidth) / ImageWidth
        Normalizer = 10
        # fontSize = 12#int(data['height']) * PdfHeight / ImageHeight - Normalizer
        Y = PdfHeight - (int(data['top']) * PdfHeight) / ImageHeight - Normalizer
        
        # pdf.setFillColor(black)
        pdf.setFillColor(fully_transparent)
        pdf.drawString(X, Y, content)
    pdf.showPage()

def getPdf():
    return pdf

def saveTheFIle():
    try:
        pdf.save()
    except Exception as e:
        print("Save Failed "+str(e))