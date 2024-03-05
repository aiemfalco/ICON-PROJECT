import pandas as pd

filename = "archive/seriea-matches.csv"
dataset = pd.read_csv(filename)

#print(dataset)

features = dataset.columns.tolist()
del features[3]
del features[31:50]

print(features)

