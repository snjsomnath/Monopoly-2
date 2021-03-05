# Monopoly OCR

An Open-CV project to create a dashboard for the monopoly game. 
A screenshot of the game results is added to the resources folder and the script runs an OCR using Open-CV and pyTesseract.  

![jpg](media/img_site.jpg)

Dashboard Site can be viewed [here](https://snjsomnath.github.io/Monopoly-2/)  

![jpg](media/GSHEET_01.jpg)
![jpg](media/GSHEET_01.jpg)

GSheets Dashboard can be viewed [here](https://snjsomnath.github.io/Monopoly-GoogleSheets-Dashboard/)

```python
import pytesseract
from PIL import Image
import cv2
import sys
import pandas as pd
import csv
import os

```

# 1 - Testing for latest files


```python
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
```


```python
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
```

    resources\Screenshot_20200702-173925 - Copy (2).jpg
    This will be appended
    

# 2 - Read latest file.


```python
file_path= newest("resources")
im = Image.open(file_path)
im.save("raw.jpg", dpi=(300, 300))
```


```python
im
```




    
![png](media/output_7_0.png)
    



# 3 - Pre-process images


```python
#Make image b&w.
im = Image.open("raw.jpg").convert("L")
im.save("bw.jpg")
readImage = cv2.imread("bw.jpg")

#Invert colour chanels.
invertImage = cv2.bitwise_not(readImage)
```


```python
im
```




    
![png](media/output_10_0.png)
    




```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(16, 8))
img2 = invertImage[:,:,::-1]
ax.imshow(img2)
```




    <matplotlib.image.AxesImage at 0x1b3623f4d88>




    
![png](media/output_11_1.png)
    


# 4 - Crop-dimensions to extract the four player names from inverted image.


```python
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
```


```python
cropList = [cropName_1,cropName_2,cropName_3,cropName_4]
def plotImages(list):
    w=10
    h=10
    fig=plt.figure(figsize=(8, 8))
    columns = 1
    rows = 4
    for i in range(1, columns*rows +1):
        img = list[i-1]
        fig.add_subplot(rows, columns, i)
        plt.imshow(img)
    plt.show()
plotImages(cropList)
```


    
![png](media/output_14_0.png)
    


# 5 - Crop dimensions for four player wealths.


```python
cropWealth_1 = invertImage[360:430,2065:wEnd]
cropWealth_2 = invertImage[570:655,wStart:wEnd]
cropWealth_3 = invertImage[790:870,wStart:wEnd]
cropWealth_4 = invertImage[1010:1100,wStart:wEnd]
```


```python
cropList = [cropWealth_1,cropWealth_2,cropWealth_3,cropWealth_4]
plotImages(cropList)
```


    
![png](media/output_17_0.png)
    


# 6 - Change threshhold for names.


```python
retval, thresholdName_1 = cv2.threshold(cropName_1,tn,255,cv2.THRESH_BINARY)
retval, thresholdName_2 = cv2.threshold(cropName_2,tn,255,cv2.THRESH_BINARY)
retval, thresholdName_3 = cv2.threshold(cropName_3,tn,255,cv2.THRESH_BINARY)
retval, thresholdName_4 = cv2.threshold(cropName_4,tn,255,cv2.THRESH_BINARY)

```


```python
cropList = [thresholdName_1,thresholdName_2,thresholdName_3,thresholdName_4]
plotImages(cropList)
```


    
![png](media/output_20_0.png)
    


# 7 - Change threshhold for wealth.


```python
retval, thresholdWealth_1 = cv2.threshold(cropWealth_1,tw,255,cv2.THRESH_BINARY)
retval, thresholdWealth_2 = cv2.threshold(cropWealth_2,tw,255,cv2.THRESH_BINARY)
retval, thresholdWealth_3 = cv2.threshold(cropWealth_3,tw,255,cv2.THRESH_BINARY)
retval, thresholdWealth_4 = cv2.threshold(cropWealth_4,tw,255,cv2.THRESH_BINARY)
```


```python
cropList = [thresholdWealth_1,thresholdWealth_2,thresholdWealth_3,thresholdWealth_4]
plotImages(cropList)
```


    
![png](media/output_23_0.png)
    


# 8 - Write edited images for preview.


```python
"""
cv2.imwrite("w1.jpg",thresholdWealth_1)
cv2.imwrite("w2.jpg",thresholdWealth_2)
cv2.imwrite("w3.jpg",thresholdWealth_3)
cv2.imwrite("w4.jpg",thresholdWealth_4)
"""
```




    '\ncv2.imwrite("w1.jpg",thresholdWealth_1)\ncv2.imwrite("w2.jpg",thresholdWealth_2)\ncv2.imwrite("w3.jpg",thresholdWealth_3)\ncv2.imwrite("w4.jpg",thresholdWealth_4)\n'




```python
name_1 = pytesseract.image_to_string(thresholdName_1)
name_2 = pytesseract.image_to_string(thresholdName_2)
name_3 = pytesseract.image_to_string(thresholdName_3)
name_4 = pytesseract.image_to_string(thresholdName_4)
```

# 9 - Force pytesseract to read numbers using the pre-config 'outputbase digits'.


```python
custom_config = r'--oem 3 --psm 6 outputbase digits'

wealth_1 = pytesseract.image_to_string(thresholdWealth_1, config=custom_config)
wealth_2 = pytesseract.image_to_string(thresholdWealth_2, config=custom_config)
wealth_3 = pytesseract.image_to_string(thresholdWealth_3, config=custom_config)
wealth_4 = pytesseract.image_to_string(thresholdWealth_4, config=custom_config)
```

# 10 - Manual correction for misread -ve sign.


```python

wealth_1 = int(wealth_1)
wealth_2 = -abs(int(wealth_2))
wealth_3 = -abs(int(wealth_3))
wealth_4 = -abs(int(wealth_4))
```

# 11 - Add read data and ranks to csv.


```python
#Add read data to csv.
data = pd.read_csv(dataCSV)
names = ["Game No",name_1,name_2,name_3,name_4]
wealths = [(len(data["Game No"])+1),wealth_1,wealth_2,wealth_3,wealth_4]
ocrData = pd.DataFrame([wealths],columns=names)
mergedData_wealth = pd.concat([data, ocrData], join = "outer")
mergedData_wealth.to_csv(dataCSV, index=False)

#Add ranks to csv.
data_r = pd.read_csv(rankCSV)
```


```python
rank_1 = 1
rank_2 = 2
rank_3 = 3
rank_4 = 4

ranks = [(len(data_r["Game No"])+1),rank_1,rank_2,rank_3,rank_4]
ocrRank = pd.DataFrame([ranks],columns=names)
mergedData_rank = pd.concat([data_r, ocrRank], join = "outer")
mergedData_rank.to_csv(rankCSV, index=False)
```

# 12 - Calculate wins and win-ratio


```python
#Calculate wins and win-ratio
players = ["Sanjay", "thamarmo", "Abhishek", "Shishtaouk", "NipPincher", "Diraj", "SugaDaddy", "Spartan"]
data_r = pd.read_csv(rankCSV)
winRatio = []
wins =[]
played = []
losses = []
```

# 13 - Check for new files and update tables


```python
for i in players:
    gamesPlayed= data_r[i].value_counts().sum()
    played.append(gamesPlayed)
    if 1 in data_r[i].unique():
        win = data_r[i].value_counts()[1]
        wins.append(win)
        wr = ((win/gamesPlayed*100).round(2))
        winRatio.append(wr)
    else:
        winRatio.append(0)
        wins.append(0)
for i in range(len(played)):
    losses.append(played[i]-wins[i])
winLoss = pd.DataFrame(list(zip(players, wins, played,losses,winRatio)), 
               columns =['Names', 'Wins', 'Played', 'Lost', 'winRatio'])
winLoss.to_csv(r'winLoss.csv', index = False) 

```


```python
winLoss
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Names</th>
      <th>Wins</th>
      <th>Played</th>
      <th>Lost</th>
      <th>winRatio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Sanjay</td>
      <td>25</td>
      <td>71</td>
      <td>46</td>
      <td>35.21</td>
    </tr>
    <tr>
      <th>1</th>
      <td>thamarmo</td>
      <td>5</td>
      <td>28</td>
      <td>23</td>
      <td>17.86</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Abhishek</td>
      <td>21</td>
      <td>78</td>
      <td>57</td>
      <td>26.92</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Shishtaouk</td>
      <td>3</td>
      <td>7</td>
      <td>4</td>
      <td>42.86</td>
    </tr>
    <tr>
      <th>4</th>
      <td>NipPincher</td>
      <td>6</td>
      <td>22</td>
      <td>16</td>
      <td>27.27</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Diraj</td>
      <td>3</td>
      <td>26</td>
      <td>23</td>
      <td>11.54</td>
    </tr>
    <tr>
      <th>6</th>
      <td>SugaDaddy</td>
      <td>14</td>
      <td>48</td>
      <td>34</td>
      <td>29.17</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Spartan</td>
      <td>13</td>
      <td>47</td>
      <td>34</td>
      <td>27.66</td>
    </tr>
  </tbody>
</table>
</div>


