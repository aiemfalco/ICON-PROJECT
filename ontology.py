import pandas as pd
import dataset as ds
from owlready2 import *

def get_last_5_matches_results(squadra, date_partita, dizionario_partite):
  """
  Questa funzione prende una squadra, una data della partita e un dizionario di partite e restituisce una lista di caratteri (W, D, L) con i risultati delle ultime 5 partite della squadra.

  Args:
    squadra: Nome della squadra per cui si vogliono ottenere i risultati.
    date_partita: Data della partita in corso.
    dizionario_partite: Dizionario che mappa le squadre alle date delle partite.

  Returns:
    Lista di caratteri (W, D, L) con i risultati delle ultime 5 partite della squadra.
  """
  # Inizializza una lista vuota per i risultati
  last_5_matches_results = []

  # Trova la posizione della partita in corso nel dizionario
  current_match_index = dizionario_partite["." + squadra].index(date_partita)

  # Itera sulle ultime 5 partite, escludendo la partita in corso
  for i in range(current_match_index - 1, current_match_index - 6, -1):
    if i >= 0:
      # Ottieni il risultato della partita
      result = dizionario_partite[squadra][i]

      # Aggiungi il risultato alla lista
      last_5_matches_results.append(result)

  # Restituisci la lista dei risultati
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
 
    squadra_di_interesse = onto.Squadra("Roma")
    for partita in onto.Partita.instances():
        # Verifica se la squadra di interesse è la squadra di casa o ospite nella partita corrente
        if squadra_di_interesse in partita.squadra_di_casa or squadra_di_interesse in partita.squadra_in_trasferta:
        # Stampa i dettagli della partita
            print("Partita index:", partita)
            print("Data partita:", partita.data_partita)
            print("Squadra di casa:", partita.squadra_di_casa[0] if squadra_di_interesse in partita.squadra_di_casa else partita.squadra_in_trasferta[0])
            print("Squadra ospite:", partita.squadra_in_trasferta[0] if squadra_di_interesse in partita.squadra_di_casa else partita.squadra_di_casa[0])
            print("Risultato:", partita.risultato)
            print("Arbitro:", partita.arbitrata)
            print("-----------------------")

    # popolo la relazione "rappresenta" tra squadra e capitano
    with onto:
        for squadra, capitano in dic_teams_cap.items():
            onto.Capitano(capitano).rappresenta = [onto.Squadra(squadra)]

    # creare le due nuove caratteristiche "last_five_home" e "last_five_away" per tutte le squadre
    dataset['last_five_home'] = None
    dataset['last_five_away'] = None

    # dizionario delle date ordinato
    X_date = list(range(1, 551))
    dates = set(dataset['date'])
    date_list = list(dates)
    ordered_date_set = sorted(date_list) 
    dic_dates = dict(zip(ordered_date_set, X_date))

    dic_teamhome_dates = {}
    for partita in onto.Partita.instances():
        hometeam = partita.squadra_di_casa.first()
        if isinstance(hometeam, Squadra):
            date = partita.data_partita.first()
            if hometeam not in dic_teamhome_dates:
                dic_teamhome_dates[hometeam]= []
            dic_teamhome_dates[hometeam].append(date)

    # print(dic_teamhome_dates)
    '''
    with onto:
        for index, row in dataset.iterrows(): #scorro il dataset
            #for partita in onto.Partita.instances(): # scorro tutte le partite in Partita
                if row["home"] == dic_teamhome_dates(row["home"]):
                    matchweek = row["round"].split(' ')
                    # print(matchweek[1])
                    if int(matchweek[1]) >= 5: # ci accertiamo che una partita sia almeno alla quinta giornata
                        if row["date"] == partita.data_partita and row["team"] == onto.partita.squadra_di_casa and row["opponent"] == onto.partita.squadra_in_trasferta:
                            games_played = dataset[row["home"] == partita.squadra_in_casa] # tutte le partite giocate da squadra di casa in partita
                            dataset["last_five_home"] = games_played.tail(5) # gli ultimi 5 results di squadra in casa di partita sottofroma di stringa
    '''
    '''
    with onto:
        for index, row in dataset.iterrows():
            # Recupera le date delle ultime 5 partite in casa
            if row["team"] in dic_teamhome_dates:
                last_five_home_dates = []
                for date in dic_teamhome_dates[row["team"]]:
                    if len(last_five_home_dates) < 5:
                        last_five_home_dates.append(str(date))

                # Controlla se la partita è almeno alla quinta giornata
                matchweek = row["round"].split(' ')
                if int(matchweek[1]) >= 5:
                    # Salva la partita corrente in una variabile
                    current_match = None
                    for partita in onto.Partita.instances():
                        if (
                            row["date"] == partita.data_partita.first()
                            and row["team"] == partita.squadra_di_casa.first()
                            and row["opponent"] == partita.squadra_in_trasferta.first()
                        ):
                            current_match = partita
                            break

                    # Controlla se la partita corrente è valida
                    if current_match:
                        # Inserisci le date nella colonna "last_five_home"
                        if "last_five_home" not in dataset.columns:
                            dataset["last_five_home"] = []
                        dataset.loc[index, "last_five_home"] = ','.join(last_five_home_dates)
        '''
    for index, row in dataset.iterrows():
        # Ottieni le informazioni dalla riga corrente
        squadra = row["team"]
        date_partita = row["date"]

        # Ottieni i risultati delle ultime 5 partite
        last_5_matches_results = get_last_5_matches_results(squadra, date_partita, dic_teamhome_dates)

        # Aggiorna il DataFrame con i risultati
        dataset.loc[index, "last_five_home"] = last_5_matches_results
    

    print(dataset["last_five_home"])    

    onto.save(file = "./archive/ontology.rdf")

    return onto