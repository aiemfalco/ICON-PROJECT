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
for i in range(31, len(features) - 1):
    features_to_delete.append(features[i]) #stringhe che non ci interessano (features)


del features[3]
del features[31:48]

print("Features che vogliamo mantenere: ", features)
print("Features da rimuovere: ", features_to_delete)
print("\n\n")

# nel drop possiamo dargli sia il vettore di indici che il vettore di stringhe, si mangia tutto
dataset = dataset.drop(features_to_delete, axis = 1)

#11.03
#preprocessing delle features stringhe in intero 
X_referee = list(range(1, 62))
referees = set(dataset['referee'])

dic_referees = list(zip(referees, X_referee)) #dizionario arbitro-valore intero
print("\nDictionary of referees: ")
print(dic_referees)

label_encoder = LabelEncoder()
referees_encoded = [] #vettore vuoto 

for tupla in dic_referees:
  for numero in tupla:
    if isinstance(numero, int) or isinstance(numero, float):
      referees_encoded.append(numero)

print("\n Lista codificata: ", referees_encoded)
print(len(referees_encoded)) 
'''
referee_name = label_encoder.inverse_transform([referees_encoded[0]])
print(referee_name)

X = dataset.drop(columns=['result'])
y = dataset['result']
# problema di classificazione, creiamo un oggetto RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, 0,2)
print(X_test)

model.fit(X_train, y_train)
predictions = model.predict(X_test)
print(predictions)

accuracy = accuracy_score(y_test, predictions)

print(accuracy)
'''