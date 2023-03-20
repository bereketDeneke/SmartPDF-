'''
    Author: Bereket Deneke
    Date: 11/06/2022 (MM/DD/YYYY)
    Description: Transcribe scanned files
'''
import numpy as np
import cv2 
import os

# for more ocr accuracy, I used floodFill
def floodFill(img):
    point = (0,0)   
    src = img.copy()

    tolerance = 25
    connectivity = 4
    flags = connectivity
    flags |= cv2.FLOODFILL_FIXED_RANGE

    cv2.floodFill(src, None, point, (0, 255, 255), (tolerance,) * 3, (tolerance,) * 3, flags)
    src = cv2.subtract(255, src) 
    return src

def fillRectInPlaceOfText(img, TextPos, outPutFileName)->None:
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
            cv2.imwrite(outPutFileName,img)
        except Exception as e:
            print("Error is raised when trying to blur the image", e)

def DeleteAllImageFiles(folderName):
    for file in os.listdir(folderName):
        file_path = os.path.join(folderName, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print("Error is raised when trying to delete the image file", str(e))