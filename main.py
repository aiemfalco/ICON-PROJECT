import pandas as pd
from skopt import BayesSearchCV
from skopt.space import Real, Categorical, Integer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
import seaborn as sns
import os
from owlready2 import *
import dataset as ds
import ontology as ot
import learning as lg

def chiedi_scelta():
    print("Scegli una delle seguenti opzioni:")
    print("1. Fai una predizione (Apprendimento supervisionato)")
    print("2. Scheduling di un calendario (CSP)")
    print("3. Esegui query SPARQL")
    
    scelta = None
    while scelta not in ['1', '2', '3']:
        scelta = input("Inserisci il numero della tua scelta (1, 2, o 3): ")
        if scelta not in ['1', '2', '3']:
            print("Scelta non valida. Per favore, scegli 1, 2, o 3.")
    
    return scelta

def chiedi_query():
    print("Queries disponibili:")
    print("1. Mostra le partite giocate da due squadre(casa e trasferta)")
    print("2. Mostra le partite giocate da una squadra")
    print("3. Mostra le partite giocate in una data specifica")

    scelta_q = None
    while scelta_q not in ['1', '2', '3']:
        scelta_q = input("Inserisci il numero della tua scelta (1, 2, o 3): ")
        if scelta_q not in ['1', '2', '3']:
            print("Scelta non valida. Per favore, scegli 1, 2, o 3.")
            
    return scelta_q

def main():
    print("Ciao user")
    scelta = int(chiedi_scelta())
    if scelta == 1:
        lg.learner()
    elif scelta == 2:
        print("da fare csp")
    else:
        scelta_q = int(chiedi_query())
        if scelta_q == 1:
            team1 = input("Inserisci prima squadra: ")
            team2 = input("Inserisci la seconda squadra: ")
            ot.history_vs(team1, team2)
        elif scelta_q == 2:
            team1 = input("Inserisci la squadra: ")
            ot.games_of_a_team(team1)
        else:
            data = input("Inserisci una data nel formato YYYY-MM-DD: ")
            ot.matches_this_day(ot.load_onto(), data)
    
    ''' ISSUE
     # path = "./archive/ontology.rdf"
    # tentativi di caricamento dell'ontologia
    try:
        ontology = get_ontology("file://" + path).load()
        #ontology = ot.load_onto(path)
        if(ontology):
            print("Ontologia caricata con successo")
    except FileNotFoundError:
        print("Creo l'ontologia...")
        ontology = ot.create_ontology()
    
    # altro modo che non funziona 
    path = "./archive/ontology.rdf"
    if os.path.exists(path):
        ontology = ot.load_onto()
        print("Ontologia caricata con successo")
        for cls in ontology.classes():
            print(cls)
    else:
        print("Creo l'ontologia...")
        ontology = ot.create_ontology()
        for cls in ontology.classes():
            print(cls)

    #non fa vedere gli attributi
    for partita in ontology.Partita.instances():
        print("partita arbitrata da: ", partita.arbitrata)
    '''
main()
