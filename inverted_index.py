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
    """A class that implements an inverted index for manga reviews taken from myanimelist.net using the whoosh library.

    The class can create a new inverted index (in the directory specified when initialized), it can index the reviews
    present in the "Reviews_MAL.csv" file and it can search the documents that satisfy a query specified by the user
    using one the three supported models.
    
    Class parameters:
        schema: the whoosh scheme used to create the inverted index
        models: a dictionary with the supported scoring models (BM25, TF_IDF, Frequency)"""

    schema = Schema(title=ID(stored=True),
                    user=ID(stored=True),
                    review=TEXT(analyzer=StemmingAnalyzer(), stored=True), #two version of the review are saved: one is stemmed
                                                                           #and without stopwords for search while the other
                                                                           #is without changes for presentation
                    sentiment_roberta=ID(stored=True),
                    sentiment_amazon=ID(stored=True),
                    sentiment_nltk=ID(stored=True),
                    number_reviews=COLUMN(NumericColumn("i")) #the total number of reviews written by the user who wrote the 
                                                              #review
                    )
    
    models = {'TF_IDF':scoring.TF_IDF(), 'BM25':scoring.BM25F(), 'Frequency':scoring.Frequency()}
                    
    def __init__(self, index_dir):
        """Initializer, it takes as an argument the name of the directory in which to create or open the inverted index."""

        self._index_dir = index_dir

    def create_index(self):
        """Method that creates a new inverted index, with the fields specified by the variable 'schema' in the 'index_dir' 
        variable. If the directory doesn't exist, it will be created."""

        if not os.path.exists(self._index_dir):
            os.mkdir(self._index_dir)

        index.create_in(self._index_dir, Inverted_index.schema)

    def index_documents(self, n_break=-1):
        """Method for indexing the documents contained in csv file 'Reviews_MAL.csv'. This can be a long operation,
        so it's possible to pass as an argument, the number of documents to index in an iteration of the method. 
        It saves in a text file called "csv_count.txt" the position of the last review indexed, so the next time it runs, 
        it starts from there and not from the beginning of the file"""

        if not os.path.exists(self._index_dir):
            print("The index doesn't exist, first you need to create one\n")
        else:
            ix = index.open_dir(self._index_dir)
            writer = ix.writer()
            with open('User_count.pkl', 'rb') as us:
                reviews_count = pickle.load(us) #dictionary with the number of reviews written by every user of MAL

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
                for row in range(csv_counter): #loop used to skip the reviews already indexed
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

    def search(self, query, m_choice = 'BM25'):
        """Method that parses the query(passed as argument), searches and returns a generator with the results. 
        The user can specify which models he wants to use (the default is BM25). The user needs to specify in the query 
        the fields he wants to search. The default operator between fields is an OR and the more fields are present and
        the higher the score will be. The results are sorted in descending order, firstly by their score and secondly 
        according to the total number of reviews written by their user"""

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
                yield len(results)
                for hit in results:
                    yield hit
