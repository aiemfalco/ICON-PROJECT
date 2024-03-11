import pandas as pd

filename = "archive/seriea-matches.csv"
dataset = pd.read_csv(filename)

features = dataset.columns.tolist()

features_to_delete = []
features_to_delete.append(features[3]) # stringa comp prima inserita
for i in range(31, len(features)):
    features_to_delete.append(features[i]) #stringhe che non ci interessano (features)


del features[3]
del features[31:50]

print("Features che vogliamo mantenere: ", features)
print("Features da rimuovere: ", features_to_delete)
print("\n\n")

# nel drop possiamo dargli sia il vettore di indici che il vettore di stringhe, si mangia tutto
dataset = dataset.drop(features_to_delete, axis = 1) # assegnare il risultato di drop a dataset!!!

print(dataset)