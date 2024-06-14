import dataset as ds
from pyswip import Prolog

def get_teams_and_referees():
    dataset = ds.get_dataset()

    teams = set(dataset['team'])
    X_teams = list(range(1, len(teams) + 1))
    teams_list = list(teams)

    referees = set(dataset['referee'])
    X_referees = list(range(1, len(referees) + 1))
    referees_list = list(referees)
    
    round_list = list(range(1, 39))
    return teams_list, referees_list, round_list


# Funzione per generare il file Prolog
def genera_file_prolog(teams_list, referees_list, round_list,  filename):
    with open(filename, 'w') as file:
        # Scrivi le squadre
        for squadra in teams_list:
            file.write(f"squadra('{squadra}').\n")
        
        # Scrivi gli arbitri
        for arbitro in referees_list:
            file.write(f"arbitro('{arbitro}').\n")

        # Scrivi le giornate
        for giornata in round_list:
            file.write(f"giornata({giornata}).\n")
    
    print(f"File Prolog {filename} generato con successo.")

# Genera le liste
liste = get_teams_and_referees()
# Genera il file prolog
genera_file_prolog(liste[0], liste[1], liste[2], 'dati.pl')

# Esegui il Prolog in Python
prolog = Prolog()
prolog.consult('scheduleNewSeason.pl')

# Esegui la query per stampare il calendario
result = list(prolog.query("stampa_calendario"))

# Stampa il risultato
for row in result:
    print(row)