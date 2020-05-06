import pandas as pd
import csv
rankCSV = "rank.csv"
players = ["Sanjay", "thamarmo", "Abhishek", "Shishtaouk", "NipPincher", "Diraj", "SugaDaddy", "Spartan"]
data_r = pd.read_csv(rankCSV)
winRatio = []
wins =[]
played = []
losses = []
lossRatio = []

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


