import csv
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.sentiment import SentimentIntensityAnalyzer


# nltk.download()   # serve per scaricare alcuni pacchetti di nltk che servono, ti viene scritto sul terminale quali ti servono
# principali: names, stopwords, state_union, twitter_samples, movie_reviews, averaged_perceptron_tagger, vader_lexicon, punkt, vader_lexicon
# link da seguire https://realpython.com/python-nltk-sentiment-analysis/
# usiamo NLTK per fare la sentiment analysis
# da quello che vedo, bisogna guardare il valore di compound per capire il sentimeno, è complicato
def nltk_sentiment(string):
    analyzer = SentimentIntensityAnalyzer()  # analizzatore base di nltk
    sentiment = analyzer.polarity_scores(string)
    if (sentiment['compound'] < 0):
        risultato = "negativa"
    else:
        if (sentiment['neu'] > 0.770):
            risultato = "neutrale"
        else:
            risultato = "positiva"
    return risultato


# funzione generale che fa partire la sentiment di un modello in tutti gli 8 modi
# si potrebbe eseguire anche lo splitting con tutte le tokenizzazioni diverse, ma attualmente mi sembra ci siano già troppi print da leggere.
def extraction(string, model_name):
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    sentiment = splitting(string, tokenizer, model)
    # sentiment = truncation(string, tokenizer, model)
    return sentiment


# # risultato di sentiment attraverso il troncamento, il modello dipende da quello che gli viene passato
# def truncation(string, tokenizer, model):
#     inputs = tokenizer(string, truncation=True, max_length=512, return_tensors="pt")
#     with torch.no_grad():
#         logits = model(**inputs).logits
#     # logits è una particolare struttura dati, simile ad una lista di liste, per lavorarci ci sono apposite funzioni,
#     # vengono utilizzate nello stesso modo, ma cambiano la loro manipolazione di dati in base al modello di Hugging face(se supportato)
#     predicted_class_id_1 = logits.argmax().item()  # funzione che trova l'ID col valore maggiore
#     return model.config.id2label[predicted_class_id_1]  # funzione per ottenere il nome(stringa) del sentimento dall'ID


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
    return model.config.id2label[predicted_class_id_1]


# preso spunto dalla funzione "index_documents" per la lettura del file csv,
# il resto sono print che verrano tolti in futuro e le chiamate delle funzioni
def sentiment_analysis(string):
    sentimento = [extraction(string, "j-hartmann/emotion-english-distilroberta-base"),
                  extraction(string, "LiYuan/amazon-review-sentiment-analysis"),
                  nltk_sentiment(string)]
    # ritorna una lista con i sentimenti dei vari modelli -> [roBERTa, ARSA, NLTK]
    return sentimento
