from inverted_index import Inverted_index

prova = Inverted_index('indicizzazione')
prova.create_index()
prova.index_documents(50)
prova.search("title:'dragon ball' OR user:blandmaster")