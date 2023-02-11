from inverted_index import Inverted_index

index = Inverted_index('indicizzazione')
model = 'BM25'
while True:
    print('----------------------------------')
    print("Menu:\n-Press 1 to write a query\n-Press 2 to change model\n-Press 2 to create a new index")
    print("-Press 4 to index documents\n-Press 5 to exit")
    print('----------------------------------')
    choice = input('Choice: ')
    if choice == '1':
        query = input("\nInsert query...\n")
        index.search(query, model)
    elif choice == '2':
        print('Available models:\n1)BM25\n2)TF_IDF\n3)Frequency')
        n_model = input('\nEnter the model number: ')
        if n_model == '1':
            model = 'BM25'
        elif n_model == '2':
            model = 'TF_IDF'
        elif n_model == '3':
            model = 'Frequency'
        else:
            print('Model not present\n')
    elif choice == '3':
        index.create_index()
    elif choice == '4':
        num_ind = int(input('Enter the number of documents you want to index: '))
        index.index_documents(num_ind)
    elif choice == '5':
        print("\nExit in progress...")
        break
    else:
        print("\nKey not available...")
