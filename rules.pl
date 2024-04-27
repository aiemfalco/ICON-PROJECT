:- use_module(library(date)).

print_current_date :-
    get_time(Timestamp),
    stamp_date_time(Timestamp, DateTime, local),
    format_time(atom(Date), '%Y-%m-%d', DateTime),
    writeln(Date).

is_a_valid_number(Numero) :-
    Numero >= 1,
    Numero =< 5.

is_a_valid_round(Numero) :-
    Numero > 0,
    Numero < 39.

valid_time(Hour, Minute) :-
    Hour > 0, Hour < 24,
    Minute > 0, Minute < 60.
    


partita(Date, Time, Round, Venue, Opponent, Formation, Referee, Team).

partita_futura(partita) :-
    partita(Date, Time, Round, Venue, Opponent, Formation, Referee, Team), Date > Date.