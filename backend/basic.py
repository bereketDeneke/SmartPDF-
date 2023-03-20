'''
    Author: Bereket Deneke
    Date: 11/06/2022 (MM/DD/YYYY)
    Description: Transcribe scanned pdf files
    Purpose: To make digital archieves easly searchable 
'''
from .combiner import *
from config import *
from .processing import *
from .pdfExtractor import *
import pytesseract

def INIT(inputFileName, outPutFileName, type, LANGUAGE):    
    pdf = getPdf()
    img, orgImg, custom_config = config(inputFileName, pdf, type, LANGUAGE)
    height, width, channels = (None, None, None)
    try:
        height, width, channels = img.shape
    except Exception: 
        try:
            height, width = img.shape
        except Exception:
            height, width = [img.width, img.height]

    
    # if LANGUAGE != 'amh': # amh -> amharic
    #     cv2.imwrite(outPutFileName, img) # save the blue channels as an image
    # else:
    #     img = orgImg

    if type == 'summary':
        ResponseString = pytesseract.image_to_string(img, lang=LANGUAGE, config=custom_config)
        return ResponseString # if it's a summary no need to proceed to the next execution
    
    ResponseData = pytesseract.image_to_data(img, lang=LANGUAGE, config=custom_config)
    Header = ResponseData.split("\n")[0].replace("\t", " ").split(" ")
    Body = ResponseData.split("\n")[1:]
    Info = []

    for lines in Body:
        array = lines.replace("\t", " ").split(" ")
        
        try:
            # array[-2] is holds the accuracy level or confidence of the transcription
            if len(array) <= 2 or float(array[-2]) < 40: 
                continue
            temp = {}
            for j in range(len(array)):
                temp[Header[j]] = array[j]
            Info.append(temp)
        except:
            pass


    outPutFileName = inputFileName
    drawOnCanvas(Info, outPutFileName, height, width)

    orgImg = cv2.imread(inputFileName)
    fillRectInPlaceOfText(orgImg, Info, outPutFileName)
    return ResponseData
    