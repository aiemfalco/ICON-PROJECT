from constraint import Problem, AllDifferentConstraint
import dataset as ds
import random

def get_teams_and_referees():

    dataset = ds.get_dataset()
    teams = list(set(dataset['team']))
    teams = random.sample(teams, 20) # seleziona randomicamente 20 squadre dalla lista teams(diverse ad ogni run)
    referees = list(set(dataset['referee']))
    rounds = list(range(1, 39))
    
    return teams, referees, rounds

def create_schedule(teams, referees, days):
    problem = Problem()
    
    # Definire le variabili per le partite
    matches = []
    for day in days:
        for i in range(len(teams)//2):
            matches.append(f"match{day}_{i}")

    # Aggiungere variabili per ogni partita
    for match in matches[:190]:  # 19 giorni * 10 partite al giorno
        problem.addVariable(match, [(team1, team2) for team1 in teams for team2 in teams if team1 != team2])

    # Vincolo: ogni squadra gioca una sola partita per giornata
    for day in days:
        match_day_vars = [f"match{day}_{i}" for i in range(len(teams)//2)]
        problem.addConstraint(AllDifferentConstraint(), match_day_vars)
    
    # Vincolo: nessuna partita ripetuta nel girone di andata
    for i in range(len(teams)//2):
        match_pairs = [f"match{day}_{i}" for day in days]
        problem.addConstraint(AllDifferentConstraint(), match_pairs)
    
    '''Vincolo: girone di ritorno invertito rispetto all'andata
    for day in days:
        for i in range(len(teams)//2):
           if day + len(days) < 2 * len(days):
                match_andata = f"match{day}_{i}"
                match_ritorno = f"match{day + len(days)}_{i}"
                problem.addConstraint(lambda andata, ritorno: andata == ritorno[::-1], [match_andata, match_ritorno])
    '''
    andata_days = days
    ritorno_days = list(range(len(days), 2*len(days)))
    
    for day in andata_days:
        for i in range(len(teams)//2):
            match_andata = f"match{day}_{i}"
            match_ritorno = f"match{day + len(days)}_{i}"
            if match_ritorno in matches:  # Verifica che la variabile esista
                problem.addConstraint(lambda andata, ritorno: andata == ritorno[::-1], [match_andata, match_ritorno])

    # Assegnare arbitri alle partite
    for day in days:
        for i in range(len(teams)//2):
            match = f"match{day}_{i}"
            problem.addVariable(f"referee_{match}", referees)
    
    # Vincolo: ogni arbitro arbitra una sola partita per giornata
    for day in days:
        referee_vars = [f"referee_match{day}_{i}" for i in range(len(teams)//2)]
        problem.addConstraint(AllDifferentConstraint(), referee_vars)    

    # Risolvere il problema
    solution = problem.getSolution()

    return solution

# Esempio di utilizzo
teams = [f"Team{i}" for i in range(1, 21)]
referees = [f"Referee{i}" for i in range(1, 11)]
days = list(range(1, 20))  # 19 giornate per il girone di andata

schedule = create_schedule(teams, referees, days)
print(schedule)
