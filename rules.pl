:- use_module(library(date)).

print_current_date :-
    get_time(Timestamp),
    stamp_date_time(Timestamp, DateTime, local),
    format_time(atom(Date), '%Y-%m-%d', DateTime),
    writeln(Date).


partita(Date, Time, Round, Venue, Opponent, Formation, Referee, Team).

partita_futura(partita(Date, Time, Round, Venue, Opponent, Formation, Referee, Team), Date) :-
    partita(Date, Time, Round, Venue, Opponent, Formation, Referee, Team), Date > Date.