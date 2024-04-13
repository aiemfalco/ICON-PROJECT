:- use_module(library(date)).

partita(Date, Time, Round, Venue, Opponent, Formation, Referee, Team).

data_corrente(Anno, Mese, Giorno).
data_corrente(2024, 04, 13)
'''
data_corrente(Data) :-
    get_time(Timestamp),
    stamp_date_time(Timestamp, DateTime, local),
    date_time_value(date, DateTime, Data).
'''

partita_futura(P) :- 
    partita(date, _, _, _, _, _, _, _,), date > data_corrente(2024, 04, 13).