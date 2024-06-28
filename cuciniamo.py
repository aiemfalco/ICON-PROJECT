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
    half_days = days[:len(days)//2]
    return_days = days[len(days)//2:]
    num_matches_per_day = len(teams) // 2

    # Part 1: Create first half of the schedule (round-robin)
    problem = Problem()
    matches = []
    for day in half_days:
        for i in range(num_matches_per_day):
            matches.append(f"match{day}_{i}")

    for match in matches:
        problem.addVariable(match, [(team1, team2) for team1 in teams for team2 in teams if team1 != team2]) # aggiungo 380 variabili al CSP

    # Vincolo 1: tutte le squadre devono essere diverse in ogni giornata
    for day in half_days:
        day_matches = [f"match{day}_{i}" for i in range(num_matches_per_day)] # prendo tutte le partite di una giornata
        for i in range(len(day_matches)):
            for j in range(i + 1, len(day_matches)):
                problem.addConstraint(lambda a, b: a[0] != b[0] and a[0] != b[1] and a[1] != b[0] and a[1] != b[1],
                                      (day_matches[i], day_matches[j])) # vincolo tutte le squadre devono essere diverse in tutte le partite della giornata i
                
    # Vincolo 2: tutte le partite/team1 vs team2) devono essere diverse in ogni giornata (itera per tutte le 19 giornate di andata )
    for day1 in half_days:
        for day2 in half_days: #19x19
            if day1 < day2:
                matches_day1 = [f"match{day1}_{i}" for i in range(num_matches_per_day)]
                matches_day2 = [f"match{day2}_{i}" for i in range(num_matches_per_day)]
                for match1 in matches_day1:
                    for match2 in matches_day2:
                        problem.addConstraint(lambda a, b: a != b and (a[0], a[1]) != (b[1], b[0]),
                                              (match1, match2)) # i match sono tutti diversi tra loro in ogni giornata per tutte le giornate 
    print("Prima di getSolutions()")
    solution = problem.getSolution()
    print("Dopo getSolutions()")
    if not solution:
        raise Exception("No solution found for the first half of the schedule")
    print(solution)

    # Creo i match di andata e ritorno 
    for day in return_days:
        for i in range(num_matches_per_day):
            match_going = f"match{day - len(half_days)}_{i}"
            match_return = f"match{day}_{i}"
            problem.addVariable(match_return, [(solution[match_going][1], solution[match_going][0])])

    return problem.getSolution()

