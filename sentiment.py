import csv
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.sentiment import SentimentIntensityAnalyzer


# nltk.download()   # remove comment, if you need to dowload certain nltk packages
# main packages: names, stopwords, state_union, twitter_samples, movie_reviews, averaged_perceptron_tagger, vader_lexicon, punkt, vader_lexicon
def nltk_sentiment(string):
    """function for using ntlk sentiment analysis"""
    analyzer = SentimentIntensityAnalyzer()  # nltk base analyzer
    sentiment = analyzer.polarity_scores(string)
    if (sentiment['compound'] < 0):
        result = "negative"
    else:
        if (sentiment['neu'] > 0.770):
            result = "neutral"
        else:
            result = "positive"
    return result


def extraction(string, model_name):
    """general function that extracts model and tokenizer, from the model name(argument) and pass them to one of the two methods for analyzing sentiment"""
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    sentiment = splitting(string, tokenizer, model)
    # sentiment = truncation(string, tokenizer, model)  # remove comment if you want to analyze sentiment through the truncation method
    return sentiment


# def truncation(string, tokenizer, model):
#     """method of sentiment analysis that use the truncate the string if it exceeds the 512 tokens, the model and tokenizer are passed as arguments"""
#     inputs = tokenizer(string, truncation=True, max_length=512, return_tensors="pt")
#     with torch.no_grad():
#         logits = model(**inputs).logits
#     # logits è una particolare struttura dati, simile ad una lista di liste, per lavorarci ci sono apposite funzioni,
#     # vengono utilizzate nello stesso modo, ma cambiano la loro manipolazione di dati in base al modello di Hugging face(se supportato)
#     predicted_class_id_1 = logits.argmax().item()  # funzione che trova l'ID col valore maggiore
#     return model.config.id2label[predicted_class_id_1]  # funzione per ottenere il nome(stringa) del sentimento dall'ID


def splitting(string, tokenizer, model):
    """method of sentiment analysis that splits the string in chunks of 512 tokens and analyze the sentiment in each one of them,
    then it takes the average sentiment and return it. The model and tokenizer are passed as arguments"""
    tokens = tokenizer.encode_plus(string, add_special_tokens=False, return_tensors='pt')
    input_id_chunks = tokens['input_ids'][0].split(510)
    mask_chunks = tokens['attention_mask'][0].split(510)
    input_id_chunks = list(input_id_chunks)
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
    # we need these 3 lines to convert the chunks into a dictionary so we can extract the values and find the average value.
    input_ids = torch.stack(input_id_chunks)
    attention_mask = torch.stack(mask_chunks)
    input_dict = {
        'input_ids': input_ids.long(),
        'attention_mask': attention_mask.int()
    }
    outputs = model(**input_dict)
    probs = torch.nn.functional.softmax(outputs[0], dim=-1)
    mean = probs.mean(dim=0)
    predicted_class_id_1 = torch.argmax(mean).item()
    return model.config.id2label[predicted_class_id_1]


def sentiment_analysis(string):
    """general function that will be called from the inverted_index file.
    it takes the review(as argument) and proceed to analyze sentiment with 3 different models(roBERTa, ARSA, NLTK)"""
    sentiment = [extraction(string, "j-hartmann/emotion-english-distilroberta-base"),
                 extraction(string, "LiYuan/amazon-review-sentiment-analysis"),
                 nltk_sentiment(string)]
    return sentiment
