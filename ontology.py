import pandas as pd
import dataset as ds
from owlready2 import *
from owlready2.reasoning import sync_reasoner

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

        class rappresenta(ObjectProperty):
            domain = [Capitano]
            range = [Squadra]
    
    # creo il dizionario squadra-capitano
    dataset = ds.get_dataset()

    teams = set(dataset['team'])
    list_teams = list(teams)
    ordered_teams = sorted(list_teams)

    '''
    captains = set(dataset['captain'])
    list_captains = list(captains)
    ordered_captains = sorted(list_captains)
    '''
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

    # collego relazione tra capitano e squadra
    '''
    for capitano in onto.Capitano.instances():
        for squadra in onto.Squadra.instances():
            capitano.rappresenta.append(squadra)
    '''

    with onto:
        for squadra, capitano in dic_teams_cap.items():
            onto.Capitano(capitano).rappresenta = [onto.Squadra(squadra)]
            print(onto.Capitano(capitano).rappresenta)
    
    '''
    # visualizzo le relazioni
    for capitano in onto.Capitano.instances():
        print("Capitano:", capitano.name)
        for squadra in capitano.rappresenta:
            print("Squadra:", squadra.name)
    '''
    
    onto.save(file = "./archive/ontology.rdf")

    return onto