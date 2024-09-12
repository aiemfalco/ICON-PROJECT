# SISTEMA PER LA PREVISIONE DI RISULTATI CALCISTICI (Progetto di Ingegneria della Conoscenza a.a 2023/2024)

L'obiettivo dell'applicativo è quello di prevedere il risultato di un match tra due squadre inserite dall'utente, considerando i dati a disposizione e le caratteristiche del match (quale squadra gioca in casa e quale in trasferta, quante partite ha vinto negli anni, le sue prestazioni recenti e altre informazioni).
Il nostro è un problema di classificazione quindi utilizziamo modelli per la classificazione. Difatti l'obiettivo è prevedere l'esito del match tra tre possibili classi (W-D-L, ossia Win, Draw, Lose).
I dati che abbiamo a disposizione provengono da un dataset trovato in rete, su cui è stato fatto preprocessing e cleaning. Successivamente è stata creata una ontologia che è possibile interrogare, che è stata utile per estrapolare una nuova colonna che è poi aggiunta al dataset. Quest'ultima ci riassume gli ultimi 5 esiti delle ultime 5 partite precedenti a quella analizzata dal punto di vista della squadra considerata. 
Questa colonna è servita per ottenere una maggiore accuratezza nella previsione del risultato. 
Dopo aver eseguito queste operazioni che sostanzialmente modificavano e rendevano il dataset più conforme alle nostre esigenze, abbiamo iniziato a lavorare sul sistema di apprendimento supervisionato, in particolare utilizzando due modelli che si basano su due approcci diversi: il Random Forest Classifier (modello basato sull'approccio di bagging) e l'AdaBoost Classifier (modello basato sull'approccio di boosting) mettendoli a confronto sui risultati ottenuti.
È Inoltre presente una seconda feature in grado di sfruttare una soluzione basata sul soddisfacimento di vincoli (CSP) per risolvere il problema della generazione di un calendario per un campionato calcistico.
Nel nostro problema, le variabili sono:
- i nomi delle squadre di calcio: 20 squadre selezionate in maniera casuale tra le 26 a disposizione. 
- i nomi degli arbitri: vengono selezionati 10 arbitri a giornata tra i 61 disponibili nel intero dataset.
- le giornate del campionato: una lista di interi da 1 a 38 (19 giornate di andata e 19 giornate di ritorno).

I dati che popolano queste liste vengono prese direttamente dal dataset.
I vincoli che abbiamo imposto sono 4:
 
- tutte le squadre e gli arbitri devono essere diversi in ogni giornata.
- una squadra non può affrontare sé stessa.
- in ogni giornata non devono esserci ripetizioni di squadre, una squadra gioca una volta per giornata.
- Le partite di ritorno devono essere con le squadre invertite e a distanza di 19 giornate (Roma-Juventus giornata 1 (andata) si sfideranno di nuovo nella giornata 20 (ritorno) in Juventus-Roma)

## Indice

- [Installazione](#Installazione)
- [Uso](#Uso)
- [Contributors](#Contributors)



## Installazione

Per eseguire l'applicativo sono necessarie numerose librerie che vengono elencate nel file requirements.txt che si può trovare nella cartella root, per cui il primo step prima di avviare il programma è quello di scrivere sul terminale di Visual Studio il comando:
pip install -r requirements.txt

## Uso

Successivamente si potrà avviare il programma dal main.py e seguirà la stampa a terminale del menu in cui sarà possibile scegliere il task da eseguire.

## Contributors

| Nome               | Ruolo             | GitHub                                               |
|--------------------|-------------------|------------------------------------------------------|
| Fabio Falcone      | Sviluppatore      | [Fabio Falcone](https://github.com/aiemfalco)        |
| Raffaele Arbues    | Sviluppatore      | [Raffaele Arbues](https://github.com/RaffaeleArbues) |
| Corrado Cristallo  | Sviluppatore      | [Corrado Cristallo](https://github.com/SamfistZg)    |
