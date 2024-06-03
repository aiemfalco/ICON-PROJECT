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
        '''
        class data_partita(DataProperty):
            domain = [Partita]
            range = [datetime]
        class risultato(DataProperty):
            domain = [Squadra]
            range = [str]
        '''
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
                '''
                nuova_partita.data_partita.append(row[1])
                '''
                # Stabilire la relazione tra partita e risultato
                '''
                nuova_partita.risultato.append(row[7])
                '''
                # Stabilire la relazione tra partita e risultato
                nuova_partita.arbitrata.append(Arbitro(row[17]))

    # print di controllo . . .    
    squadra_di_interesse = onto.Squadra("Roma")
    for partita in onto.Partita.instances():
        # Verifica se la squadra di interesse è la squadra di casa o ospite nella partita corrente
        if squadra_di_interesse in partita.squadra_di_casa or squadra_di_interesse in partita.squadra_in_trasferta:
        # Stampa i dettagli della partita
            print("Partita:", partita)
            #print("Partita:", partita.data_partita)
            print("Squadra di casa:", partita.squadra_di_casa[0] if squadra_di_interesse in partita.squadra_di_casa else partita.squadra_in_trasferta[0])
            print("Squadra ospite:", partita.squadra_in_trasferta[0] if squadra_di_interesse in partita.squadra_di_casa else partita.squadra_di_casa[0])
            #print("Risultato:", partita.risultato)
            print("Arbitro:", partita.arbitrata)
            print("-----------------------")


    '''      
    print(onto.Capitano.instances())
    print(onto.Squadra.instances())
    '''

    # popolo la relazione "rappresenta" tra squadra e capitano
    with onto:
        for squadra, capitano in dic_teams_cap.items():
            onto.Capitano(capitano).rappresenta = [onto.Squadra(squadra)]
            
    

    onto.save(file = "./archive/ontology.rdf")

    return onto