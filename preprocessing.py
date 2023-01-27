import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from csv import reader
from csv import DictReader
import string
import time

def preprocessing(text):
    '''Function that preprocess text passed as argument by tokenizing it, removing the stopwords and stemming'''
    pre = time.perf_counter()
    #porter = PorterStemmer()
    wnl = nltk.WordNetLemmatizer()
    tokens = nltk.word_tokenize(text.lower())
    tokens = [t.translate(str.maketrans('','',string.punctuation)) for t in tokens] #removal of punctuantion
    #rimuovi punteggiatura
    tokens = [t for t in tokens if not t in stopwords.words('english') and t != '']
    tokens = [wnl.lemmatize(t) for t in tokens]
    print(time.perf_counter() - pre)
    return tokens


if __name__ == '__main__':
    #sentence = input('Inserisci la frase di input: ')
    with open('Reviews_MAL.csv', 'r') as read_obj:
        csv_dict_reader = DictReader(read_obj)
        for row in csv_dict_reader:
            print(preprocessing(row['Text']))
            break
    #print(preprocessing(sentence))