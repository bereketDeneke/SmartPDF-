'''
    Author: Bereket Deneke
    Date: 11/06/2022 (MM/DD/YYYY)
    Description: Transcribe scanned pdf files
'''
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import PCMYKColor, PCMYKColorSep, Color, black, blue, red
from config import *
import io

class PDFWriter:
    def __init__(self):
        self.FILE_STREAM = io.BytesIO() #'./Result/Scan2pdf+_transcribed.pdf'
        self.__pdf = canvas.Canvas(self.FILE_STREAM)

    def drawOnCanvas(self, Info, outputImage, height, width):
        try:
            ImageWidth = width #1476
            ImageHeight = height #1982

            # Standard letter size pdf document dimensions
            PdfWidth = 612
            PdfHeight = 792

            buf = io.BytesIO()
            outputImage.save(buf, format='PNG')
            buf.seek(0)
            file = ImageReader(buf)
            
            self.__pdf.drawImage(file, 0, 0, width =  PdfWidth, height= PdfHeight)# ,preserveAspectRatio=True)
    
            for data in Info:
                content = data['text']
                X = (int(data['left']) * PdfWidth) / ImageWidth
                Normalizer = 10
                # fontSize = 12#int(data['height']) * PdfHeight / ImageHeight - Normalizer
                Y = PdfHeight - (int(data['top']) * PdfHeight) / ImageHeight - Normalizer
                
                # self.__pdf.setFillColor(red)
                self.__pdf.setFillColor(fully_transparent)
                self.__pdf.drawString(X, Y, content)
            self.__pdf.showPage()
        except Exception as e:
            raise Exception(f"combiner {str(e)}")

    def getPdf(self):
        return self.__pdf

    def saveTheFIle(self):
        try:
            self.__pdf.save()
        except Exception as e:
            print("Error >> Save Failed "+str(e))