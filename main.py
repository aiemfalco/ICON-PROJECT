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
import csp as csp
import cuciniamo as cc
import scarabocchi as sca

def chiedi_scelta():
    scelta = None
    while scelta not in ['1', '2', '3']:
        scelta = input("Inserisci il numero della tua scelta (1, 2, o 3): ")
        if scelta not in ['1', '2', '3']:
            print("Scelta non valida. Per favore, scegli 1, 2, o 3.")
    
    return scelta

def main():
    ontology = ot.create_ontology() 
    print("Scegli una delle seguenti opzioni:")
    print("1. Fai una predizione (Apprendimento supervisionato)")
    print("2. Scheduling di un calendario (CSP)")
    print("3. Esegui query SPARQL")
    scelta = int(chiedi_scelta())
    if scelta == 1:
        lg.learner(ontology)
    elif scelta == 2:
        liste = cc.get_teams_and_referees()
        schedule = cc.create_schedule(liste[0], liste[1], liste[2])
        filtered_matches = {k: v for k, v in schedule.items() if k.startswith('match')}
        sorted_matches = sorted(filtered_matches.items(), key=lambda x: int(x[0][5:].split('_')[0]))
        for match_id, teams in sorted_matches:
            print(f"{match_id}: {teams[0]} vs {teams[1]}")
    else:
        print("Queries disponibili:")
        print("1. Mostra le partite giocate da due squadre(casa e trasferta)")
        print("2. Mostra le partite giocate da una squadra")
        print("3. Mostra le partite giocate in una data specifica")
        scelta_q = int(chiedi_scelta())
        if scelta_q == 1:
            team1 = input("Inserisci prima squadra: ")
            team2 = input("Inserisci la seconda squadra: ")
            ot.history_vs(team1, team2)
        elif scelta_q == 2:
            team1 = input("Inserisci la squadra: ")
            ot.games_of_a_team(team1)
        else:
            data = input("Inserisci una data nel formato YYYY-MM-DD: ")
            ot.matches_this_day(data)

main()
