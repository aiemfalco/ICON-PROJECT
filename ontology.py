import pandas as pd
import dataset as ds
from owlready2 import *

'''
    Modulo riguardo l'ontologia
'''


def load_onto():
    onto = get_ontology("./archive/ontology.rdf").load()
    return onto

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

    onto = get_ontology("")

    with onto:
        class Squadra(Thing):
            pass
        class Capitano(Thing):
            pass
        class Arbitro(Thing):
            pass
        class Partita(Thing):
            pass
        
        # Relazioni tra classi
        class rappresenta(ObjectProperty):
            domain = [Capitano]
            range = [Squadra]
        class squadra_di_casa(ObjectProperty):
            domain = [Partita]
            range = [Squadra]
        class squadra_in_trasferta(ObjectProperty):
            domain = [Partita]
        class arbitrata(ObjectProperty):
            domain = [Partita]
            range = [Arbitro]

        # Definizione degli attributi
        class nome_squadra(DataProperty):
            domain = [Squadra]
            range = [str]
        class nome_capitano(DataProperty):
            domain = [Capitano]
            range = [str]
        class nome_arbitro(DataProperty):
            domain = [Arbitro]
            range = [str]
        class data_partita(DataProperty):
            domain = [Partita]
            range = [datetime.date]
        class risultato(DataProperty):
            domain = [Partita]
            range = [str]

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
            if row.iloc[49] == item:
                dic_teams_cap[item] = row.iloc[15]

    # popolo le classi Squadra e Capitano
    with onto:
        for squadra, capitano in dic_teams_cap.items():
            s = Squadra(squadra)
            s.nome_squadra = [squadra]
            c = Capitano(capitano)
            c.nome_capitano = [capitano]
            c.rappresenta.append(s)
    
    # popolo la classe Arbitro
    refs = set(dataset["referee"])
    list_refs = list(refs)
    ordered_refs = sorted(list_refs)
    with onto:
        for arbitro in ordered_refs:
            a = Arbitro(arbitro)
            a.nome_arbitro = [arbitro]

    
    # popolo le istanze di Partita", inclusi attributi e relazioni
    with onto:
        for index, row in dataset.iterrows():
            if row.iloc[6] == "Home":
                nuova_partita = Partita(row["team"][:3] + row["opponent"][:3] + row["date"])
                # Stabilire la relazione tra la squadra di casa e la nuova partita
                nuova_partita.squadra_di_casa.append(Squadra(row.iloc[49]))
                # Stabilire la relazione tra la squadra ospite e la nuova partita
                nuova_partita.squadra_in_trasferta.append(Squadra(row.iloc[10]))
                # Stabilire la relazione tra partita e orario, che in questo caso è una stringa
                nuova_partita.data_partita = [row.iloc[1]]
                # Stabilire la relazione tra partita e risultato
                nuova_partita.risultato = [row.iloc[7]]
                # Stabilire la relazione tra partita e arbitro
                nuova_partita.arbitrata.append(Arbitro(row.iloc[17]))

    # salvo l'ontologia
    onto.save(file = "./archive/ontology.rdf", format="rdfxml")

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
    with onto:
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
            matchn = index + 1
            if (matchn) % 38 == 1 or (matchn) % 38 == 2 or (matchn) % 38 == 3 or (matchn) % 38 == 4 or (matchn) % 38 == 5:
                dataset.loc[index, "last_five"] = "0"
            else:
                # Ottieni i risultati delle ultime 5 partite
                last_5_matches_results = get_last_5_matches_results(squadra, date_partita, dic_teamhome_dates, onto)
                # Aggiorna il DataFrame con i risultati 
                dataset.loc[index, "last_five"] = last_5_matches_results
    return dataset

def asktoSparQL():
    team_name = "Juventus"
    query = f"""
        SELECT ?partita ?risultato
        WHERE {{
            ?partita rdf:type :Partita .
            ?partita :risultato ?risultato .
            ?squadra rdf:type :Squadra .
            ?squadra :nome_squadra "{team_name}" .
            ?partita :squadra_di_casa ?squadra .
            }}
    """
    result = list(default_world.sparql(query))
    for r in result:
        print("Match:", str(r[0])[1:], " result:", r[1])

def queryH2H(squadra1, squadra2):
    vs1 = 0
    vs2 = 0
    d = 0

    # cerca le partite sq1 vs sq2
    query = f"""
        SELECT ?partita ?risultato
        WHERE {{
            ?partita rdf:type :Partita .
            ?partita :risultato ?risultato .
            ?squadraH rdf:type :Squadra .
            ?squadraH :nome_squadra "{squadra1}" .
            ?squadraA rdf:type :Squadra .
            ?squadraA :nome_squadra "{squadra2}" .
            ?partita :squadra_di_casa ?squadraH .
            ?partita :squadra_in_trasferta ?squadraA .
            }}
    """
    result = list(default_world.sparql(query))
    # computa i risultati e stampa le partite (opzionale)
    for r in result:
        if str(r[1]) == "W":
            vs1 += 1
        elif str(r[1]) == "L":
            vs2 += 1
        else:
            d += 1
    
    for r in result:
        print("Match:", str(r[0])[1:], " result:", r[1])
    
    # cerca le partite sq2 vs sq1
    query = f"""
        SELECT ?partita ?risultato
        WHERE {{
            ?partita rdf:type :Partita .
            ?partita :risultato ?risultato .
            ?squadraH rdf:type :Squadra .
            ?squadraH :nome_squadra "{squadra2}" .
            ?squadraA rdf:type :Squadra .
            ?squadraA :nome_squadra "{squadra1}" .
            ?partita :squadra_di_casa ?squadraH .
            ?partita :squadra_in_trasferta ?squadraA .
            }}
    """
    result = list(default_world.sparql(query))
    # computa i risultati e stampa le partite (opzionale)
    for r in result:
        if str(r[1]) == "W":
            vs2 += 1
        elif str(r[1]) == "L":
            vs1 += 1
        else:
            d += 1
    
    for r in result:
        print("Match:", str(r[0])[1:], " result:", r[1])
    
    print(squadra1, "vs ", squadra2, " (W-D-L): ", vs1, "-", d, "-", vs2)