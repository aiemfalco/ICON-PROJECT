import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
#from pyswip import Prolog
import dataset as ds
from datetime import datetime

# Inizializza l'interprete Prolog
#prolog = Prolog()

# Carica il file Prolog
#prolog.consult("rules.pl")

def cerca_stringa_in_dizionario(dizionario, stringa):
    for chiave, valore in dizionario.items():
        if stringa in chiave:
            return valore
    return None  # Se la stringa non è stata trovata in nessun valore del dizionario

def cerca_numero_in_dizionario(dizionario, numero):
    for chiave, valore in dizionario.items():
        if valore == numero:
            return chiave
    return None  # Restituisce None se il numero non è presente nel dizionario

# metodo che prende in input la stringa di input che servirà come input al modello
# game(casa, trasferta, giornata, arbitro, stadio, ora, formazione)
def get_input():
    user_input = []
    i = 0
    for i in range(7):
        datoutente = ""
        exit = True
        if i==0:
            while exit:
                datoutente=input("Inserisci una squadra di Serie A: ")
                if cerca_stringa_in_dizionario(dizionari[i], datoutente) != None:
                    print("Input corretto")
                    exit = False
                else:
                    print("[!] È necessario inserire un nome valido")

        if i==1:
            while exit:
                datoutente=input("Inserisci la squadra avversaria: ")
                if cerca_stringa_in_dizionario(dizionari[i], datoutente) != None:
                    print("Input corretto")
                    exit = False
                else:
                    print("[!] È necessario inserire un nome valido")

        if i==2:
            while exit:
                datoutente = input("Inserisci a che giornata si gioca la partita: ")
                if cerca_stringa_in_dizionario(dizionari[i], datoutente) != None and datoutente != "0":
                    print("Input corretto")
                    exit = False
                else:
                    print("La giornata deve essere un numero compreso in [1, 38]")
            
        if i==3:
            while exit:
                datoutente=input("Inserisci l'arbitro: ")
                if cerca_stringa_in_dizionario(dizionari[i], datoutente) != None:
                    print("Input corretto")
                    exit = False
                else:
                    print("[!] È necessario inserire un nome valido")

        if i==4:
            while exit:
                datoutente = input("Inserisci dove giocherà la prima squadra (Casa/Trasferta): ")
                if datoutente == "Casa" or datoutente == "casa":
                    print("Input corretto")
                    datoutente = "Home"
                    exit = False
                elif datoutente == "Trasferta" or datoutente == "trasferta":
                    print("Input corretto")
                    datoutente = "Away"
                    exit = False
                else:
                    print("[!] È necessario scegliere solo tra \"Casa\" o \"Trasferta\"")
        
        if i==5:
            while exit:
                datoutente = input("Inserisci l'orario in cui si gioca la partita (nel formato hh:mm): ")
                if cerca_stringa_in_dizionario(dizionari[i], datoutente) != None and len(datoutente) > 4:
                    print("Input corretto") 
                    exit = False
                else:
                    print("[!] Hai inserito un orario inesistente o in un formato errato (deve essere hh:mm)")
        
        if i==6:
            while exit:
                datoutente=input("Inserisci la formazione della prima squadra (nel formato n-n-n o n-n-n-n): ")
                if cerca_stringa_in_dizionario(dizionari[i], datoutente) != None and len(datoutente) > 4:
                    print("Input corretto")
                    exit = False
                else:
                    print("[!] Formazione non valida")
            
        user_input.append(datoutente)
    return user_input

# problema di classificazione, creiamo un oggetto RandomForestClassifier
model = RandomForestClassifier(n_estimators = 50, min_samples_split = 10, random_state = 1)

# devo mettere in X_train tutti i valori codificati relativi alle partite prima del '2021-05-23' (alleniamo 4 anni di partenza e ci riserviamo 1/5 di dataset per il test)
dataset = ds.create_dataset() # creo il dataset "pulito"
dizionari = ds.generate_dictionary(dataset) # creo i dizionari
dataset = ds.create_data_frame(dataset, dizionari) # creo il dataset mappato
X = dataset.loc[dataset[1] <= 430]
X_train = X.drop(6, axis = 1) # prendo tutti i games prima della data 430 (escluso result chiaramente)
X_train = X.loc[:, [29, 9, 3, 15, 5, 2, 14]]
y_train = X.iloc[:, 6]

# [!] spostare la colonna 5(result) come ultima colonna per comodità
X = dataset.loc[dataset[1] > 430] # prendo tutti i games successivi alla data 430
X_test = X.drop(6, axis = 1)
colonne_da_modificare = [0, 4, 7, 8, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
X_test[colonne_da_modificare] = X_test[colonne_da_modificare].fillna(0)
X_test = X.loc[:, [29, 9, 3, 15, 5, 2, 14]]
y_test = X.iloc[:, 6]

model.fit(X_train, y_train) # alleno il modello dandogli X e i result di X per ottenere un modello in grado di darci risposte

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(accuracy)

current_date = datetime.now()

game = get_input()

print("pre game " , game)

# game(casa, trasferta, giornata, arbitro, stadio, ora, formazione)

print("dizionari:\n", dizionari)

for i in range(len(game)):
    game[i] = cerca_stringa_in_dizionario(dizionari[i], game[i])

print(game)

# cerchaimo quante W,D,L hanno le due squadre inserite
# 190<= w + d + l >0
wins_team1 = 0
draw_team1 = 0
loss_team1 = 0
for index, row in dataset.iterrows():
    if row[29] == game[0]:
        if row[6] == cerca_stringa_in_dizionario(dizionari[7], "W"):
            wins_team1 += 1
        elif row[6] == cerca_stringa_in_dizionario(dizionari[7], "L"):
            loss_team1 += 1
        else:
            draw_team1 += 1

'''
team1 = game[0]
teams_list = list(dataset[29])
results_list = list(dataset[6])
for i in range(len(teams_list)):
    if teams_list[i] == team1:
        if results_list[i] == 1:
            wins_team1 = wins_team1 + 1
        elif results_list[i] == 2:
            loss_team1 = loss_team1 + 1
        else:
            draw_team1 = draw_team1 + 1
'''

print("Wins: ", wins_team1, " Losses: ", loss_team1, " Draws: ", draw_team1)
print("% Wins: ", wins_team1 / (wins_team1+loss_team1+draw_team1), " % Losses: ", loss_team1 / (wins_team1+loss_team1+draw_team1), " % Draws: ", draw_team1 / (wins_team1+loss_team1+draw_team1))

gameind = [29, 9, 3, 15, 5, 2, 14]

gamedict = {colonna: valore for colonna, valore in zip(gameind, game)}

game_2_pred = pd.DataFrame([gamedict])

print("post game ", game)
print("gamedict ", gamedict)
print("dataframe ", game_2_pred)

predicted = model.predict(game_2_pred)
print("predizione: ", predicted, "=", cerca_numero_in_dizionario(dizionari[7], predicted))