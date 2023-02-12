"""Module that implements the terminal user interface of the search engine. The user can write queries and navigate through
the results, change the information retrieval model, create a new inverted index, index an arbitrary number of documents and
try a set of ten benchmark queries for which the user can give a relevance value to calculate the DCG.

Parameters:
    index: instance of the inverted index class
    model: default IR model used by the search engine
    bench_uin: benchmark queries expressed in natural language
    bench_query: benchmark queries expressed with the query language of the search engine
"""
from inverted_index import Inverted_index
from math import log2

def hit_print(hit,position,length):
    """Function to pretty-print the results of query search. For every results, the function prints the ranking number of the 
    review out of the total reviews retrieved, the title of the manga, the user who wrote the review, the results of three 
    sentiment analysis methods performed on the reviews separated by a dash and finally the review itself"""
    print("\n------------------ RESULT ", position, " OUT OF ",length," ------------------\n\n")
    print(f"Title: {hit['title']}, User: {hit['user']}, Sentiments: "
            f"{hit['sentiment_roberta']} - {hit['sentiment_amazon']} - {hit['sentiment_nltk']}\nReview: {hit['review']}\n")

def DCG_calc(relevances):
    """Function that given a list of integers, calculates the Dispositioned cumulative gain using a binary logarithm. Every
    relevance value is divided by the binary logarithm of the ranking position of the review it represents. The function
    assumes that the position in the list reflects the position in the ranking (so the first the value corresponds to the
    first review in the ranking and so on)"""
    DCG = relevances[0]
    for i in range(1,len(relevances)):
        DCG += relevances[i] / log2(i+1)
    return DCG

index = Inverted_index('Index')
model = 'BM25'

bench_uin = ["I want to find all the reviews about the manga \'naruto\' that have from 3 stars to 5 stars",
"I want to find the reviews about a manga whose name I remember starts with \'Dra\' and is about fighting," 
"the protagonist's name is goku, he has a tail and can transform", "I want to find all the reviews about"
"\'Chainsaw man\' that are either written by \'skylucario\' or that are negative", "I want to find reviews" 
"about alchemy-themed mangas aside from \'fullmetal alchemist\' which I already read", "I want to find" 
"reviews about historical mangas, especially about samurais", "I want to find all reviews about \'fairy tail\'" 
"that communicate anger or sadness", "I want to find all the reviews about action mangas that are set in " 
"either of the World War", "I want to find all the reviews about mangas that have spiders and monsters",
"I want to read the 5 stars reviews written by the user \'abystoma\' but I don’t remember the number his username ends with",
"I want to find reviews of mangas about magic or elves that have neutral reviews"]

bench_query = ["title:naruto AND sentiment_amazon:[\'3 stars\' TO \'5 stars\']", "title:dra* AND review:fighting,goku,tail,"
"transform", "title:\'chainsaw man\' AND (user:skylucario OR sentiment_nltk:negative)", "NOT title:\'fullmetal alchemist\'" 
"AND review:alchemy AND" "NOT review:\'fullmetal alchemist\'", "review:historical^2,samurai", "title:\'fairy tail\' AND" 
"(sentiment_roberta:anger sentiment_roberta:sadness)", "review:(action AND \"world war\")", "review:spiders AND monsters",
"user:abystoma? AND sentiment_amazon:\'5 stars\'", "(review:magic review:elves) AND sentiment_nltk:neutral"]

while True:
    print('-------------------------------------')
    print("Menù:\n-Press 1 to write a query\n-Press 2 to change model\n-Press 3 to create a new index")
    print("-Press 4 to index some documents\n-Press 5 to try the benchmark queries\n-Press 6 to exit")
    print('-------------------------------------')
    choice = input('Choice: ')

    if choice == '1':
        query = input("\nEnter the query...\n")
        results = index.search(query, model)
        length = next(results) #variable that stores the total number of documents retrieved
        if length == 0:
            print("\nNo results found\n")
        else:
            position = 1 #variable that stores the position of the current document in the ranking
            for hit in results:
                hit_print(hit, position, length)
                progress = input("\n-Press 1 to proceed to the next result\n-Press 2 to return to the menù\n")
                if progress == '1':
                    position += 1
                    continue
                elif progress == '2':
                    position += 1
                    break
                else:
                    position += 1
                    print("Key not available...")
                    break
            if position >= 11:
                print("\nEnd of list..")
            print("\nReturning to the menù...")

    elif choice == '2':
        print('Available models:\n1)BM25\n2)TF_IDF\n3)Frequency')
        n_model = input('\nEnter what model you want: ')
        if n_model == '1':
            model = 'BM25'
        elif n_model == '2':
            model = 'TF_IDF'
        elif n_model == '3':
            model = 'Frequency'
        else:
            print('Model not present\n')

    elif choice == '3':
        confirm = input('Are you sure you want to create a new index?: ')
        if confirm.lower() == 'yes':
            index.create_index()

    elif choice == '4':
        try:
            ind_num = int(input('Enter the number of documents you want to index: '))
        except ValueError:
            print("\nYou have to enter a positive value!")
            continue
        if ind_num <= 0 :
            print("\nYou have to enter a positive value!")
            continue
        index.index_documents(ind_num)

    elif choice == '5':
        print("Available benchmark queries:\n")
        for i,query in enumerate(bench_uin):
            print(i+1,") ",query,sep='')
        try:
            q_choice = int(input("\nEnter the query you want to try: ")) - 1
        except ValueError:
            print("Query not available")
            continue
        if q_choice < 0 or q_choice > 9:
            print("Query not available")
            continue
        print(bench_query[q_choice])
        dcg_choice = input("Do you want to calculate the DCG?: ").lower()
        if dcg_choice == 'yes':
            dcg_choice = True
        elif dcg_choice == 'no':
            dcg_choice = False
        else:
            print("\nChoice not supported... DCG will not be calculated")
            dcg_choice = False
        results = index.search(bench_query[q_choice], model)
        length = next(results)
        position = 1
        relevances = [] #list that will store the relevance values decided by the user
        for hit in results:
            hit_print(hit, position, length)
            if dcg_choice:
                try:
                    relevance = int(input("\nWhat relevance do you think this result has with regards to the UIN " 
                    "on a scale of 1 to 3?: "))
                except ValueError:
                    print("\nIncorrect relevance value, exiting the benchark...")
                    break
                if relevance < 1 or relevance > 3:
                    print("\nIncorrect relevance value, exiting the benchmark...")
                    break
                relevances.append(relevance)
            progress = input("\n-Press 1 to proceed to the next result\n-Press 2 to return to the menù\n")
            if progress == '1':
                position += 1
                continue
            elif progress == '2':
                position += 1
                break
            else:
                position += 1
                print("Key not available...\n")
                break
        if position >= 11:
            print("\nEnd of list..")
            if dcg_choice:
                print("\nThe DCG is", DCG_calc(relevances))
        print("\nReturning to the menù...")

    elif choice == '6':
        print("Exiting...")
        break

    else:
        print("\nKey not available...") 
