import pandas as pd
import csv
rankCSV = "rank.csv"
players = ["Sanjay", "thamarmo", "Abhishek", "Shishtaouk", "NipPincher", "Diraj", "SugaDaddy", "Spartan"]
data_r = pd.read_csv(rankCSV)
winRatio = []
wins


for i in players:
    gamesPlayed= data_r[i].value_counts().sum()
    if 1 in data_r[i].unique():
        win = data_r[i].value_counts()[1]
        wr = ((win/gamesPlayed*100).round(2))
        winRatio.append(wr)
    else:
        winRatio.append(0)
print(winRatio)


