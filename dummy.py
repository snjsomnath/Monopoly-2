import glob
import os
import pandas as pd
import sys


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
