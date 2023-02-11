from inverted_index import Inverted_index
from math import log2

def hit_print(hit,count,length):
    print("\n------------------ RESULT ", count, " OUT OF ",length," ------------------\n\n")
    print(f"Title: {hit['title']}, User: {hit['user']}, Sentiments: "
            f"{hit['sentiment_roberta']} - {hit['sentiment_amazon']} - {hit['sentiment_nltk']}\nReview: {hit['review']}\n")

def DCG_calc(relevances):
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
    print('----------------------------------')
    print("Menù:\n-Press 1 to write a query\n-Press 2 to change model\n-Press 3 to create a new index")
    print("-Press 4 to index some documents\n-Press 5 to try the benchmark queries\n-Press 6 to exit")
    print('----------------------------------')
    choice = input('Choice: ')
    if choice == '1':
        query = input("\nEnter the query...\n")
        results = index.search(query, model)
        length = next(results)
        if length == 0:
            print("\nNo results found\n")
        else:
            count = 1
            for hit in results:
                hit_print(hit, count, length)
                spostamento = input("-Press 1 to proceed to the next result\n-Press 2 to return to the menù\n")
                if spostamento == '1':
                    count += 1
                    continue
                elif spostamento == '2':
                    break
                else:
                    print("Key not available...")
                    break
            if count >= 11:
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
        num_ind = int(input('Enter the number of documents you want to index: '))
        index.index_documents(num_ind)
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
        results = index.search(bench_query[q_choice], 'BM25')
        length = next(results)
        count = 1
        relevances = []
        for hit in results:
            hit_print(hit, count, length)
            try:
                relevance = int(input("\nWhat relevance do you think this result has with regards to the UIN " 
                "on a scale of 1 to 3?: "))
            except ValueError:
                print("Incorrect relevance value, exiting the benchark...\n")
                continue
            if relevance < 1 or relevance > 3:
                print("Incorrect relevance value, exiting the benchmark...\n")
            relevances.append(relevance)
            spostamento = input("\n-Press 1 to proceed to the next result\n-Press 2 to return to the menù\n")
            if spostamento == '1':
                count += 1
                continue
            elif spostamento == '2':
                count += 1
                break
            else:
                count += 1
                print("Key not available...")
                break
        if count >= 11:
            DCG = DCG_calc(relevances)
            print("\nEnd of list..\nThe DCG is:", DCG)
        print("\nReturning to the menù...")
    elif choice == '6':
        print("\nExiting...")
        break
    else:
        print("\nKey not available...") 
