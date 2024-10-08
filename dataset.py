import pandas as pd

'''
    Modulo che riguarda la pulizia del dataset grezzo caricato da csv
'''

# Restituisce il dataset grezzo
def get_dataset():
    filename = "archive/seriea-matches.csv"
    dataset = pd.read_csv(filename)

    # cambia la stringa "Internazionale" in "Inter" nella colonna "team", l'ultima
    for index, row in dataset.iterrows(): # itera sulle righe (index) e le colonne (rows) alle quali ci si può riferire con il nome
        if row["team"] == "Internazionale":
            dataset.at[index, "team"] = "Inter"
    
    return dataset

# Restituisce il dataset ridotto delle features che abbiamo deciso di rimuovere 
def refine_dataset(dataset):

    features = dataset.columns.tolist()

    features_to_delete = []
    features_to_delete.append(features[2])
    features_to_delete.append(features[3])
    features_to_delete.append(features[4])
    features_to_delete.append(features[5])
    features_to_delete.append(features[14])
    features_to_delete.append(features[15])
    features_to_delete.append(features[16])
    features_to_delete.append(features[17])
    features_to_delete.append(features[21])
    for i in range(31, len(features) - 2):
        features_to_delete.append(features[i]) 

    dataset = dataset.drop(features_to_delete, axis = 1)

    #andiamo ad eliminare tutti i valori null (ne rimanevano solamente 3 nella colonna "dist")
    dataset = dataset[dataset.isnull().sum(axis=1) == 0]
    
    return dataset

# Restiuisce i dizionari delle features che hanno bisogno di mapping per essere date ai modelli.
def generate_dictionary(dataset):

    # preprocessing delle features stringhe in intero
    dates = set(dataset['date'])
    X_date = list(range(1, len(dates) + 1))
    date_list = list(dates)
    ordered_date_set = sorted(date_list) # ho ordinato il set di date in ordine crescente (dal 2017 al 2022)
    dic_dates = dict(zip(ordered_date_set, X_date)) # e poi codifico ogni data con un valore intero, ora so che 3 è una data più avanti cronologicamente di 2
    
    venues = set(dataset['venue'])
    X_venue = list(range(1, len(venues) + 1))
    venues_list = list(venues)
    ordered_venues_set = sorted(venues_list)
    dic_venues = dict(zip(ordered_venues_set, X_venue))

    results = set(dataset['result'])
    X_result = list(range(1, len(results) + 1))
    results_list = list(results)
    ordered_results_set = sorted(results_list)
    dic_results = dict(zip(ordered_results_set, X_result))
    
    teams = set(dataset['team'])
    X_team = list(range(1, len(teams) + 1))
    teams_list = list(teams)
    ordered_teams_set = sorted(teams_list)
    dic_teams = dict(zip(ordered_teams_set, X_team))

    dic_opponents = dic_teams

    lastfive = set(dataset['last_five'])
    X_lastfive = list(range(1, len(lastfive) + 1))
    lastfive_list = list(lastfive)
    ordered_lastfive_set = sorted(lastfive_list)
    dic_lastfive = dict(zip(ordered_lastfive_set, X_lastfive))

    return dic_teams, dic_opponents, dic_venues, dic_results, dic_dates, dic_lastfive

# Restituisce il dataset mappato grazie ai dizionari ottenuti dalla funzione generate_dictionary -> dataset pronto per l'addestramento
def create_data_frame(dataset, dizionari):
    
    # qui andiamo a sostituire gli elementi che sono rappresentati come stringhe dentro il dataset con i valori dei rispettivi dizionari tramite la funzione di libreria "map"
    dataset["team"] = dataset["team"].map(dizionari[0])
    dataset["opponent"] = dataset["opponent"].map(dizionari[1])
    dataset["venue"] = dataset["venue"].map(dizionari[2])
    dataset["result"] = dataset["result"].map(dizionari[3])
    dataset["date"] = dataset["date"].map(dizionari[4])
    dataset["last_five"] = dataset["last_five"].map(dizionari[5])

    dataset = dataset.rename(columns={"mp": 0, "date": 1, "venue": 2, "result": 3, "gf": 4, "ga": 5, "opponent": 6, "xg": 7, "xga": 8, "poss_x": 9,
                                    "sh": 10, "sot": 11, "dist": 12, "pk": 13, "pkatt": 14,  "poss_y": 15, "touches": 16, 
                                    "def pen": 17, "def 3rd": 18, "mid 3rd": 19, "att 3rd": 20, "att pen": 21, "team": 22, "last_five": 23})
    
    return dataset