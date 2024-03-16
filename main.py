import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder #per codificare stringhe

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


print("Features che vogliamo mantenere: ", features)
print("Features da rimuovere: ", features_to_delete)
print("\n\n")

# nel drop possiamo dargli sia il vettore di indici che il vettore di stringhe, si mangia tutto
dataset = dataset.drop(features_to_delete, axis = 1)

#andiamo ad eliminare tutti i valori null (ne rimanevano solamente 3 nella colonna "dist")
dataset = dataset[dataset.isnull().sum(axis=1) == 0]
  

#11.03
#preprocessing delle features stringhe in intero 
X_referee = list(range(1, 62))
referees = set(dataset['referee'])
dic_referees = dict(zip(referees, X_referee))

X_date = list(range(1, 551))
dates = set(dataset['date'])
dic_dates = dict(zip(dates, X_date))

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
for tupla in dic_referees:
  for numero in tupla:
    if isinstance(numero, int) or isinstance(numero, float):
      referees_encoded.append(numero)

referee_name = label_encoder.inverse_transform([referees_encoded[0]])
print(referee_name)

'''

# qua andiamo a sostituire gli elementi che sono rappresentati come stringhe dentro il dataset con le chiavi dei rispettivi dizionari tramite la funzione di libreria "map"

dataset["referee"] = dataset["referee"].map(dic_referees)
dataset["date"] = dataset["date"].map(dic_dates)
dataset["round"] = dataset["round"].map(dic_rounds)
dataset["day"] = dataset["day"].map(dic_days)
dataset["venue"] = dataset["venue"].map(dic_venues)
dataset["result"] = dataset["result"].map(dic_results)
dataset["opponent"] = dataset["opponent"].map(dic_opponents)
dataset["captain"] = dataset["captain"].map(dic_captains)
dataset["formation"] = dataset["formation"].map(dic_formations)
dataset["team"] = dataset["team"].map(dic_teams)


# droppiamo result perché nella x andiamo a mettere tutti i dati senza risultati, mentre nella y andiamo a mettere solo i risultati (x e y sono cloni del dataset)
X = dataset.drop(columns=['result'])
y = dataset['result']

# problema di classificazione, creiamo un oggetto RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)

# qui andiamo a splittare i dataset in 4 (2) parti ossia l'x training e test e l'y training e test
X_train, X_test, y_train, y_test = train_test_split(X, y, 0,2)
print(X_test)

'''
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print(predictions)

accuracy = accuracy_score(y_test, predictions)

print(accuracy)
'''