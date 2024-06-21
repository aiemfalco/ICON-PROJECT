import dataset as ds
import random
from constraint import Problem, AllDifferentConstraint # libreria per il CSP

def get_teams_and_referees():

    dataset = ds.get_dataset()
    teams = list(set(dataset['team']))
    teams = random.sample(teams, 20) # seleziona randomicamente 20 squadre dalla lista teams(diverse ad ogni run)
    referees = list(set(dataset['referee']))
    rounds = list(range(1, 39))
    
    return teams, referees, rounds

def create_schedule(teams, referees, days):

    # Crea un problema CSP
    problem = Problem()
    #Definiamo le variabili
    matches = []
    for day in days:
        for i in range(len(teams)//2): # 10: n. di squadre che si affrontano a giornata
            matches.append(f"match_{day}_{i}")
             
    # Aggiungo le variabili al problema - 380 combinazioni di partite
    for match in matches[:190]:
        problem.addVariable(match, [(team1, team2)
                                    for team1 in teams for team2 in teams
                                    if team1 != team2])
        
    # Vincolo: Ogni squadra gioca una volta per giornata
    for day in days:
        for team in teams:
            problem.addConstraint(
                lambda *args, team=team: len([1 for match in args if team in match[:2]]) == 1,
                [f"Match_{day}_{i}" for i in range(len(teams) // 2)]
            )

    # Vincolo: Gli arbitri non possono arbitrare più partite nella stessa giornata
    for day in days:
        problem.addConstraint(
            AllDifferentConstraint(), # tutti arbitri diversi
            [f"Match_{day}_{i}" for i in range(len(teams) // 2)]
        )

    for match in matches:
        problem.addVariable(match, [(referee) for referee in referees])

    # Risolviamo il problema
    solutions = problem.getSolution()

    if solutions is None:
        print("Nessuna soluzione trovata.")
        return None
    
    # Creiamo il calendario
    schedule = {}
    for day in days:
        schedule[day] = []
        for i in range(len(teams) // 2):
            match = solutions[f"Match_{day}_{i}"]
            schedule[day].append(match)

    return schedule