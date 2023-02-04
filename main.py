from inverted_index import Inverted_index

index = Inverted_index('indicizzazione')
model = 'BM25'
while True:
    print('----------------------------------')
    print("Menù:\n-Premere 1 per scrivere una query\n-Premere 2 per cambiare modello\n-Premere 3 per creare un nuovo indice")
    print("-Premere 4 per indicizzare dei documenti\n-Premere 5 per uscire")
    print('----------------------------------')
    scelta = input('Scelta: ')
    if scelta == '1':
        query = input("\nInserire la query...\n")
        index.search(query, model)
    elif scelta == '2':
        print('Modelli disponibili:\n1)BM25\n2)TF_IDF\n3)Frequency')
        n_model = input('\nInserire il numero del modello: ')
        if n_model == '1':
            model = 'BM25'
        elif n_model == '2':
            model = 'TF_IDF'
        elif n_model == '3':
            model = 'Frequency'
        else:
            print('Modello non presente\n')
    elif scelta == '3':
        index.create_index()
    elif scelta == '4':
        num_ind = int(input('Inserire il numero di documenti che vuoi indicizzare: '))
        index.index_documents(num_ind)
    elif scelta == '5':
        print("\nUscita in corso...")
        break
    else:
        print("\nTasto non disponibile...")
