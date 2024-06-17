import pandas as pd
from skopt import BayesSearchCV
from skopt.space import Real, Categorical, Integer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import dataset as ds
import ontology as ot
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
import seaborn as sns
import os
from owlready2 import *
import learning as lg

def chiedi_scelta():
    print("Scegli una delle seguenti opzioni:")
    print("1. Apprendimento supervisionato")
    print("2. CSP")
    print("3. Esegui query SPARQL")
    
    scelta = None
    while scelta not in ['1', '2', '3']:
        scelta = input("Inserisci il numero della tua scelta (1, 2, o 3): ")
        if scelta not in ['1', '2', '3']:
            print("Scelta non valida. Per favore, scegli 1, 2, o 3.")
    
    return scelta

def main():

    scelta = int(chiedi_scelta())
    if scelta == 1:
        lg.learner()
    elif scelta == 2:
        print("CSP")
    else:
        print("Ontologia")

    '''
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
