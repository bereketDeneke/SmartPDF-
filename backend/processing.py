'''
    Author: Bereket Deneke
    Date: 11/06/2022 (MM/DD/YYYY)
    Description: Transcribe scanned files
'''
import numpy as np
import cv2 

# for more ocr accuracy, I used tresh inversion
def treshInversion(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # threshold the image using Otsu's thresholding method
    thresh = cv2.threshold(gray, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    return thresh


def fillRectInPlaceOfText(img, TextPos)->None:
    for pos in TextPos:
        # img = cv2.blur(img, (pos[0], pos[1], pos[0], pos[1]))
        try:
            initialPosY = int(pos['top'])
            initialPosX = int(pos['left'])

            finalPosY = int(initialPosY + int(pos['height']))
            finalPosX = int(initialPosX + int(pos['width']))

            # bluring image
            kernel = 100
            blurredPart = cv2.blur(img[initialPosY:finalPosY, initialPosX:finalPosX], ksize=(kernel, kernel))

            avg_color_per_row = np.average(blurredPart, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)

            cv2.rectangle(img,(finalPosX,finalPosY),(initialPosX,initialPosY),avg_color,-1) # -1 means fill rectanlg with color and 5 is stroke
            # cv2.imwrite(outPutFileName,img)
            return img
        except Exception as e:
            print("Error is raised when trying to blur the image", e)
