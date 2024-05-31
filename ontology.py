import pandas as pd
import dataset as ds
from owlready2 import *

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
        
        # RELAZIONI
        class rappresenta(ObjectProperty):
            domain = [Capitano]
            range = [Squadra]
        class partita(ObjectProperty):
            domain = [Squadra]
            range = [Squadra]

        # Definizione della classe che estende la relazione per includere attributi
        class dettaglioPartita(partita):
            pass
        # Definizione delle proprietà della relazione partita
        dettaglioPartita.addProperty("squadra_di_casa", [Squadra])
        dettaglioPartita.addProperty("squadra_in_trasferta", [Squadra])
        dettaglioPartita.addProperty("data_partita", [str])
        dettaglioPartita.addProperty("punteggio", [int])
        dettaglioPartita.addProperty("stadio", [str])
        dettaglioPartita.addProperty("arbitro", [Arbitro])

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

    print(onto.Capitano.instances())
    print(onto.Squadra.instances())

    with onto:
        for squadra, capitano in dic_teams_cap.items():
            onto.Capitano(capitano).rappresenta = [onto.Squadra(squadra)]
            print(onto.Capitano(capitano).rappresenta)

    onto.save(file = "./archive/ontology.rdf")

    return onto