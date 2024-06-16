import dataset as ds
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

def calendario_csp(teams, referees, rounds):
    problem = Problem()

    # Aggiungi variabili: ogni partita è identificata da (team1, team2, round, referee)
    matches = [(team1, team2, round_num, referee)
               for team1 in teams
               for team2 in teams
               for round_num in rounds
               for referee in referees
               if team1 != team2]

    problem.addVariables(matches, [0, 1])  # Variabile binaria: 0 = non giocata, 1 = giocata

    # Vincolo: Ogni squadra gioca esattamente una volta per giornata
    for team in teams:
        for round_num in rounds:
            round_matches = [(team1, team2, round_num, referee)
                             for team1, team2, rnd, referee in matches
                             if (team1 == team or team2 == team) and rnd == round_num]
            problem.addConstraint(lambda *args: sum(args) == 1, round_matches)

    # Vincolo: Ogni arbitro arbitra esattamente una volta per giornata
    for round_num in rounds:
        for referee in referees:
            referee_matches = [(team1, team2, round_num, referee)
                               for team1, team2, rnd, ref in matches
                               if rnd == round_num and ref == referee]
            problem.addConstraint(lambda *args: sum(args) <= 1, referee_matches)

    # Vincolo: Unica partita per squadra per giornata
    for round_num in rounds:
        for team in teams:
            team_matches = [(team1, team2, round_num, referee)
                            for team1, team2, rnd, referee in matches
                            if (team1 == team or team2 == team) and rnd == round_num]
            problem.addConstraint(lambda *args: sum(args) <= 1, team_matches)

    solutions = problem.getSolutions()

    if solutions:
        solution = solutions[0]  # Prendiamo la prima soluzione trovata
        calendar = [match for match in solution if solution[match] == 1]
        return calendar
    else:
        return None

def print_calendario(calendar):
    if calendar:
        for match in calendar:
            team1, team2, round_num, referee = match
            print(f"Partita: {team1} vs {team2}, Giornata: {round_num}, Arbitro: {referee}")
    else:
        print("Nessun calendario generato.")

# Genera le liste
teams, referees, rounds = get_teams_and_referees()

# Genera il calendario
calendar = calendario_csp(teams, referees, rounds)

# Stampa il calendario
print_calendario(calendar)