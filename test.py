import pytesseract
from PIL import Image
import cv2
import sys
import pandas as pd
import csv
import os

#Testing conditions
test = False
if test:
    latestCSV = "latest_test.csv"
    dataCSV = "data_test.csv"
    rankCSV = "rank_test.csv"
else:
    latestCSV = "latest.csv"
    dataCSV = "data.csv"
    rankCSV = "rank.csv"

#Check latest file.
check = pd.read_csv(latestCSV)
latest_file = check.iloc[0,0]


def newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files if basename.endswith('.jpg')]
    return max(paths, key=os.path.getctime)
print(newest("resources"))
latest = pd.DataFrame([newest("resources")])
latest.to_csv(latestCSV,index = False)
if latest_file == newest("resources"):
    sys.exit("Item has been appended")

else:
    print("This will be appended")


#Read latest file.
file_path= newest("resources")
im = Image.open(file_path)
im.save("raw.jpg", dpi=(300, 300))

#Make image b&w.
im = Image.open("raw.jpg").convert("L")
im.save("bw.jpg")
readImage = cv2.imread("bw.jpg")

#Invert colour chanels.
invertImage = cv2.bitwise_not(readImage)

#Crop-dimensions to extract the four player names from inverted image.
cropName_1 = invertImage[428:478,683:970]
cropName_2 = invertImage[645:700,683:970]
cropName_3 = invertImage[869:918,683:970]
cropName_4 = invertImage[1086:1136,683:970]

#Global Crop width for wealth except first value.
wStart = 2085
wEnd = 2225

#Global variables for threshold value.
tn = 25
tw = 28

#Crop dimensions for four player wealths.
cropWealth_1 = invertImage[360:430,2065:wEnd]
cropWealth_2 = invertImage[570:655,wStart:wEnd]
cropWealth_3 = invertImage[790:870,wStart:wEnd]
cropWealth_4 = invertImage[1010:1100,wStart:wEnd]


#Change threshhold for names.
retval, thresholdName_1 = cv2.threshold(cropName_1,tn,255,cv2.THRESH_BINARY)
retval, thresholdName_2 = cv2.threshold(cropName_2,tn,255,cv2.THRESH_BINARY)
retval, thresholdName_3 = cv2.threshold(cropName_3,tn,255,cv2.THRESH_BINARY)
retval, thresholdName_4 = cv2.threshold(cropName_4,tn,255,cv2.THRESH_BINARY)

#Change threshhold for wealth.
retval, thresholdWealth_1 = cv2.threshold(cropWealth_1,tw,255,cv2.THRESH_BINARY)
retval, thresholdWealth_2 = cv2.threshold(cropWealth_2,tw,255,cv2.THRESH_BINARY)
retval, thresholdWealth_3 = cv2.threshold(cropWealth_3,tw,255,cv2.THRESH_BINARY)
retval, thresholdWealth_4 = cv2.threshold(cropWealth_4,tw,255,cv2.THRESH_BINARY)

#Write edited images for preview.
"""
cv2.imwrite("w1.jpg",thresholdWealth_1)
cv2.imwrite("w2.jpg",thresholdWealth_2)
cv2.imwrite("w3.jpg",thresholdWealth_3)
cv2.imwrite("w4.jpg",thresholdWealth_4)
"""

name_1 = pytesseract.image_to_string(thresholdName_1)
name_2 = pytesseract.image_to_string(thresholdName_2)
name_3 = pytesseract.image_to_string(thresholdName_3)
name_4 = pytesseract.image_to_string(thresholdName_4)

#Force pytesseract to read numbers using the pre-config 'outputbase digits'.
custom_config = r'--oem 3 --psm 6 outputbase digits'

wealth_1 = pytesseract.image_to_string(thresholdWealth_1, config=custom_config)
wealth_2 = pytesseract.image_to_string(thresholdWealth_2, config=custom_config)
wealth_3 = pytesseract.image_to_string(thresholdWealth_3, config=custom_config)
wealth_4 = pytesseract.image_to_string(thresholdWealth_4, config=custom_config)

#Manual correction for misread -ve sign.
wealth_1 = int(wealth_1)
wealth_2 = -abs(int(wealth_2))
wealth_3 = -abs(int(wealth_3))
wealth_4 = -abs(int(wealth_4))

#Add read data to csv.
data = pd.read_csv(dataCSV)
names = ["Game No",name_1,name_2,name_3,name_4]
wealths = [(len(data["Game No"])+1),wealth_1,wealth_2,wealth_3,wealth_4]
ocrData = pd.DataFrame([wealths],columns=names)
mergedData_wealth = pd.concat([data, ocrData], join = "outer")
mergedData_wealth.to_csv(dataCSV, index=False)

#Add ranks to csv.
data_r = pd.read_csv(rankCSV)

rank_1 = 1
rank_2 = 2
rank_3 = 3
rank_4 = 4

ranks = [(len(data_r["Game No"])+1),rank_1,rank_2,rank_3,rank_4]
ocrRank = pd.DataFrame([ranks],columns=names)
mergedData_rank = pd.concat([data_r, ocrRank], join = "outer")
mergedData_rank.to_csv(rankCSV, index=False)

#Calculate wins and win-ratio
data_r.heads
print("Run complete")
