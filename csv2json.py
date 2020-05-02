import pandas as pd

data=pd.read_csv("data.csv")
data_r=pd.read_csv("rank.csv")
#csv to json
data_r.to_json(r"rank.json")
data.tojson (r"data.json")