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
    matches = [] # 380 stringhe, chiavi poi 
    for day in days:
        for i in range(len(teams)//2): #380(38x10) matches, da 1_0 a 38_9
            matches.append(f"match{day}_{i}")

    # Aggiungere variabili per ogni partita
    for match in matches:
        problem.addVariable(match, [(team1, team2) for team1 in teams for team2 in teams if team1 != team2]) #aggiunge 380 variabili

    # Assegnare arbitri alle partite, aggiungo variabili per ogni partita
    for day in days:
        for i in range(len(teams)//2): #38 x 10
            match = f"match{day}_{i}"
            problem.addVariable(f"referee_{match}", referees) #aggiunge 380 variabili

    # Vincolo 1: ogni squadra gioca esattamente una partita per ogni giornata
    for day in range(1, len(days) + 1):
        # prende tutti i match che vanno da day_0 a day_9 a ogni iterata (quindi una giornata)
        day_matches = [match for match in matches if match.startswith(f"match{day}_")]

        # Lista delle squadre coinvolte in ciascuna partita della giornata
        teams_involved = []
        for match in day_matches:
            team1, team2 = problem.get_assignment(match)
            teams_involved.extend([team1, team2])
        '''
        # Lista delle variabili per le partite di questa giornata
        match_vars = [problem._variables(match) for match in day_matches] # non esiste sto metodo PD!
        
        # Lista delle squadre coinvolte in tutte le partite di questa giornata
        teams_involved = []
        for match_var in day_matches:
            teams_involved.extend(problem.get_values(match_vars))
        '''

        # Aggiungi vincolo: tutte le squadre coinvolte devono essere diverse tra loro
        problem.addConstraint(AllDifferentConstraint(), teams_involved)


    ''' Vincolo: ogni squadra gioca una sola partita per giornata
    for day in days:
        teams_for_day = [f"match{day}_{i}" for i in range(len(teams)//2)]
        # teams_for_day = [match for match in matches if team in match and problem.getSolution()[match] == day]
        for team in teams:
            # problem.addConstraint(lambda *matches, team=team: sum(team in match for match in matches) == 1, teams_for_day)
            problem.addConstraint(AllDifferentConstraint(), teams_for_day)
    
    andata_days = days[:19]
    for day in andata_days: 
        for i in range(len(teams)//2): # 19 x 10
            match_andata = f"match{day}_{i}" #match di andata viene preso tra [1_0 , 19_9]
            match_ritorno = f"match{day + len(andata_days)}_{i}" # match di ritorno viene preso tra [20_0 , 38_9]
            problem.addConstraint(lambda andata, ritorno: andata == ritorno[::-1], [match_andata, match_ritorno])
    '''
    # Vincolo 2: ogni arbitro arbitra una sola partita per giornata
    for day in days:
        referee_vars = [f"referee_match{day}_{i}" for i in range(len(teams)//2)]
        problem.addConstraint(AllDifferentConstraint(), referee_vars)    

    # Risolvere il problema
    solution = problem.getSolution()

    return solution
