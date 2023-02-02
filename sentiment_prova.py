import csv
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.sentiment import SentimentIntensityAnalyzer


# questo file è a sè, quindi puoi farlo partire da solo intanto per vedere i print e tutto,
# sarà poi da modificare per finalizzarlo(togliere print e codice superfluo, ottimizzare i return,
# riguardare tutta la parte dei commenti e pensare se tradurli in inglese).
# Sarà infine da integrare(in inverted_index.py) o da metterci un return finale, per inserire il sentimento dentro all'inverted index

# attualmente sto usando 3 modelli(roBERTa, ARSA, NTLK), per ogni modello di Hugging face provo 2 metodi diversi(splitting e troncamento),
# per il troncamento utilizzo 7 manipolazioni di dati differenti(anche per NLTK):
# (base del modello, stemming, lemmatization, base di nltk, senza punteggiaturae di nltk, senza stopworde di nltk, senza entrambee di nltk)
# e per ogni esecuzione ritorno i primi 2 sentimenti maggiori(non per NLTK).

# c'è anche il codice commentato per utilizzare le varie tokenizzazioni nello splitting,
# non lo lascio perchè c'è già molta roba da leggere e diventa pensante, se vuoi provarlo basta togliere i commenti(dentro la funzione extraction)

# nomi dei modelli di Hugging face che attualemnte funzionano in extraction:
# "j-hartmann/emotion-english-distilroberta-base"
# "LiYuan/amazon-review-sentiment-analysis"


# nltk.download()   # serve per scaricare alcuni pacchetti di nltk che servono, ti viene scritto sul terminale quali ti servono
# principali: names, stopwords, state_union, twitter_samples, movie_reviews, averaged_perceptron_tagger, vader_lexicon, punkt, vader_lexicon
# link da seguire https://realpython.com/python-nltk-sentiment-analysis/
# usiamo NLTK per fare la sentiment analysis
# da quello che vedo, bisogna guardare il valore di compound per capire il sentimeno, è complicato
def nltk_sentiment(string):
    print("\nNLTK...")
    analyzer = SentimentIntensityAnalyzer()  # analizzatore base di nltk
    sentiment = analyzer.polarity_scores(string)
    print("base -> ", sentiment)
    sentiment = analyzer.polarity_scores(stemming(string))
    print(sentiment)
    sentiment = analyzer.polarity_scores(lemmatization(string))
    print(sentiment)
    testo_nltk = tokenization_nltk(string)
    for item in testo_nltk:
        print(item[0], "nltk ->", sep='_', end=' ')
        sentiment = analyzer.polarity_scores(item[1])
        print(sentiment)
    return sentiment


# funzione generale che fa partire la sentiment di un modello in tutti gli 8 modi
# si potrebbe eseguire anche lo splitting con tutte le tokenizzazioni diverse, ma attualmente mi sembra ci siano già troppi print da leggere.
def extraction(string, model_name):
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    print('\n', model_name, "...", sep='')
    sentimento = splitting(string, tokenizer, model)
    # qui sotto c'è il codice se si volesse provare anche lo splitting con tutte le varie tokenizzazioni,
    # si può riformattare il codice per avere print diversi in base alle prenferenze, lo lascio così perchè non so nemmeno se lo useremo
    # sentimento = splitting(stemming(string), tokenizer, model)
    # sentimento = splitting(lemmatization(string), tokenizer, model)
    # testo_nltk = tokenization_nltk(string)
    # for item in testo_nltk:
    #     print(item[0], "nltk ->", sep='_', end=' ')
    #     sentimento = splitting(item[1], tokenizer, model)
    sentimento = truncation(string, tokenizer, model)
    sentimento = truncation(stemming(string), tokenizer, model)
    sentimento = truncation(lemmatization(string), tokenizer, model)
    testo_nltk = tokenization_nltk(string)
    for item in testo_nltk:
        print(item[0], "nltk ->", sep='_', end=' ')
        sentimento = truncation(item[1], tokenizer, model)
    return sentimento


# facciamo noi la tokenizzazione con stemming -> ritorna il testo stemmato
def stemming(string):
    porter = PorterStemmer()
    tokens = nltk.word_tokenize(string)
    count = 0
    for t in tokens:
        if count >= 510:
            break
        if t not in nltk.corpus.stopwords.words('english'):
            if count == 0:
                nuovo_testo_stem = t
            else:
                nuovo_testo_stem = nuovo_testo_stem + ' ' + porter.stem(t)
            count = count + 1
    print("stemming ->", end=' ')
    return nuovo_testo_stem


# i cicli for di queste 2 funzioni sono diversi da quello di nltk, in quello di nltk ho un whitespace ad inizio testo.
# semplicemente è più facile e pulito come codice e non penso cambi molto ad avere un whitespace in più
# facciamo noi la tokenizzazione con lemmatization -> ritorna il testo lemmatizato
def lemmatization(string):
    wnl = nltk.WordNetLemmatizer()
    tokens = nltk.word_tokenize(string)
    count = 0
    for t in tokens:
        if count >= 510:
            break
        if t not in nltk.corpus.stopwords.words('english'):
            if count == 0:
                nuovo_testo_lemma = t
            else:
                nuovo_testo_lemma = nuovo_testo_lemma + ' ' + wnl.lemmatize(t)
            count = count + 1
    print("lemmatize ->", end=' ')
    return nuovo_testo_lemma


#  metodo per tokenizzare tramite ntlk -> ritorna una lista di 4 liste,
#  ognuna con il nome del metodo usato(per stamparlo col print dopo, non servirà in futuro) e il testo ottenuto
def tokenization_nltk(string):
    tokens = nltk.word_tokenize(string, language="english")  # tokenizer di nltk base
    alpha_tokens = [t for t in tokens if t.isalpha()]  # rimossa solo la punteggiatura
    stop_tokens = [t for t in tokens
                   if t.lower() not in nltk.corpus.stopwords.words("english")]  # rimossa solo le stopwords
    both_tokens = [t for t in alpha_tokens
                   if
                   t.lower() not in nltk.corpus.stopwords.words("english")]  # rimosse sia stopwords, sai punteggiatura
    metodi = [
        ["tokens", tokens], ["alpha_tokens", alpha_tokens], ["stop_tokens", stop_tokens], ["both_tokens", both_tokens]
    ]
    for item in metodi:  # for solo per iterare tra i 4 metodi
        new_string = ' '
        for word in item[1]:  # for importante per creare la stringa(dalla lista di token)
            new_string += word + ' '
        item[1] = new_string
    return metodi


# risultato di sentiment attraverso il troncamento, il modello dipende da quello che gli viene passato
def truncation(string, tokenizer, model):
    inputs = tokenizer(string, truncation=True, max_length=512, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    # logits è una particolare struttura dati, simile ad una lista di liste, per lavorarci ci sono apposite funzioni,
    # vengono utilizzate nello stesso modo, ma cambiano la loro manipolazione di dati in base al modello di Hugging face(se supportato)
    predicted_class_id_1 = logits.argmax().item()  # funzione che trova l'ID col valore maggiore
    logits[
        0, logits.argmax()] = 0  # questo mi serve solo per ottenere il secondo ID col valore maggiore, in futuro andrà tolto
    predicted_class_id_2 = logits.argmax().item()  # secondo ID
    sentimento = model.config.id2label[
        predicted_class_id_1]  # funzione per ottenere il nome(stringa) del sentimento dall'ID
    sentimento_secondario = model.config.id2label[predicted_class_id_2]  # idem per il secondo
    print("truncation -> ", sentimento, " and ", sentimento_secondario)
    return [sentimento, sentimento_secondario]


# risultato di sentiment attraverso lo splitting, il modello dipende da quello che gli viene passato
def splitting(string, tokenizer, model):
    tokens = tokenizer.encode_plus(string, add_special_tokens=False, return_tensors='pt')
    input_id_chunks = tokens['input_ids'][0].split(510)
    mask_chunks = tokens['attention_mask'][0].split(510)
    input_id_chunks = list(input_id_chunks)  # cambio in lista, perchè normalmente sono tuple
    mask_chunks = list(mask_chunks)
    for i in range(len(input_id_chunks)):
        #  this is for adding the input_ids for start and finish sequence, and for mask_ids
        input_id_chunks[i] = torch.cat([
            torch.Tensor([101]), input_id_chunks[i], torch.Tensor([102])
        ])
        mask_chunks[i] = torch.cat([
            torch.Tensor([1]), mask_chunks[i], torch.Tensor([1])
        ])
        #  this is for padding the sequences
        pad_len = 512 - input_id_chunks[i].shape[0]
        # check if tensor length satisfies required chunk size
        if pad_len > 0:
            # if padding length is more than 0, we must add padding
            input_id_chunks[i] = torch.cat([
                input_id_chunks[i], torch.Tensor([0] * pad_len)
            ])
            mask_chunks[i] = torch.cat([
                mask_chunks[i], torch.Tensor([0] * pad_len)
            ])
    if len(input_id_chunks) > 1:  # print per vedere quali recensioni contenevano più di 512 token, andrà tolto in futuro
        print("recensione splittata")
    # nello splitting usiamo le funzioni di torch, non ho ben capito perchè
    # queste tre righe mi servono per avere un dizionario con il tensor dentro(simile al troncamento),
    # che dovremo estrarre per ottenere i valori e farci la media
    input_ids = torch.stack(input_id_chunks)
    attention_mask = torch.stack(mask_chunks)
    input_dict = {
        'input_ids': input_ids.long(),
        'attention_mask': attention_mask.int()
    }
    outputs = model(**input_dict)  # stessa cosa del troncamento
    probs = torch.nn.functional.softmax(outputs[0], dim=-1)  # estrazione dei tensor
    mean = probs.mean(
        dim=0)  # fa la media dei valori dentro ai tensor, se ne abbiamo più di uno(caso in cui testo ha più di 512 token)
    # queste di seguito sono uguali al troncamento
    predicted_class_id_1 = torch.argmax(mean).item()
    mean[torch.argmax(mean)] = 0
    predicted_class_id_2 = torch.argmax(mean).item()
    sentimento = model.config.id2label[predicted_class_id_1]
    sentimento_secondario = model.config.id2label[predicted_class_id_2]
    print("splitting -> ", sentimento, " and ", sentimento_secondario)
    return [sentimento, sentimento_secondario]


# preso spunto dalla funzione "index_documents" per la lettura del file csv,
# il resto sono print che verrano tolti in futuro e le chiamate delle funzioni
def sentiment_analysis():
    n_break = 2
    try:
        with open('csv_count.txt', 'x') as number:
            number.write(str(0))
    except FileExistsError:
        pass

    # with open('csv_count.txt', 'r') as number:
    #     csv_counter = int(number.read())
    csv_counter = 0

    with open('Reviews_MAL.csv', 'r', encoding='utf8') as rev:
        break_counter = 0
        df = csv.DictReader(rev)
        for row in range(csv_counter):
            next(df)
        for line in df:
            testo = line['Text']
            #  print per confrontare
            print('\n', line['Title'].lower(), ' | ', line['User'], '\n', line['Rating'], ' ', line['Recommendation'])
            sentimento = extraction(testo, "j-hartmann/emotion-english-distilroberta-base")
            sentimento = extraction(testo, "LiYuan/amazon-review-sentiment-analysis")
            sentimento = nltk_sentiment(testo)
            # attualmente sentimento(il return dei modelli) è una lista(extraction) o dizionario(nltk_sentiment).
            # in futuro dovremmo pensare a come lo vogliamo(se solo una stringa o altro),
            # perchè dovremmo poi inserirlo nell'inverted index
            csv_counter += 1
            break_counter += 1
            with open('csv_count.txt', 'w') as number:
                number.write(str(csv_counter))
            if break_counter != 1 and break_counter == n_break:
                break


sentiment_analysis()  # chiamata di funzione principale che verrà tolta(sarà il main a chiamarla)
