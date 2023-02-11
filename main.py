from inverted_index import Inverted_index

index = Inverted_index('Index')
model = 'BM25'
while True:
    print('----------------------------------')
    print("Menù:\n-Press 1 to write a query\n-Press 2 to change model\n-Press 3 to create a new index")
    print("-Press 4 to index some documents\n-Press 5 to exit")
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
                print("\n------------------ RESULT ", count, " OUT OF ",length," ------------------\n\n")
                print(f"Title: {hit['title']}, User: {hit['user']}, Sentiments: "
                    f"{hit['sentiment_roberta']} - {hit['sentiment_amazon']} - {hit['sentiment_nltk']}\nReview: {hit['review']}\n")
                spostamento = input("-Press 1 to proceed to the next result\n-Press 2 to return to the menù\n")
                if spostamento == '1':
                    count += 1
                    continue
                elif spostamento == '2':
                    break
                else:
                    print("Key not available... returning to menù\n")
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
        print("\nExiting...")
        break
    else:
        print("\nKey not available...")
