from whoosh.fields import Schema, TEXT, ID, COLUMN
from whoosh.columns import NumericColumn
from whoosh.analysis import StemmingAnalyzer
import os, os.path
from whoosh import index
import csv
from whoosh.qparser import MultifieldParser
from whoosh import qparser
from whoosh import scoring
from sentiment import sentiment_analysis
import pickle
from whoosh.sorting import ScoreFacet, FieldFacet


class Inverted_index():

    schema = Schema(title=ID(stored=True),
                    user=ID(stored=True),
                    review=TEXT(analyzer=StemmingAnalyzer(), stored=True),
                    sentiment_roberta=ID(stored=True),
                    sentiment_amazon=ID(stored=True),
                    sentiment_nltk=ID(stored=True),
                    number_reviews=COLUMN(NumericColumn("i"))
                    )
    
    models = {'TF_IDF':scoring.TF_IDF(), 'BM25':scoring.BM25F(), 'Frequency':scoring.Frequency()}
                    
    def __init__(self, index_dir):
        """Inizializzatore a cui deve essere passato il nome della directory 
            in cui creare o aprire l'inverted index"""
        self._index_dir = index_dir

    def create_index(self):
        """Metodo che si occupa di creare l'inverted index con i campi
            specificati dalla variabile schema"""
        if not os.path.exists(self._index_dir):
            os.mkdir(self._index_dir)

        index.create_in(self._index_dir, Inverted_index.schema)

    def index_documents(self, n_break=-1):
        """Metodo che si occupa di indicizzare i documenti contenuti nel file csv Reviews_MAL.csv. Essendo
        un'operazione lunga, è possibile passare come parametro il numero di documenti da indicizzare
        per questa iterazione del metodo (oppure -1 per indicizzarli tutti in una volta). Il metodo non 
        riparte ogni volta dalla prima recensione ma salva in un file a quale recensione era arrivato."""
        if not os.path.exists(self._index_dir):
            print("The index doesn't exist, first you need to create one\n")
        else:
            ix = index.open_dir(self._index_dir)
            writer = ix.writer()
            with open('User_count.pkl', 'rb') as us:
                reviews_count = pickle.load(us)

            try:
                with open('csv_count.txt', 'x') as number:
                    number.write(str(0))
            except FileExistsError:
                pass

            with open('csv_count.txt', 'r') as number:
                csv_counter = int(number.read())

            with open('Reviews_MAL.csv', 'r', encoding='utf8') as rev:
                break_counter = 0
                df = csv.DictReader(rev)
                for row in range(csv_counter):
                    next(df)
                for line in df:
                    sentiments = sentiment_analysis(line['Text'])
                    writer.add_document(title=line['Title'].lower(), user=line['User'], review=line['Text'], 
                    _stored_review=line['Text'], sentiment_roberta=sentiments[0], sentiment_amazon = sentiments[1],
                    sentiment_nltk=sentiments[2], number_reviews = reviews_count[line['User']])
                    csv_counter += 1
                    break_counter +=1
                    with open('csv_count.txt', 'w') as number:
                        number.write(str(csv_counter))
                    if n_break != -1 and break_counter == n_break:
                        break

            writer.commit(optimize=True)

    def search(self, query, m_choice):
        """Metodo che si occupa di parsare la query passata come parametro dall'utente, cercarla e
           stampare i risultati"""
        if not os.path.exists(self._index_dir):
            print("The index doesn't exist, first you need to create one\n")
        else:
            ix = index.open_dir(self._index_dir)
            with ix.searcher(weighting=Inverted_index.models[m_choice]) as s:
                og = qparser.OrGroup.factory(0.9)
                parser = MultifieldParser(
                    ['title', 'user', 'review', 'sentiment_roberta', 'sentiment_amazon', 'sentiment_nltk'],
                    schema=Inverted_index.schema, group=og)
                parsed_q = parser.parse(query)
                numb_review = FieldFacet("number_reviews", reverse=True)
                scores = ScoreFacet()
                results = s.search(parsed_q, sortedby=[scores,numb_review])
                # results.formatter = UppercaseFormatter(between="\n")
                totale = len(results)
                if totale == 0:
                    print("\nNo results found\n")
                else:
                    count = 1
                    for hit in results:
                        print("\n------------------ RISULTATO ", count, "SU ", totale, "TOTALI ------------------\n\n")
                        print(f"Title: {hit['title']}, User: {hit['user']}, Sentiments: "
                            f"{hit['sentiment_roberta']} - {hit['sentiment_amazon']} - {hit['sentiment_nltk']}\nReview: {hit['review']}\n")
                        spostamento = input("-premere 1 per passare al prossimo risultato\n-premere 2 per tornare al menù\n")
                        if spostamento == '1':
                            count += 1
                            continue
                        elif spostamento == '2':
                            break
                        else:
                            print("tasto non disponibile...")
                    if count == totale + 1:
                        print("LISTA FINITA...\n")
                    print("ritorno al menù...\n")
