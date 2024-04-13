:- use_module(library(date)).

partita(campionato, squadra_casa, squadra_ospite, data).
data_corrente(Data) :-
    get_time(Timestamp),
    stamp_date_time(Timestamp, DateTime, local),
    date_time_value(date, DateTime, Data).

partita_futura(P) :- partita(_, _, _, Data), Data > data_corrente(P).
