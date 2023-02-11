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

    models = {'TF_IDF': scoring.TF_IDF(), 'BM25': scoring.BM25F(), 'Frequency': scoring.Frequency()}

    def __init__(self, index_dir):
        """Initializer, it takes the name of the directory, in which to create or open the inverted index, as an argument"""
        self._index_dir = index_dir

    def create_index(self):
        """Method that create the inverted index, with the fields specified by the variable schema"""
        if not os.path.exists(self._index_dir):
            os.mkdir(self._index_dir)

        index.create_in(self._index_dir, Inverted_index.schema)

    def index_documents(self, n_break=-1):
        """Method for indexing the documents contained in csv file Reviews_MAL.csv. This can be a long operation,
        so it's possible to pass as argument, the number of documents to index in this iteration of the method
        (or -1 to index all the file). It saves in a file the position of the last review indexed,
        so the next time it runs, it starts from there and not from the beginning of the file"""
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
                                        _stored_review=line['Text'], sentiment_roberta=sentiments[0],
                                        sentiment_amazon=sentiments[1],
                                        sentiment_nltk=sentiments[2], number_reviews=reviews_count[line['User']])
                    csv_counter += 1
                    break_counter += 1
                    with open('csv_count.txt', 'w') as number:
                        number.write(str(csv_counter))
                    if n_break != -1 and break_counter == n_break:
                        break

            writer.commit(optimize=True)

    def search(self, query, m_choice):
        """Method that parse the query(passed as argument), searches and prints the results"""
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
                results = s.search(parsed_q, sortedby=[scores, numb_review])
                # results.formatter = UppercaseFormatter(between="\n")
                total = len(results)
                if total == 0:
                    print("\nNo results found\n")
                else:
                    count = 1
                    for hit in results:
                        print("\n------------------ REVIEW ", count, "OUT OF ", total, "TOTAL ------------------\n\n")
                        print(f"Title: {hit['title']}, User: {hit['user']}, Sentiments: "
                              f"{hit['sentiment_roberta']} - {hit['sentiment_amazon']} - {hit['sentiment_nltk']}\nReview: {hit['review']}\n")
                        choice = input("-press 1 to see next result\n-press 2 to return to the menu\n")
                        if choice == '1':
                            count += 1
                            continue
                        elif choice == '2':
                            break
                        else:
                            print("key not available...")
                    if count == total + 1:
                        print("REACHED END OF LIST...\n")
                    print("returning to menu...\n")
