import pandas as pd

def create_dataset():
    # carichiamo il dataset da csv
    filename = "archive/seriea-matches.csv"
    dataset = pd.read_csv(filename)

    features = dataset.columns.tolist()

    features_to_delete = []
    features_to_delete.append(features[0])
    features_to_delete.append(features[3]) # stringa comp prima inserita
    features_to_delete.append(features[14])
    features_to_delete.append(features[15])
    features_to_delete.append(features[16])
    features_to_delete.append(features[17])
    features_to_delete.append(features[21])
    for i in range(31, len(features) - 1):
        features_to_delete.append(features[i]) #stringhe che non ci interessano (features)

    # del features[3]
    # del features[14]
    # del features[15:18]
    # del features[31:48]

    # nel drop possiamo dargli sia il vettore di indici che il vettore di stringhe, si mangia tutto
    dataset = dataset.drop(features_to_delete, axis = 1)

    #andiamo ad eliminare tutti i valori null (ne rimanevano solamente 3 nella colonna "dist")
    dataset = dataset[dataset.isnull().sum(axis=1) == 0]

    # cambia la stringa "Internazionale" in "Inter" nella colonna "team", l'ultima
    for index, row in dataset.iterrows(): # itera sulle righe (index) e le colonne (rows) alle quali ci si può riferire con il nome
        if row["team"] == "Internazionale":
            dataset.at[index, "team"] = "Inter"
    
    """
    # rimuove tutti i nomi degli arbitri, lasciando solo i cognomi
    for index, row in dataset.iterrows(): # itera sulle righe (index) e le colonne (rows) alle quali ci si può riferire con il nome
        dataset.at[index, "referee"] = dataset.at[index, "referee"][dataset.at[index, "referee"].find(" ") + 1:]
    """
    
    return dataset

def generate_dictionary(dataset):

    #preprocessing delle features stringhe in intero
    '''
    X_referee = list(range(1, 62))
    referees = set(dataset['referee'])
    dic_referees = dict(zip(referees, X_referee))
    '''

    X_date = list(range(1, 551))
    dates = set(dataset['date'])
    print(len(dates))
    date_list = list(dates)
    ordered_date_set = sorted(date_list) # ho ordinato il set di date in ordine crescente (dal 2017 al 2022)
    dic_dates = dict(zip(ordered_date_set, X_date)) # e poi codifico ogni data con un valore intero, ora so che 3 è una data più avanti cronologicamente di 2

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

    X_team = list(range(1,29))
    teams = set(dataset['team'])
    dic_teams = dict(zip(teams, X_team))

    dic_opponents = dic_teams

    # game(casa, trasferta, giornata, arbitro, stadio, ora, formazione)

    return dic_teams, dic_opponents, dic_rounds, dic_venues, dic_time, dic_results, dic_dates, dic_days
    # return dic_teams, dic_opponents, dic_rounds, dic_referees, dic_venues, dic_time, dic_formations, dic_results, dic_dates, dic_days, dic_captains

def create_data_frame(dataset, dizionari):
    
    # qui andiamo a sostituire gli elementi che sono rappresentati come stringhe dentro il dataset con i valori dei rispettivi dizionari tramite la funzione di libreria "map"
    dataset["team"] = dataset["team"].map(dizionari[0])
    dataset["opponent"] = dataset["opponent"].map(dizionari[1])
    dataset["round"] = dataset["round"].map(dizionari[2])
    #dataset["referee"] = dataset["referee"].map(dizionari[3])
    dataset["venue"] = dataset["venue"].map(dizionari[3])
    dataset["time"] = dataset["time"].map(dizionari[4])
    #dataset["formation"] = dataset["formation"].map(dizionari[6])
    dataset["result"] = dataset["result"].map(dizionari[5])
    dataset["date"] = dataset["date"].map(dizionari[6])
    dataset["day"] = dataset["day"].map(dizionari[7])
    #dataset["captain"] = dataset["captain"].map(dizionari[10])

    dataset = dataset.rename(columns={"date": 0, "time": 1, "round": 2, "day": 3, "venue": 4, "result": 5, "gf": 6, "ga": 7, "opponent": 8, "xg": 9, "xga": 10, "poss_x": 11,
                                    "sh": 12, "sot": 13, "dist": 14, "pk": 15, "pkatt": 16,  "poss_y": 17, "touches": 18, 
                                    "def pen": 19, "def 3rd": 20, "mid 3rd": 21, "att 3rd": 22, "att pen": 23, "team": 24})
    
    return dataset