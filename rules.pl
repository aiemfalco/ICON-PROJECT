:- use_module(library(date)).

print_current_date :-
    get_time(Timestamp),
    stamp_date_time(Timestamp, DateTime, local),
    format_time(atom(Date), '%Y-%m-%d', DateTime),
    writeln(Date).

/*Predicato per controllare se il numero inserito per la formazione è valido*/
is_a_valid_number(Numero) :-
    Numero >= 1,
    Numero =< 5.

partita(Date, Time, Round, Venue, Opponent, Formation, Referee, Team).

partita_futura(partita(Date, Time, Round, Venue, Opponent, Formation, Referee, Team), Date) :-
    partita(Date, Time, Round, Venue, Opponent, Formation, Referee, Team), Date > Date.