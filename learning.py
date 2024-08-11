import pandas as pd
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
import dataset as ds
from skopt import BayesSearchCV
from skopt.space import Real, Categorical, Integer
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score
import seaborn as sns
import ontology as ot

'''
    Modulo riguardo l'apprendimento supervisionato
'''

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
def get_input(dictionaries):
    user_input = []
    i = 0
    for i in range(3):
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
        # dove gioca la squadra principale, casa o trasferta
        if i==2:
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
        # converte il dato che stiamo maneggiando e lo aggiunge alla lista
        user_data = search_String(dictionaries[i], user_data)
        user_input.append(user_data)

    return user_input

def pre_match_stats(dataset, game, dictionaries):
    # cerchiamo quante W,D,L hanno le due squadre inserite e ne calcoliamo le percentuali
    # 190<= w + d + l >0
    wins_team1 = 0
    draw_team1 = 0
    loss_team1 = 0
    wins_team2 = 0
    draw_team2 = 0
    loss_team2 = 0
    for index, row in dataset.iterrows(): # itera sulle righe (index) e le colonne (rows) alle quali ci si può riferire con il nome
        if row[22] == game[0]: # 22 è il nome della colonna dei team, cioè la prima squadra che diamo in input
            if row[3] == search_String(dictionaries[3], "W"): # 3 è il nome della colonna dei result
                wins_team1 += 1
            elif row[3] == search_String(dictionaries[3], "L"):
                loss_team1 += 1
            else:
                draw_team1 += 1
        if row[22] == game[1]: # 22 è il nome della colonna dei team, cioè la prima squadra che diamo in input
            if row[3] == search_String(dictionaries[3], "W"): # 3 è il nome della colonna dei result
                wins_team2 += 1
            elif row[3] == search_String(dictionaries[3], "L"):
                loss_team2 += 1
            else:
                draw_team2 += 1
    return wins_team1, draw_team1 , loss_team1, wins_team2, draw_team2, loss_team2

def create_gui(team1_win_percentage, team1_draw_percentage, team1_lose_percentage, team2_win_percentage, team2_draw_percentage, team2_lose_percentage, team1, team2):
    labels = ['Vittorie', 'Pareggi', 'Sconfitte']
    colors = ['green', 'blue', 'red']
    # Dati per il grafico a torta del team1
    sizes_team1 = [team1_win_percentage, team1_draw_percentage, team1_lose_percentage]

    # Dati per il grafico a torta del team2
    sizes_team2 = [team2_win_percentage, team2_draw_percentage, team2_lose_percentage]

    # Crea una figura e assicurati che abbia due sottografici uno accanto all'altro
    fig, axs = plt.subplots(1, 2)

    # Primo grafico a torta
    axs[0].pie(sizes_team1, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    axs[0].set_title('Dati ' + team1)

    # Secondo grafico a torta
    axs[1].pie(sizes_team2, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    axs[1].set_title('Dati ' + team2)

    plt.show()

def learner(ontology):
    # Problema di classificazione, creiamo un oggetto RandomForestClassifier e adaBoosting e alleniamo i modelli di apprendimento
    # base_estimator parte da un albero di profondità 1, quindi solo il root
    base_estimator = DecisionTreeClassifier(max_depth = 1)
    # i due modelli
    model_rf = RandomForestClassifier(n_estimators = 150, max_depth = 10, min_samples_split = 5, random_state = 1)
    model_ada = AdaBoostClassifier(n_estimators = 50, learning_rate = 1.0, random_state = 42, estimator = base_estimator)
    # prendiamo il dataset da csv "grezzo"
    dataset = ds.get_dataset()
    # gli aggiungiamo la nuova colonna ottenuta grazie all'ontologia
    dataset = ot.getNewColumn(ontology, dataset)

    # devo mettere in X_train tutti i valori codificati relativi alle partite prima del '2021-05-23' (alleniamo 4 anni di partenza e ci riserviamo 1/5 di dataset per il test)
    dataset = ds.refine_dataset(dataset) # creo il dataset "pulito" di features che non ci servono

    dictionaries = ds.generate_dictionary(dataset) # creo i dizionari
    dataset = ds.create_data_frame(dataset, dictionaries) # creo il dataset mappato
    X = dataset.loc[dataset[1] <= 440]
    X_train = X.drop(3, axis = 1) # prendo tutti i games prima della data 430 (escluso result chiaramente)
    X_train = X.drop(1, axis = 1) # droppo la colonna delle date che ci è servita solo come spartiacque
    X_train = X.loc[:, [22, 6, 2]]
    y_train = X.iloc[:, 3]

    X = dataset.loc[dataset[1] > 440] # prendo tutti i games successivi alla data 430
    X_test = X.drop(3, axis = 1)
    X_test = X.drop(1, axis = 1)
    columns_to_modify = [4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23]
    X_test[columns_to_modify] = X_test[columns_to_modify].fillna(0)
    X_test = X.loc[:, [22, 6, 2]]
    y_test = X.iloc[:, 3]

    # Questi sono i parametri per il random forest
    param_space_rf = {
    'n_estimators': Integer(50, 150),
    'max_depth': Integer(1, 20),
    'min_samples_split': Integer(2, 10)
    }
    
    # Questi sono i parametri per l'ada boost
    param_space_ada = {
    'n_estimators': (50, 500),  # Numero di estimatori deboli
    'learning_rate': (0.01, 1.0, 'log-uniform'),  # Learning rate
    'algorithm': ['SAMME', 'SAMME.R']  # Algoritmo di boosting
    }


    # Esecuzione della Bayesian Optimization per il random forest
    bayes_search_rf = BayesSearchCV(
        model_rf,
        param_space_rf, 
        n_iter=50,  # Numero di iterazioni della ricerca
        cv=5,  # Numero di fold della cross-validation
        scoring='accuracy',  # Metrica di valutazione da ottimizzare
        n_jobs=-1,
        random_state=1 #seed per riproducibilità
    )

    # Esecuzione della Bayesian Optimization per l'ada boost
    bayes_search_ada = BayesSearchCV(
        model_ada,
        param_space_ada,
        n_iter = 50,  # Numero di iterazioni della ricerca
        cv = 5,  # Numero di fold della cross-validation
        scoring = 'accuracy',  # Metrica di valutazione da ottimizzare
        n_jobs =- 1,
        random_state = 1  # Seed per riproducibilità
    )   


    bayes_search_rf.fit(X_train, y_train)

    bayes_search_ada.fit(X_train, y_train)

    # Estrazione dei migliori iperparametri
    best_params = bayes_search_rf.best_params_
    print("Migliori iperparametri per il random forest:", best_params)
    best_score = bayes_search_rf.best_score_
    print("Miglior risultato di accuracy per il random forest:", best_score)

    best_params_ada = bayes_search_ada.best_params_
    print("I migliori parametri trovati per l'ada boosting:", best_params_ada)
    best_score_ada = bayes_search_ada.best_score_
    print("Miglior risultato di accuracy per l'ada boosting:", best_score_ada)


    predictions_rf = bayes_search_rf.predict(X_test)
    predictions_ada = bayes_search_ada.predict(X_test)

    cm = confusion_matrix(y_test, predictions_rf)
    cm = confusion_matrix(y_test, predictions_ada)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, cmap='Blues', fmt='g', cbar=False)
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')
    plt.title('Confusion Matrix')
    plt.show()

    accuracy_rf = accuracy_score(y_test, predictions_rf)
    accuracy_ada = accuracy_score(y_test, predictions_ada)
    print("Accuratezza del modello per il random forest: ", accuracy_rf)
    print("Accuratezza del modello per l'ada boosting: ", accuracy_ada)

    precision_rf = precision_score(y_test, predictions_rf, average='macro')  # Puoi scegliere 'micro', 'macro' o 'weighted'
    precision_ada = precision_score(y_test, predictions_ada, average='macro', zero_division = 0)  # Puoi scegliere 'micro', 'macro' o 'weighted'
    print("Precision per il random forest:", precision_rf)
    print("Precision per l'ada boosting:", precision_ada)

    recall_rf = recall_score(y_test, predictions_rf, average='macro')  # Puoi scegliere 'micro', 'macro' o 'weighted'
    recall_ada = recall_score(y_test, predictions_ada, average='macro')  # Puoi scegliere 'micro', 'macro' o 'weighted'
    print("Recall per il random forest:", recall_rf)
    print("Recall per l'ada boosting:", recall_ada)

    f1_rf = f1_score(y_test, predictions_rf, average='macro')  # Puoi scegliere 'micro', 'macro' o 'weighted'
    f1_ada = f1_score(y_test, predictions_ada, average='macro')  # Puoi scegliere 'micro', 'macro' o 'weighted'
    print("F1-score per il random forest:", f1_rf)
    print("F1-score per l'ada boosting:", f1_ada)

    game = get_input(dictionaries)

    stats = pre_match_stats(dataset, game, dictionaries)

    team1_win_percentage = stats[0] / (stats[0]+stats[2]+stats[1])
    team1_draw_percentage = stats[1] / (stats[0]+stats[2]+stats[1])
    team1_lose_percentage = stats[2] / (stats[0]+stats[2]+stats[1])

    team2_win_percentage = stats[3] / (stats[3]+stats[4]+stats[5])
    team2_draw_percentage = stats[5] / (stats[3]+stats[4]+stats[5])
    team2_lose_percentage = stats[4] / (stats[3]+stats[4]+stats[5])

    #stampiamo in risultati raccolti, le percentuali sono calcolate al momento evitando di creare variabili in più
    print("Vittorie: ", stats[0], "\nSconfitte: ", stats[2], "\nPareggi: ", stats[1])
    print("% Vittorie: ", team1_win_percentage, "\n% Sconfitte: ", team1_lose_percentage, "\n% Pareggi: ", team1_draw_percentage)

    #dati della seconda squadra messa
    print("Vittorie: ", stats[3], "\nSconfitte: ", stats[4], "\nPareggi: ", stats[5])
    print("% Vittorie: ", team2_win_percentage, "\n% Sconfitte: ", team2_lose_percentage, "\n% Pareggi: ", team2_draw_percentage)
    gameind = [22, 6, 2]

    gamedict = {column: value for column, value in zip(gameind, game)}

    game_2_pred = pd.DataFrame([gamedict])


    predicted_rf = bayes_search_rf.predict(game_2_pred)
    predicted_ada = bayes_search_ada.predict(game_2_pred)
    prob_rf = bayes_search_rf.predict_proba(game_2_pred)
    prob_ada = bayes_search_ada.predict_proba(game_2_pred)
    print("Predizione RANDOM FOREST: ", predicted_rf, "=", search_Value(dictionaries[3], predicted_rf))
    print("Predizione ADABOOSTING: ", predicted_ada, "=", search_Value(dictionaries[3], predicted_ada))
    print(prob_rf)
    print(prob_ada)
    team1 = game[0]
    team1 = search_Value(dictionaries[0], team1)
    team2 = game[1]
    team2 = search_Value(dictionaries[1], team2)
    create_gui(team1_win_percentage, team1_draw_percentage, team1_lose_percentage, team2_win_percentage, team2_draw_percentage, team2_lose_percentage, team1, team2)