import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder #per codificare stringhe
import numpy as np
from prettytable import PrettyTable

filename = "archive/seriea-matches.csv"
dataset = pd.read_csv(filename)

features = dataset.columns.tolist()

features_to_delete = []
features_to_delete.append(features[3]) # stringa comp prima inserita
features_to_delete.append(features[14]) 
for i in range(31, len(features) - 1):
    features_to_delete.append(features[i]) #stringhe che non ci interessano (features)


del features[3]
del features[14]
del features[31:48]

# nel drop possiamo dargli sia il vettore di indici che il vettore di stringhe, si mangia tutto
dataset = dataset.drop(features_to_delete, axis = 1)

#andiamo ad eliminare tutti i valori null (ne rimanevano solamente 3 nella colonna "dist")
dataset = dataset[dataset.isnull().sum(axis=1) == 0]

#preprocessing delle features stringhe in intero 
X_referee = list(range(1, 62))
referees = set(dataset['referee'])
dic_referees = dict(zip(referees, X_referee))

X_date = list(range(1, 551))
dates = set(dataset['date'])
date_list = list(dates)
ordered_date_set = sorted(date_list) # ho ordinato il set di date in ordine crescente (dal 2017 al 2022)
dic_dates = dict(zip(ordered_date_set, X_date)) # e poi codifico ogni data con un valore intero, ora so che 3 è una data più avanti cronologicamente di 2
key = dic_dates['2021-05-22']
#print(key)

X_time = list(range(1, 25))
time = set(dataset['time'])
dic_time = dict(zip(time, X_time))

X_round = list(range(1, 39))
rounds = set(dataset['round'])
dic_rounds = dict(zip(rounds, X_round))

X_day = list(range(1,8))
days = set(dataset['day'])
dic_days = dict(zip(days, X_day))

X_venue = list(range(1,3))
venues = set(dataset['venue'])
dic_venues = dict(zip(venues, X_venue))

X_result = list(range(1,4))
results = set(dataset['result'])
dic_results = dict(zip(results, X_result))

X_opponent = list(range(1,29))
opponents = set(dataset['opponent'])
dic_opponents = dict(zip(opponents, X_opponent))

X_captain = list(range(1, 225))
captains = set(dataset['captain'])
dic_captains = dict(zip(captains, X_captain))

X_formation = list(range(1,32))
formations = set(dataset['formation'])
dic_formations = dict(zip(formations, X_formation))

X_team = list(range(1,29))
teams = set(dataset['team'])
dic_teams = dict(zip(teams, X_team))

'''
#decodifica del valore numerico a stringa
for tupla in dic_referees:
  for numero in tupla:
    if isinstance(numero, int) or isinstance(numero, float):
      referees_encoded.append(numero)

referee_name = label_encoder.inverse_transform([referees_encoded[0]])
print(referee_name)

# filtro le partite comprese tra due date
data_inizio = pd.to_datetime('2021-05-22')
data_fine = pd.to_datetime('2021-05-23')
dataset['date'] = pd.to_datetime(dataset['date']) # converto la colonna date in formato datetime per permettere di filtrare su quel tipo di dato
time_ordered = dataset.loc[dataset['date'].between(data_inizio, data_fine)] # disordinati ma in quel range
time_ordered = time_ordered.sort_values(by='date', ascending=False) # in ordine decr

# prettytable fa visualizzare il dataframe allineato
table = PrettyTable()
table = time_ordered
print("rows: ", len(table))
print(table.to_string(max_rows=None))
'''

# qua andiamo a sostituire gli elementi che sono rappresentati come stringhe dentro il dataset con i valori dei rispettivi dizionari tramite la funzione di libreria "map"
dataset["referee"] = dataset["referee"].map(dic_referees)
dataset["date"] = dataset["date"].map(dic_dates)
dataset["time"] = dataset["time"].map(dic_time)
dataset["round"] = dataset["round"].map(dic_rounds)
dataset["day"] = dataset["day"].map(dic_days)
dataset["venue"] = dataset["venue"].map(dic_venues)
dataset["result"] = dataset["result"].map(dic_results)
dataset["opponent"] = dataset["opponent"].map(dic_opponents)
dataset["captain"] = dataset["captain"].map(dic_captains)
dataset["formation"] = dataset["formation"].map(dic_formations)
dataset["team"] = dataset["team"].map(dic_teams)
dataset = dataset.rename(columns={"Unnamed: 0": 0, "date": 1, "time": 2, "round": 3, "day": 4, "venue": 5, "result": 6, "gf": 7, "ga": 8, "opponent": 9, "xg": 10, "xga": 11, "poss_x": 12,
                                  "captain": 13, "formation": 14, "referee": 15, "sh": 16, "sot": 17, "dist": 18, "fk": 19, "pk": 20, "pkatt": 21,  "poss_y": 22, "touches": 23, 
                                  "def pen": 24, "def 3rd": 25, "mid 3rd": 26, "att 3rd": 27, "att pen": 28, "team": 29})

# droppiamo result perché nella x andiamo a mettere tutti i dati senza risultati, mentre nella y andiamo a mettere solo i risultati (X e y sono cloni del dataset)
np.X = dataset.drop(columns=[6])
np.y = dataset[6]
features.remove('attendance')

# problema di classificazione, creiamo un oggetto RandomForestClassifier
model = RandomForestClassifier(n_estimators = 50, min_samples_split = 10, random_state = 1)

#devo mettere in X_train tutti i valori codificati relativi alle partite prima del '2021-05-23' (alleniamo 4 anni di partenza e ci riserviamo 1/5 di dataset per il test)
dataset2 = dataset # clono il dataset senza la colonna result
X = dataset2.loc[dataset2[1] <= 430]
X_train = X.drop(6, axis = 1) # prendo tutti i games prima della data 430
X_train = X.loc[:, [29, 9, 1, 3, 15, 5, 2, 14]]
y_train = X.iloc[:, 6]

# [!] spostare la colonna 5(result) come ultima colonna per comodità
X = dataset2.loc[dataset2[1] > 430] # prendo tutti i games successivi alla data 430
X_test = X.drop(6, axis = 1)
colonne_da_modificare = [0, 4, 7, 8, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
X_test[colonne_da_modificare] = X_test[colonne_da_modificare].fillna(0)
X_test = X.loc[:, [29, 9, 1, 3, 15, 5, 2, 14]]
y_test = X.iloc[:, 6]

model.fit(X_train, y_train) # alleno il modello dandogli X e i result di X per ottenere un modello in grado di darci risposte

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(accuracy)
