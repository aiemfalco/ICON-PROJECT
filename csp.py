from constraint import Problem, AllDifferentConstraint
import random

def create_schedule(dataset): 

    teams = list(set(dataset['team']))
    teams = random.sample(teams, 20) 
    referees = list(set(dataset['referee']))
    rounds = list(range(1, 39))

    problem = Problem()

    # Definizione delle variabili per ogni giornata di andata e ritorno
    matches = [] # un match è descritto come: squadra casa, squadra ospite, arbitro
    for round in range(1, len(rounds) + 1):
        for match in range(10): 
            problem.addVariable(f"R{round}M{match}_home", teams)
            problem.addVariable(f"R{round}M{match}_away", teams)
            problem.addVariable(f"R{round}M{match}_referee", referees)
            matches.append((f"R{round}M{match}_home", f"R{round}M{match}_away", f"R{round}M{match}_referee")) # 380 matches

    # Vincolo 1: tutte le squadre e gli arbitri devono essere diversi nella giornata - FUNZIONA
    for round in range(1, len(rounds)+1): # da 1 a 38, si esclude il 39 perciò mettiamo +1
        home_teams = [f"R{round}M{match}_home" for match in range(10)]
        away_teams = [f"R{round}M{match}_away" for match in range(10)]
        all_teams = home_teams + away_teams
        # imponiamo che i teams devono essere tutti diversi, relativi alla giornata(round)
        
        # Questa riga di codice toglie tutti gli elementi che si presentano due volte.
        problem.addConstraint(AllDifferentConstraint(), all_teams)  

        # Vincolo sugli arbitri: devono essere tutti diversi nella giornata
        referees_round = [f"R{round}M{match}_referee" for match in range(10)] # contiene tutti gli arbitri della giornata "round"
        problem.addConstraint(AllDifferentConstraint(), referees_round)

        # Aggiungiamo la casualità degli arbitri
        referees_round = random.sample(referees, 10)  # Seleziona 10 arbitri casuali per la giornata
        referees_vars = [f"R{round}M{match}_referee" for match in range(10)]
        for var in referees_vars:
            problem.addConstraint(lambda arb, r=referees_round: arb in r, [var])
        problem.addConstraint(AllDifferentConstraint(), referees_vars)

    # Vincolo 2: una squadra non può affrontare se stessa - FUNZIONA
    for (home, away, arbiter) in matches: #scorro matches, dove ogni cella ha tre stringhe
        # Uso la funzione lambda
        problem.addConstraint(lambda h, a: h != a, (home, away)) # impongo che home e away devono essere diversi

    # Vincolo 3: Aggiungo vincolo per evitare ripetizioni esatte nelle giornate
    for round1 in range(1, 20):
        for round2 in range(round1 + 1, 20):
            for match1 in range(10):
                for match2 in range(10):
                    home_team1 = f"R{round1}M{match1}_home"
                    away_team1 = f"R{round1}M{match1}_away"
                    home_team2 = f"R{round2}M{match2}_home"
                    away_team2 = f"R{round2}M{match2}_away"
                    problem.addConstraint(lambda h1, a1, h2, a2: (h1 != h2 or a1 != a2), 
                                        (home_team1, away_team1, home_team2, away_team2))

    # Vincolo 4: partite di ritorno devono essere invertite
    for round in range(1, 20):
        for match in range(10):
            home_team = f"R{round}M{match}_home"
            away_team = f"R{round}M{match}_away"
            return_home_team = f"R{round+19}M{match}_home"
            return_away_team = f"R{round+19}M{match}_away"
            problem.addConstraint(lambda h, a, rh, ra: h == ra and a == rh, 
                                (home_team, away_team, return_home_team, return_away_team))

    # Risolvere il problema
    solution = problem.getSolution()

    # Stampare il calendario
    for round in range(1, 20):
        print(f"\nGiornata {round} (Andata): ")
        for match in range(10):
            home = solution[f"R{round}M{match}_home"]
            away = solution[f"R{round}M{match}_away"]
            referee = solution[f"R{round}M{match}_referee"]
            print(f"{home} vs {away} - Arbitro: {referee}")

    for round in range(20, 39):
        print(f"Giornata {round} (Ritorno): \n")
        for match in range(10):
            home = solution[f"R{round}M{match}_home"]
            away = solution[f"R{round}M{match}_away"]
            referee = solution[f"R{round}M{match}_referee"]
            print(f"{home} vs {away} - Arbitro: {referee}")
