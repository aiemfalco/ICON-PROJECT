% Carica i dati generati da Python
:- consult('dati.pl').

% Predicato per definire partite
partita(Squadra1, Squadra2, Giornata, Arbitro) :-
    squadra(Squadra1),
    squadra(Squadra2),
    Squadra1 \= Squadra2,
    giornata(Giornata),
    arbitro(Arbitro).

% Vincolo: una squadra non può giocare due volte nella stessa giornata
vincolo_unicita_giornata([]).
vincolo_unicita_giornata([partita(S1, S2, G, _)|Rest]) :-
    \+ (member(partita(S1, _, G, _), Rest); member(partita(_, S1, G, _), Rest)),
    \+ (member(partita(S2, _, G, _), Rest); member(partita(_, S2, G, _), Rest)),
    vincolo_unicita_giornata(Rest).

% Vincolo: ogni arbitro può arbitrare una sola partita per giornata
vincolo_arbitro_unico([]).
vincolo_arbitro_unico([partita(_, _, G, A)|Rest]) :-
    \+ member(partita(_, _, G, A), Rest),
    vincolo_arbitro_unico(Rest).

% Generazione di un calendario valido
calendario(Calendario) :-
    findall/4(partita(S1, S2, G, A), partita(S1, S2, G, A), Partite),
    permutation(Partite, Calendario),
    vincolo_unicita_giornata(Calendario),
    vincolo_arbitro_unico(Calendario).

% Stampa il calendario
stampa_calendario :-
    calendario(Calendario),
    print_calendario(Calendario).

print_calendario([]).
print_calendario([partita(S1, S2, G, A) | Rest]) :-
    format('Partita: ~w vs ~w, Giornata: ~w, Arbitro: ~w~n', [S1, S2, G, A]),
    print_calendario(Rest).

% Query per eseguire la stampa del calendario
:- stampa_calendario.
