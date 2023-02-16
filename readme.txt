REQUISITI PER LA CORRETTA ESECUZIONE:
Pacchetti da installare:
-whoosh
-transformers
-torch
-nltk
Se si vogliono indicizzare documenti, bisogna eseguire il comando "nltk.dowload()", per accertarsi di avere tutti i seguenti pacchetti:
averaged_perceptron_tagger, movie_reviews, names, punkt, state_union, stopwords, twitter_samples, vader_lexicon.
N.B.: il progetto e' stato testato solo su windows e linux ma non dovrebbe dare problemi su qualunque sistema in grado di eseguire file python.

COME ESEGUIRE IL PROGETTO:
Eseguire il file main.py per fare partire l'applicazione assicurandosi di essere all'interno della cartella con i vari file 
python e la cartella 'index'. L'applicazione presenta un menu' testuale dove ci sono 6 opzioni tra cui scegliere (per scegliere 
bisogna inserire il numero relativo all'opzione che si vuole eseguire e premere invio). Le opzioni permettono di creare un 
indice, indicizzare documenti dal file csv, scrivere query e cambiare modello di information retrival.

I risultati delle query vengono stampati su terminale uno alla volta sottoforma di una lista dentro cui si puo' iterare:
viene stampata la prima recensione, con le informazioni su di essa (titolo del manga, autore, 3 sentiment calcolati 
e testo recensione); dopodiche' si può decidere di uscire o proseguire stampando la recensione successiva, questo fino 
all'ultimo risultato dopo il quale si ritorna forzatamente al menu'. Ricordiamo che vengono stampati i risultati fino 
al decimo nel ranking.

Questa applicazione utilizza 3 diversi modelli per calcolare la sentiment value delle recensioni: roBERTa, NLTK e amazon_review_sentiment.
Questa applicazione utilizza 3 diversi modelli di information retrival: BM25, TF_IDF, Frequency.
Di default si usa il modello BM25, ma e' possibile cambiarlo (in base al modello scelto, le query potrebbero dare risultati differenti).

LINGUAGGIO DI QUERY:
Per fare ricerce e' sufficiente inserire uno o piu' campi fra 'title', 'user', 'review', 'sentiment_roberta', 
'sentiment_amazon', 'sentiment_nltk', seguiti da due punti e una serie di valori. E' possibile utilizzare operatori 
booleani (altrimenti tra i vari campi specificati verra' implicitamente inserito un OR), e' possibile specificare un 
certo ordine utilizzando parentesi tonde e sono supportate anche wildcard, boost di un certo valore usando 
il carattere '^' seguito da un numero e le phrase query (tenendo conto pero' che viene applicato stemming ed 
eliminazione delle stopwords quindi il risultato potrebbe essere diverso da quanto previsto).
N.B.: se nessun campo viene specificato per un valore, allora quest'ultimo verra' cercato su tutti i campi.

ESECUZIONE BENCHMARK:
Per eseguire le query di benchmark è stata creata una opzione (la quinta) apposta per semplificare il processo; 
basta seguire l'indicazioni scritte dal menù. Inoltre c'è anche la possibilità di calcolare il DCG delle 
query di benchmark, in fondo al readme ci saranno comunque i DCG calcolati da noi.

DCG CALCOLATI DA NOI:
La nostra scala di valori va da 1 a 3 quindi si passa da un punteggio minimo di 0 ad un punteggio massimo di 15.763483535311375. 
Inoltre per ogni query abbiamo preso in considerazione solo i primi 10 risultati del ranking.

1) 15.061165851291104
2) 11.639918777112372
3) 9.348837372816664
4) 11.580110714822036
5) 14.127548384512831
6) 9.865282106390543
7) 9.883064667196543
8) 12.675569794465977
9) 14.317088904954188
10)12.049731333863209
