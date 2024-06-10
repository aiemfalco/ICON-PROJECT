import pandas as pd
import dataset as ds
from owlready2 import *

def get_last_5_matches_results(squadra, date_partita, dizionario_partite_casa, ontology):

    # Inizializza una lista vuota per i risultati
    last_5_matches_results = []
    
    current_match_index = -1

    # Trova la posizione della partita in corso nel dizionario
    for s, data in dizionario_partite_casa.items():
        if date_partita in data and squadra in s:
            current_match_index = dizionario_partite_casa[s].index(date_partita)
            break

    if current_match_index != -1:
        # Itera sulle ultime 5 partite, escludendo la partita in corso
        for i in range(current_match_index - 1, current_match_index - 6, -1):
            if i != 0:
                # Ottieni il risultato della partita
                date = dizionario_partite_casa[s][i]
                #scorriamo le partite in Partita
                for partita in ontology.Partita.instances():
                    # Controllo che la data sia giusta e che la squadra sia giusta per ogni iterata, in caso positivo appendo il risultato alla lista.
                    if date == partita.data_partita.first() and (str(partita.squadra_di_casa.first()) == s or str(partita.squadra_in_trasferta.first()) == s):
                        result = partita.risultato.first()
                        if str(partita.squadra_in_trasferta.first()) == s and partita.risultato.first() != "D":       
                            if result == "W":
                                result = "L"
                            else:
                                result = "W"
                        # Aggiungi il risultato alla lista
                        last_5_matches_results.append(result)


    # Restituisci la lista dei risultati
    last_5_matches_results = ''.join(last_5_matches_results)
    return last_5_matches_results


def create_ontology():
    path = "./archive/ontology.rdf"
    onto = get_ontology("")
    
    #creo le classi Squadra, Capitano e le relazioni
    class rappresenta (Thing >> Thing):
        pass
    with onto:
        class Squadra(Thing):
            pass
        class Capitano(Thing):
            pass
        class Arbitro(Thing):
            pass
        class Partita(Thing):
            pass
        
        # RELAZIONI
        class rappresenta(ObjectProperty):
            domain = [Capitano]
            range = [Squadra]

        # Definizione egli attributi
        class squadra_di_casa(ObjectProperty):
            domain = [Partita]
            range = [Squadra]
        class squadra_in_trasferta(ObjectProperty):
            domain = [Partita]
            range = [Squadra]
        class data_partita(DataProperty):
            domain = [Partita]
            range = [datetime.date]
        class risultato(DataProperty):
            domain = [Squadra]
            range = [str]
        class arbitrata(ObjectProperty):
            domain = [Partita]
            range = [Arbitro]

    # creo il dizionario squadra-capitano
    dataset = ds.get_dataset()

    teams = set(dataset['team'])
    list_teams = list(teams)
    ordered_teams = sorted(list_teams)
    
    # captains viene commentato perché tramite i teams presi dal dataset si può fare questo for:
    dic_teams_cap = {}
    for index, row in dataset.iterrows():
        for item in ordered_teams:
            # qui si scorrono tutti i teams presenti nel dataset, e si assegna il corrispondente capitano del team
            if row[49] == item:
                dic_teams_cap[item] = row[15]

    # popolo le classi Squadra e Capitano
    with onto:
        for squadra, capitano in dic_teams_cap.items():
            onto.Squadra(squadra)
            onto.Capitano(capitano)

    arbitri = set(dataset["referee"])
    with onto:
        for index, row in dataset.iterrows():
            for arbitro in arbitri:
                if row[17] == arbitro:
                    onto.Arbitro(arbitro)

    
    # popolo gli oggetti di "partita", mettendo in relazione due squadre e aggiungo gli attributi degli oggetti
    with onto:
        for index, row in dataset.iterrows():
            if row[6]=="Home":
                nuova_partita = Partita()
                # Stabilire la relazione tra la squadra di casa e la nuova partita
                nuova_partita.squadra_di_casa.append(Squadra(row[49]))
                # Stabilire la relazione tra la squadra ospite e la nuova partita
                nuova_partita.squadra_in_trasferta.append(Squadra(row[10]))
                # Stabilire la relazione tra partita e orario, che in questo caso è una stringa
                nuova_partita.data_partita.append(row[1])
                # Stabilire la relazione tra partita e risultato
                nuova_partita.risultato.append(row[7])
                # Stabilire la relazione tra partita e risultato
                nuova_partita.arbitrata.append(Arbitro(row[17]))

    # popolo la relazione "rappresenta" tra squadra e capitano
    with onto:
        for squadra, capitano in dic_teams_cap.items():
            onto.Capitano(capitano).rappresenta = [onto.Squadra(squadra)]
    
    # salvo l'ontologia
    onto.save(file = "./archive/ontology.rdf")

    
            
    # print(dataset["last_five"])    

    return onto

def getNewColumn(onto, dataset):
    # creo una nuova colonna "last_five" grazie alla conoscenza derivata
    dataset['last_five'] = None

    # dizionario delle date ordinato
    X_date = list(range(1, 551))
    dates = set(dataset['date'])
    date_list = list(dates)
    ordered_date_set = sorted(date_list) 
    dic_dates = dict(zip(ordered_date_set, X_date))

    dic_teamhome_dates = {}
    list_team_dates_to_sort = []
    for partita in onto.Partita.instances():
        date = partita.data_partita.first()
        hometeam = partita.squadra_di_casa.first()
        awayteam = partita.squadra_in_trasferta.first()
        if str(hometeam) not in dic_teamhome_dates:
            dic_teamhome_dates[str(hometeam)] = []
            dic_teamhome_dates[str(hometeam)].append(date)
        else:          
            dic_teamhome_dates[str(hometeam)].append(date)
        if str(awayteam) not in dic_teamhome_dates:
            dic_teamhome_dates[str(awayteam)] = []
            dic_teamhome_dates[str(awayteam)].append(date)
        else:          
            dic_teamhome_dates[str(awayteam)].append(date)
        dic_teamhome_dates[str(hometeam)] = sorted(dic_teamhome_dates[str(hometeam)])
        dic_teamhome_dates[str(awayteam)] = sorted(dic_teamhome_dates[str(awayteam)])

    for index, row in dataset.iterrows():
        # Ottieni le informazioni dalla riga corrente
        squadra = row["team"]
        date_partita = row["date"]
        matchweek = row["round"].split(' ')
        if int(matchweek[1]) > 5:
            # Ottieni i risultati delle ultime 5 partite
            last_5_matches_results = get_last_5_matches_results(squadra, date_partita, dic_teamhome_dates, onto)
            # Aggiorna il DataFrame con i risultati 
            dataset.loc[index, "last_five"] = last_5_matches_results
        else:
            dataset.loc[index, "last_five"] = "0"

    return dataset