import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import dataset as ds
#from pyswip import Prolog

# Inizializza l'interprete Prolog
#prolog = Prolog()

# Carica il file Prolog
#prolog.consult("rules.pl")

def search_String(dictionary, string):
    for key, value in dictionary.items():
        if string == key:
            return value
    return None  # Restituisce None se la stringa non è presente nel dizionario

def search_Value(dictionary, number):
    for key, value in dictionary.items():
        if value == number:
            return key
    return None  # Restituisce None se il numero non è presente nel dizionario

# metodo che prende in input la stringa di input che servirà come input al modello
def get_input():
    user_input = []
    i = 0
    for i in range(7):
        user_data = ""
        exit = True

        # squadra principale
        if i==0:
            while exit:
                user_data = input("Inserisci una squadra di Serie A: ")
                if search_String(dictionaries[i], user_data) != None:
                    print("Input corretto")
                    exit = False
                else:
                    print("[!] È necessario inserire un nome valido")

        # squadra avversaria
        if i==1:
            while exit:
                user_data = input("Inserisci la squadra avversaria: ")
                if search_String(dictionaries[i], user_data) != None:
                    print("Input corretto")
                    exit = False
                else:
                    print("[!] È necessario inserire un nome valido")

        # giornata del campionato
        if i==2:
            while exit:
                user_data = input("Inserisci a che giornata si gioca la partita: ")
                if search_String(dictionaries[i], "Matchweek " + str(user_data)) != None:
                    user_data = "Matchweek " + str(user_data)
                    print("Input corretto")
                    exit = False
                else:
                    print("La giornata deve essere un numero compreso in [1, 38]")

        # arbitro della partita    
        if i==3:
            while exit:
                user_data = input("Inserisci l'arbitro: ")
                if search_String(dictionaries[i], user_data) != None:
                    print("Input corretto")
                    exit = False
                else:
                    print("[!] È necessario inserire un cognome valido")

        # dove gioca la squadra principale, casa o trasferta
        if i==4:
            while exit:
                user_data = input("Inserisci dove giocherà la prima squadra (Casa/Trasferta): ")
                if user_data == "Casa" or user_data == "casa":
                    print("Input corretto")
                    user_data = "Home"
                    exit = False
                elif user_data == "Trasferta" or user_data == "trasferta":
                    print("Input corretto")
                    user_data = "Away"
                    exit = False
                else:
                    print("[!] È necessario scegliere solo tra \"Casa\" o \"Trasferta\"")
        
        # ora della partita
        if i==5:
            while exit:
                user_data = input("Inserisci l'orario in cui si gioca la partita (nel formato hh:mm): ")
                if search_String(dictionaries[i], user_data) != None:
                    print("Input corretto")
                    exit = False
                else:
                    print("[!] Hai inserito un orario inesistente o in un formato errato (deve essere hh:mm)")
        
        # formazione della squadra principale
        if i==6:
            while exit:
                user_data=input("Inserisci la formazione della prima squadra (nel formato n-n-n o n-n-n-n): ")
                if search_String(dictionaries[i], user_data) != None:
                    print("Input corretto")
                    exit = False
                else:
                    print("[!] Formazione non valida")
        
        # converte il dato che stiamo maneggiando e lo aggiunge alla lista
        user_data = search_String(dictionaries[i], user_data)
        user_input.append(user_data)

    return user_input

# problema di classificazione, creiamo un oggetto RandomForestClassifier
model = RandomForestClassifier(n_estimators = 50, min_samples_split = 10, random_state = 1)

# devo mettere in X_train tutti i valori codificati relativi alle partite prima del '2021-05-23' (alleniamo 4 anni di partenza e ci riserviamo 1/5 di dataset per il test)
dataset = ds.create_dataset() # creo il dataset "pulito"
dictionaries = ds.generate_dictionary(dataset) # creo i dizionari
dataset = ds.create_data_frame(dataset, dictionaries) # creo il dataset mappato
X = dataset.loc[dataset[1] <= 430]
X_train = X.drop(6, axis = 1) # prendo tutti i games prima della data 430 (escluso result chiaramente)
X_train = X.loc[:, [29, 9, 3, 15, 5, 2, 14]]
y_train = X.iloc[:, 6]

# [!] spostare la colonna 5(result) come ultima colonna per comodità
X = dataset.loc[dataset[1] > 430] # prendo tutti i games successivi alla data 430
X_test = X.drop(6, axis = 1)
columns_to_modify = [0, 4, 7, 8, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
X_test[columns_to_modify] = X_test[columns_to_modify].fillna(0)
X_test = X.loc[:, [29, 9, 3, 15, 5, 2, 14]]
y_test = X.iloc[:, 6]

model.fit(X_train, y_train) # alleno il modello dandogli X e i result di X per ottenere un modello in grado di darci risposte

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print("Precisione del modello: ", accuracy)

game = get_input()

print("Dizionari:\n", dictionaries)

# cerchiamo quante W,D,L hanno le due squadre inserite e ne calcoliamo le percentuali
# 190<= w + d + l >0
wins_team1 = 0
draw_team1 = 0
loss_team1 = 0
for index, row in dataset.iterrows(): # itera sulle righe (index) e le colonne (rows) alle quali ci si può riferire con il nome
    if row[29] == game[0]: # 29 è il nome della colonna dei team, cioè la prima squadra che diamo in input
        if row[6] == search_String(dictionaries[7], "W"): # 6 è il nome della colonna dei result
            wins_team1 += 1
        elif row[6] == search_String(dictionaries[7], "L"):
            loss_team1 += 1
        else:
            draw_team1 += 1

#stampiamo in risultati raccolti, le percentuali sono calcolate al momento evitando di creare variabili in più
print("Vittorie: ", wins_team1, "\nSconfitte: ", loss_team1, "\nPareggi: ", draw_team1)
print("% Vittorie: ", wins_team1 / (wins_team1+loss_team1+draw_team1), "\n% Sconfitte: ", loss_team1 / (wins_team1+loss_team1+draw_team1), "\n% Pareggi: ", draw_team1 / (wins_team1+loss_team1+draw_team1))

gameind = [29, 9, 3, 15, 5, 2, 14]

gamedict = {column: value for column, value in zip(gameind, game)}

game_2_pred = pd.DataFrame([gamedict])

print("Valori di game inseriti dal utente(mappati):\n", game)
print("Gamedict:\n", gamedict)
print("Dataframe:\n", game_2_pred)

predicted = model.predict(game_2_pred)
print("Predizione: ", predicted, "=", search_Value(dictionaries[7], predicted))