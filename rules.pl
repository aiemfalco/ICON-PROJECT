:- use_module(library(date)).

get_current_date/1(Date) :-
    get_time(Stamp),
    stamp_date_time/(Stamp, DateTime, local),
    date_time_value(date, DateTime, Date).


partita(Date, Time, Round, Venue, Opponent, Formation, Referee, Team).

partita_futura(partita) :- 
    partita(Date, _, _, _, _, _, _, _,), Date > get_current_date/1(Date)