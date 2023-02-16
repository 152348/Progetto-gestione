Pacchetti da installare:
-whoosh
-transformers
-torch
-nltk
Se si vogliono indicizzare documenti, bisogna eseguire il comando "nltk.dowload()", per accertarsi di avere tutti i seguenti pacchetti:
averaged_perceptron_tagger, movie_reviews, names, punkt, state_union, stopwords, twitter_samples, vader_lexicon.


Questa applicazione utilizza 3 diversi modelli per calcolare la sentiment value delle recensioni: roBERTa, NLTK e amazon_review_sentiment.
Questa applicazione utilizza 3 diversi modelli di information retrival: BM25, TF_IDF, Frequency.
Di default si usa il modello BM25, ma e' possibile cambiarlo (in base al modello scelto, le query potrebbero dare risultati differenti).

Eseguire il main per fare partire l'applicazione assicurandosi di essere all'interno della cartella con i vari file python e la cartella 'index'.
L'applicazione presenta un menu' testuale dove ci sono 6 opzioni tra cui scegliere (per scegliere bisogna inserire il numero relativo all'opzione 
che si vuole eseguire e premere invio).
Le opzioni permettono di creare un indice, indicizzare documenti dal file csv, scrivere query e cambiare modello di information retrival.

Per eseguire le query di benchmark è stata creata una opzione (la quinta) apposta per semplificare il processo; basta seguire l'indicazioni scritte dal menù.
Inoltre c'è anche la possibilità di calcolare il DCG delle query di benchmark, in fondo al readme ci saranno comunque i DCG calcolati da noi.

I risultati delle query vengono stampati su terminale uno alla volta sottoforma di una lista in cui si può iterare dentro:
viene stampata la prima recensione, con le informazioni su di essa (titolo del manga, autore, 3 sentiment calcolati e testo recensione);
dopodichè si può decidere di uscire o proseguire stampando la recensione successiva, questo fino all'ultimo risultato dopo il quale si ritorna al menù.
Ricordiamo che vengono stampati i risultati fino al decimo nel ranking.

DCG calcoalti da noi:
1) 15.061165851291104
2) 11.639918777112372(in una ho messo 1, mentre gabriel 2)
3) 9.348837372816664(in una ho messo 1, mentre gabriel 2 e in una ho messo 3, mentre gabriel 1)
4) 11.580110714822036(in una ho messo 2, mentre gabriel 1)
5) 14.127548384512831(in una ho messo 3, mentre gabriel 2)
6) 9.865282106390543(in una ho messo 2, mentre gabriel 3)
7) 9.883064667196543
8) 12.675569794465977
9) 14.317088904954188
10)12.049731333863209
