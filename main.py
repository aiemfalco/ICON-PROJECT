from owlready2 import *
import dataset as ds
import ontology as ot
import learning as lg
import csp as csp

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
        csp.create_schedule(ds.get_dataset())
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
