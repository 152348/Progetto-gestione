from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer
import os, os.path
from whoosh import index
import csv
from whoosh.qparser import MultifieldParser
from whoosh import qparser
from whoosh import scoring
from sentiment import sentiment_analysis
from whoosh.highlight import UppercaseFormatter

class Inverted_index():

    schema = Schema(title=ID(stored=True),
                    user=ID(stored=True),
                    review=TEXT(analyzer=StemmingAnalyzer(), stored=True),
                    sentiment_roberta=ID(stored=True),
                    sentiment_amazon=ID(stored=True),
                    sentiment_nltk=ID(stored=True))
                    
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
            print("La cartella dell'indice non esiste, esegui prima create_index")
        else:
            ix = index.open_dir(self._index_dir)
            writer = ix.writer()

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
                    sentiment_nltk=sentiments[2])
                    csv_counter += 1
                    break_counter +=1
                    with open('csv_count.txt', 'w') as number:
                        number.write(str(csv_counter))
                    if break_counter != 1 and break_counter == n_break:
                        break

            writer.commit(optimize=True)

    def search(self, query):
        """Metodo che si occupa di parsare la query passata come parametro dall'utente, cercarla e 
           stampare i risultati"""
        ix = index.open_dir(self._index_dir)
        with ix.searcher() as s:
            og = qparser.OrGroup.factory(0.9)
            parser = MultifieldParser(['title', 'user', 'review', 'sentiment_roberta', 'sentiment_amazon', 'sentiment_nltk'],
                schema = Inverted_index.schema, group = og)
            parsed_q = parser.parse(query)
            results = s.search(parsed_q, terms= True)
            #results.formatter = UppercaseFormatter(between="\n")
            if len(results) == 0:
                print("No results found")
            else:
                for hit in results:
                    print(f"Title: {hit['title']}, User: {hit['user']}, Sentiments: "
                    f"{hit['sentiment_roberta']}-{hit['sentiment_amazon']}-{hit['sentiment_nltk']}, Review: {hit['review']}\n")
                #for hit in results:
                    #print(hit.highlights("review"))

