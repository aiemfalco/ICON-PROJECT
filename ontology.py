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

        # Definizione egli attributi
        class squadra_di_casa(DataProperty):
            domain = [Squadra]
            range = [Squadra]
        class squadra_in_trasferta(DataProperty):
            domain = [Squadra]
            range = [Squadra]
        class ha_giocato(DataProperty):
            domain = [Squadra]
            range = [str]
        class risultato(DataProperty):
            domain = [Squadra]
            range = [str]
        class arbitrata(DataProperty):
            domain = [Squadra]
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

    with onto:
        for index, row in dataset.iterrows():
            if row[6]=="Home":
                onto.Squadra(row[49]).partita.append(onto.Squadra(row[10]))
                #onto.Squadra(row[49]).partita = [onto.Squadra(row[10])]

    print(onto.Capitano.instances())
    print(onto.Squadra.instances())

    with onto:
        for squadra, capitano in dic_teams_cap.items():
            onto.Capitano(capitano).rappresenta = [onto.Squadra(squadra)]
            print(onto.Capitano(capitano).rappresenta)

    onto.save(file = "./archive/ontology.rdf")

    return onto