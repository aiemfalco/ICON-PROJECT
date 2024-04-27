import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder #per codificare stringhe
from pyswip import Prolog
import numpy as np
import dataset as ds

# Inizializza l'interprete Prolog
prolog = Prolog()

# Carica il file Prolog
prolog.consult("rules.pl")

# Definisci una funzione Python per verificare se un numero è valido (per la formazione)
def is_a_valid_number(numero):
    return bool(list(prolog.query(f"is_a_valid_number({numero})")))

def is_a_valid_round(numero):
    return bool(list(prolog.query(f"is_a_valid_round({numero})")))

def valid_time(ora, minuti):
    return bool(list(prolog.query(f"valid_time({ora}, {minuti})")))

# metodo che prende in input la stringa di input che servirà come input al modello
def get_input():
    user_input = []
    i = 0
    for i in range(8):
        datoutente = ""
        exit = True
        if i==0:
            while exit:
                datoutente = input("Inserisci una data nel formato gg/aaamm/a: ")
                if len(datoutente) == 10 and datoutente[:2].isdigit() and datoutente[3:5].isdigit() and datoutente[6:].isdigit() and datoutente[2] == '/' and datoutente[5] == '/':
                    print("Input corretto")
                    exit = False
                else:
                 print("[!] La data deve essere in formato gg/mm/aaaa")

        if i==1:
            while exit:
                datoutente = input("Inserisci l'orario in cui si gioca la partita (nel formato hh:mm): ")
                if len(datoutente) == 5 and datoutente[:2].isdigit() and datoutente[3:].isdigit() and datoutente[2] == ':':
                    hour_indexes = [0, 1]
                    min_indexes = [3, 4]
                    ora = ''.join(map(str, [datoutente[i] for i in hour_indexes]))
                    minuti = ''.join(map(str, [datoutente[i] for i in min_indexes]))
                    print(ora, minuti)
                    if(valid_time(ora, minuti)):
                        print("Input corretto") 
                        exit = False
                    else:
                        print("[!] Hai inserito un orario inesistente")
                else:
                    print("[!] L'ora deve essere in formato hh:mm")

        if i==2:
            while exit:
                datoutente = input("Inserisci la giornata: ")
                if len(datoutente) > 0 and len(datoutente) < 3 and is_a_valid_round(datoutente):
                    print("Input corretto")
                    exit = False
                else:
                    print("La giornata deve essere un numero compreso in [1, 38]")

        if i==3:
            while exit:
                datoutente = input("Inserisci il nome dello stadio in cui si giocherà la partita: ")
                if len(datoutente) > 1:
                    print("Input corretto")
                    exit = False
                else:
                    print("[!] È necessario inserire un nome")

        if i==4:
            while exit:
                datoutente=input("Inserisci la squadra che gioca in casa: ")
                if len(datoutente) > 1:
                    print("Input corretto")
                    exit = False
                else:
                    print("[!] È necessario inserire un nome")

        if i==5:
            while exit:
                datoutente=input("Inserisci la formazione (nel formato n-n-n o n-n-n-n): ")
                if (len(datoutente) == 5 and datoutente[0].isdigit() and datoutente[2].isdigit() and datoutente[4].isdigit() and datoutente[1]=='-' and datoutente[3]=='-' and is_a_valid_number(datoutente[0]) and is_a_valid_number(datoutente[2]) and is_a_valid_number(datoutente[4])) or (len(datoutente) == 7 and datoutente[0].isdigit() and datoutente[2].isdigit() and datoutente[4].isdigit() and datoutente[6].isdigit() and datoutente[1]=='-' and datoutente[3]=='-' and datoutente[5]=='-' and is_a_valid_number(datoutente[0]) and is_a_valid_number(datoutente[2]) and is_a_valid_number(datoutente[4]) and is_a_valid_number(datoutente[6])):
                    print("Input corretto")
                    exit = False
                else:
                    print("[!] Valori non accettati")
        
        if i==6:
            while exit:
                datoutente=input("Inserisci l'arbitro: ")
                if len(datoutente) > 1:
                    print("Input corretto")
                    exit = False
                else:
                    print("[!] È necessario inserire un nome")
        
        if i==7:
            while exit:
                datoutente=input("Inserisci la squadra che gioca in trasferta: ")
                if len(datoutente) > 1:
                    print("Input corretto")
                    exit = False
                else:
                    print("[!] È necessario inserire un nome")
        user_input.append(datoutente)
    return user_input

# problema di classificazione, creiamo un oggetto RandomForestClassifier
model = RandomForestClassifier(n_estimators = 50, min_samples_split = 10, random_state = 1)

#devo mettere in X_train tutti i valori codificati relativi alle partite prima del '2021-05-23' (alleniamo 4 anni di partenza e ci riserviamo 1/5 di dataset per il test)
dataset = ds.create_data_frame() # clono il dataset senza la colonna result
X = dataset.loc[dataset[1] <= 430]
X_train = X.drop(6, axis = 1) # prendo tutti i games prima della data 430
X_train = X.loc[:, [29, 9, 1, 3, 15, 5, 2, 14]]
y_train = X.iloc[:, 6]

# [!] spostare la colonna 5(result) come ultima colonna per comodità
X = dataset.loc[dataset[1] > 430] # prendo tutti i games successivi alla data 430
X_test = X.drop(6, axis = 1)
colonne_da_modificare = [0, 4, 7, 8, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
X_test[colonne_da_modificare] = X_test[colonne_da_modificare].fillna(0)
X_test = X.loc[:, [29, 9, 1, 3, 15, 5, 2, 14]]
y_test = X.iloc[:, 6]

model.fit(X_train, y_train) # alleno il modello dandogli X e i result di X per ottenere un modello in grado di darci risposte

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(accuracy)


# Fai una query a Prolog per trovare tutte le partite future
result = list(prolog.query("print_current_date"))
if result:
    print("Current date:", result[0])
else:
    print("Failed to get current date")

data_corrente = result[0]

game = get_input()
print(game)
# spezziamo la data del game in anno-mese-giorno e diamo questi tre valori come input al predicato partita futura e faremo il controllo sulla data

# test per capire se funzione la regola prolog (la partita P è una partita futura?)
result = bool(prolog.query("partita_futura(game)"))
if result:
    print(result)
else:
    print("Non ho niente")