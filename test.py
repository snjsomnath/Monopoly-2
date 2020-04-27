import pytesseract
from PIL import Image
import cv2
import numpy as np
import sys
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import os

check = pd.read_csv("latest.csv")
latest_file = check.iloc[0,0]

def newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)
print(newest("resources"))
latest = pd.DataFrame([newest("resources")])
latest.to_csv(r"latest.csv",index = False)
if latest_file == newest("resources"):
    sys.exit('Item has been appended')

else:
    print("This will be appended")

file_path= newest("resources")
im = Image.open(file_path)
im.save("ocr.jpg", dpi=(300, 300))

#make image b&w
im = Image.open("ocr.jpg").convert("L")
im.save("ocr.jpg")

image = cv2.imread("ocr.jpg")

#invert colour chanels
invert = cv2.bitwise_not(image)

#Crop image to name boxes
#Crop dimensions for names
crop1 = invert[428:478,683:970]
crop2 = invert[645:700,683:970]
crop3 = invert[869:918,683:970]
crop4 = invert[1086:1136,683:970]


#Global Crop width for wealth except first value
#ww1 = 2067
#ww2 = 2198
ww1 = 2085
ww2 = 2225
#Global variables for threshold
tn = 25
tw = 28

#Crop image to number boxes
#Crop dimensions for Total Wealth
crop1a = invert[360:430,2065:ww2]
crop2a = invert[570:655,ww1:ww2]
crop3a = invert[790:870,ww1:ww2]
crop4a = invert[1010:1100,ww1:ww2]


#Threshhold for names
retval, threshold1 = cv2.threshold(crop1,tn,255,cv2.THRESH_BINARY)
retval, threshold2 = cv2.threshold(crop2,tn,255,cv2.THRESH_BINARY)
retval, threshold3 = cv2.threshold(crop3,tn,255,cv2.THRESH_BINARY)
retval, threshold4 = cv2.threshold(crop4,tn,255,cv2.THRESH_BINARY)

#Threshhold for Total wealth
retval, threshold1a = cv2.threshold(crop1a,tw,255,cv2.THRESH_BINARY)
retval, threshold2a = cv2.threshold(crop2a,tw,255,cv2.THRESH_BINARY)
retval, threshold3a = cv2.threshold(crop3a,tw,255,cv2.THRESH_BINARY)
retval, threshold4a = cv2.threshold(crop4a,tw,255,cv2.THRESH_BINARY)

cv2.imwrite("w1.jpg",threshold1a)
cv2.imwrite("w2.jpg",threshold2a)
cv2.imwrite("w3.jpg",threshold3a)
cv2.imwrite("w4.jpg",threshold4a)

name1 = pytesseract.image_to_string(threshold1)
name2 = pytesseract.image_to_string(threshold2)
name3 = pytesseract.image_to_string(threshold3)
name4 = pytesseract.image_to_string(threshold4)

custom_config = r'--oem 3 --psm 6 outputbase digits'
wealth1 = pytesseract.image_to_string(threshold1a, config=custom_config)
wealth2 = pytesseract.image_to_string(threshold2a, config=custom_config)
wealth3 = pytesseract.image_to_string(threshold3a, config=custom_config)
wealth4 = pytesseract.image_to_string(threshold4a, config=custom_config)

wealth1 = int(wealth1)
wealth2 = -abs(int(wealth2))
wealth3 = -abs(int(wealth3))
wealth4 = -abs(int(wealth4))

#add read data to csv
data = pd.read_csv("data.csv")
names = ["Game No",name1,name2,name3,name4]
wealths = [(len(data["Game No"])+1),wealth1,wealth2,wealth3,wealth4]

ocr = pd.DataFrame([wealths],columns=names)

merging = pd.concat([data, ocr], join = "outer")
print(merging)

merging.to_csv(r"data.csv", index=False)

#add ranks to csv
data_r = pd.read_csv("rank.csv")

rank1 = 1
rank2 = 2
rank3 = 3
rank4 = 4

wealths = [(len(data_r["Game No"])+1),rank1,rank2,rank3,rank4]

ocr = pd.DataFrame([wealths],columns=names)

merging = pd.concat([data_r, ocr], join = "outer")
print(merging)

merging.to_csv(r"rank.csv", index=False)

#dashboard stuff
df = pd.read_csv('data.csv')
df_rank = pd.read_csv("rank.csv")



print(name1,name2,name3,name4)
print(wealth1,wealth2,wealth3,wealth4)

            


#Read CSV and plot the chart
fig = make_subplots(
    rows=8, cols=3,
    specs=[[{}, {"rowspan": 2,"colspan": 2},None],
        [{}, None,None],
        [{}, None,None],
        [{}, None,None],
        [{}, None,None],
        [{}, None,None],
        [{}, None,None],
        [{}, None,None]],
    subplot_titles=("Sanjay","Rank tracking", "Thamar", "Abhishek", "Shishir","Nivin","Diraj","Nithin","Hrideek"))
fig.add_trace(
    go.Scatter(
    x=df['Game No'], 
    y=df['Sanjay'], name="Sanjay",line_shape='spline',connectgaps=True,showlegend=False),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(
    x=df['Game No'], 
    y=df['thamarmo'], name="Thamar",line_shape='spline',connectgaps=True,showlegend=False),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
    x=df['Game No'], 
    y=df['Abhishek'], name="Abhishek",line_shape='spline',connectgaps=True,showlegend=False),
    row=3, col=1
)

fig.add_trace(
    go.Scatter(
    x=df['Game No'], 
    y=df['Shishtaouk'], name="Shishir",line_shape='spline',connectgaps=True,showlegend=False),
    row=4, col=1
)

fig.add_trace(
    go.Scatter(
    x=df['Game No'], 
    y=df['NipPincher'], name="Nivin",line_shape='spline',connectgaps=True,showlegend=False),
    row=5, col=1
)

fig.add_trace(
    go.Scatter(
    x=df['Game No'], 
    y=df['Diraj'], name="Diraj",line_shape='spline',connectgaps=True,showlegend=False),
    row=6, col=1
)

fig.add_trace(
    go.Scatter(
    x=df['Game No'], 
    y=df['Nithin'], name="Nithin",line_shape='spline',connectgaps=True,showlegend=False),
    row=7, col=1
)

fig.add_trace(
    go.Scatter(
    x=df['Game No'], 
    y=df['Spartan'], name="Hrideek",line_shape='spline',connectgaps=True,showlegend=False),
    row=8, col=1
)

#Rank tracking
fig.add_trace(
    go.Scatter(
    x=df_rank['Game No'], 
    y=df_rank['Sanjay'], name='Sanjay',line_shape='spline',connectgaps=True),
    row=1,col=2
)
fig.add_trace(
    go.Scatter(
    x=df_rank['Game No'], 
    y=df_rank['thamarmo'], name = 'Thamar',line_shape='spline',connectgaps=True),
    row=1,col=2
)
fig.add_trace(
    go.Scatter(
    x=df_rank['Game No'], 
    y=df_rank['Abhishek'], name='Abhishek',line_shape='spline',connectgaps=True),
    row=1,col=2
)
fig.add_trace(
    go.Scatter(
    x=df_rank['Game No'], 
    y=df_rank['Shishtaouk'], name='Shishir',line_shape='spline',connectgaps=True),
    row=1,col=2
)
fig.add_trace(
    go.Scatter(
    x=df_rank['Game No'], 
    y=df_rank['NipPincher'], name = 'Nivin',line_shape='spline',connectgaps=True),
    row=1,col=2
)

fig.add_trace(
    go.Scatter(
    x=df_rank['Game No'], 
    y=df_rank['Diraj'], name = 'Diraj',line_shape='spline',connectgaps=True),
    row=1,col=2
)

fig.add_trace(
    go.Scatter(
    x=df_rank['Game No'], 
    y=df_rank['Nithin'], name = 'Nithin',line_shape='spline',connectgaps=True),
    row=1,col=2
)

fig.add_trace(
    go.Scatter(
    x=df_rank['Game No'], 
    y=df_rank['Spartan'], name='Hrideek',line_shape='spline',connectgaps=True),
    row=1,col=2
)


fig.update_layout(height=800, width=1024, title_text="Monopoly Tracking Dashboard")
fig.show()

