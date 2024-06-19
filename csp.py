import dataset as ds
#from constraint import Problem, AllDifferentConstraint
import random
from constraint import Problem, AllDifferentConstraint

'''
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
result = list(prolog.query("calendario(Calendario)"))

# Stampa il risultato
if result:
    for row in result[0]['Calendario']:
        print(f"Partita: {row['S1']} vs {row['S2']}, Giornata: {row['G']}, Arbitro: {row['A']}")
else:
    print("Nessun calendario generato.")
'''
def get_teams_and_referees():
    dataset = ds.get_dataset()

    teams = list(set(dataset['team']))
    referees = list(set(dataset['referee']))
    rounds = list(range(1, 39))
    
    return teams, referees, rounds


def generate_football_schedule(teams, referees, days):

    #seleziona randomicamente 20 squadre dalla lista teams
    selected_teams = random.sample(teams, 20)

    # Crea un problema CSP
    problem = Problem()

    # Variabili
    variables = []

    # Genera tutte le possibili combinazioni di partite
    matches = []
    for team1 in selected_teams:
        for team2 in selected_teams:
            if team1 != team2:
                matches.append((team1, team2))

    # Variabili per le partite
    for day in days:
        for i in range(10):
            match_var = f"match_{day}_{i}"
            variables.append(match_var)
            # Quello che deve fare è prendere una partita a caso dalla lista matches e appenderla a match var.
            # La cosa a cui bisogna stare attenti è che quando itera la partita non deve contenere le due squadre già messe nelle partite precedenti.
            problem.addVariable(match_var, matches)

    # Variabili per gli arbitri
    for day in days:
        for i in range(10):
            referee_var = f"referee_{day}_{i}"
            variables.append(referee_var)
            problem.addVariable(referee_var, referees)

    # Vincoli
    # Un arbitro non può arbitrare più di una partita a giornata
    for day in days:
        for i in range(10):
            for j in range(i + 1, 10):
                problem.addConstraint(
                    lambda referee1, referee2: referee1 != referee2,
                    (f"referee_{day}_{i}", f"referee_{day}_{j}")
                )

    # Ogni squadra gioca una partita a giornata
    for day in days:
        for team in teams:
            problem.addConstraint(
                lambda *matches: sum(team in match for match in matches) == 1,
                [f"match_{day}_{i}" for i in range(10)]
            )

    # Una squadra non può giocare contro se stessa
    for day in days:
        for i in range(10):
            problem.addConstraint(
                lambda team1, team2: team1 != team2,
                (f"match_{day}_{i}", f"match_{day}_{i}")
            )

    # Risolvi il CSP
    calendar = problem.getSolution()
    return calendar


def print_football_schedule(calendar, days):
    if not calendar:
        print("Nessuna soluzione trovata.")
        return
    
    schedule = {day: [] for day in days}
    
    for key, value in calendar.items():
        if key.startswith("match"):
            day = int(key.split("_")[1])
            schedule[day].append(value)
    
    for day in days:
        print(f"Giornata {day}:")
        for match in schedule[day]:
            team1, team2 = match
            # Trova l'arbitro associato alla partita
            referee_var = f"referee_{day}_{schedule[day].index(match)}"
            referee = calendar[referee_var]
            print(f"Partita: {team1} vs {team2}, Arbitro: {referee}")
        print("\n")


# Genera le liste
lists = get_teams_and_referees()

# Genera il calendario
calendar = generate_football_schedule(lists[0], lists[1], lists[2])

# Stampa il calendario
print_football_schedule(calendar, lists[2])