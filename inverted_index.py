from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.analysis import StemmingAnalyzer
import os, os.path
from whoosh import index

class Inverted_index():

    schema = Schema(title=ID(stored=True,lowercase=True),
                    user=ID(stored=True),
                    review=TEXT(analyzer=StemmingAnalyzer()),
                    _review=STORED,
                    sentiment=ID)
                    
    def __init__(self, index_dir):
        """Inizializzatore a cui deve essere passato il nome della directory 
            in cui creare o aprire l'inverted index"""
        _index_dir = index_dir

    def create_index(self):
        """Metodo che si occupa di creare l'inverted index con i campi
            specificati dalla variabile schema"""
        if not os.path.exists(self._index_dir):
            os.mkdir(self._index_dir)

        ix = index.create_in(self._index_dir, Inverted_index.schema)

    def index_documents(self):
        pass

    def open_index(self):
        pass
