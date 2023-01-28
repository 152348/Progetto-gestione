from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer
import os, os.path
from whoosh import index
import csv
from whoosh.qparser import MultifieldParser

class Inverted_index():

    schema = Schema(title=ID(stored=True),
                    user=ID(stored=True),
                    review=TEXT(analyzer=StemmingAnalyzer(), stored=True),
                    sentiment=ID)
                    
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

    def index_documents(self, n_break):
        if not os.path.exists(self._index_dir):
            print("La cartella dell'indice non esiste, esegui prima create_index")
        else:
            ix = index.open_dir(self._index_dir)
            writer = ix.writer()

            try:
                with open('csv_count.txt', 'x') as number:
                    number.write(str(1))
            except FileExistsError:
                pass

            with open('csv_count.txt', 'r') as number:
                csv_counter = int(number.read())

            with open('Reviews_MAL.csv', 'r', encoding='utf8') as rev:
                df = csv.DictReader(rev)
                for row in range(csv_counter):
                    next(df)
                for line in df:
                    writer.add_document(title=line['Title'], user=line['User'], review=line['Text'], _stored_review=line['Text'])
                    csv_counter += 1
                    if csv_counter == n_break:
                        break

            with open('csv_count.txt', 'w') as number:
                number.write(str(csv_counter))

            writer.commit()

    def search(self, query):
        ix = index.open_dir(self._index_dir)
        with ix.searcher() as s:
            parser = MultifieldParser(['title', 'user', 'review', 'sentiment'], schema = Inverted_index.schema)
            parsed_q = parser.parse(query)
            results = s.search(parsed_q)
            if len(results) == 0:
                print("No results found")
            else:
                for result in results:
                    print(result)

