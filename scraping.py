import requests, pandas, time, random
from bs4 import BeautifulSoup
from termcolor import colored

with open('numero_pagina.txt', 'r') as numero:
    page_count = int(numero.read())
URL = f"https://myanimelist.net/reviews.php?t=manga&filter_check=&filter_hide=&preliminary=on&spoiler=on&p={page_count}"
user_agent = {'User-Agent'  : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'}
response = requests.get(URL, headers = user_agent) #richiesta https per la prima pagina
reviews = []
#df = pandas.DataFrame(list(), columns = ['Title', 'User', 'Text', 'Rating', 'Recommendation'])
#df.to_csv('Reviews_MAL.csv')
controllo = True

while response.status_code != 404 and controllo:
    response = response.content #prende contenuto pagina dell'URL
    soup = BeautifulSoup(response, 'html.parser') #estrae l'html dalla risposta
    div_content = soup.find('div', id = 'content') #prende insieme di elementi con anche le recensioni
    page_reviews = div_content.find_all('div', class_= 'review-element js-review-element') #estrae le recensione
    for page_review in page_reviews:
        link = page_review.find('div', class_= 'open').find('a', class_= 'ga-click')['href'] #estrae il link alla recensione
        print(colored(link, 'yellow'))
        review_page = requests.get(link, headers = user_agent) #manda la richiesta per la recensione
        review_page = review_page.content #prende il contenuto della pagina
        soup = BeautifulSoup(review_page, 'html.parser') #estrae html dalla risposta
        title = [soup.find('a', class_= 'title ga-click').text] #titolo
        user = [soup.find('div', class_= 'username').find('a', class_= 'ga-click').text] #user
        text = [soup.find('div', class_= 'text').text.strip()] #recensione
        rating = [soup.find('div', class_= 'rating mt20 mb20 js-hidden').find('span', class_= 'num').text] #rating
        recommendation = [soup.find('div', class_= ['tag recommended', 'tag not-recommended', 'tag mixed-feelings']).text]  #recommended
        reviews = {'Title': title, 'User': user, 'Text': text, 'Rating': rating, 'Recommendation': recommendation}
        df = pandas.DataFrame(reviews)
        df.to_csv('Reviews_MAL.csv', mode = 'a', index=False, header=False)
        time.sleep(random.randint(3, 10))
    page_count += 1 #counter per la prossima pagina
    with open('numero_pagina.txt', 'w') as numero:
        numero.write(str(page_count))
    URL = f"https://myanimelist.net/reviews.php?t=manga&filter_check=&filter_hide=&preliminary=on&spoiler=on&p={page_count}"
    response = requests.get(URL, headers = user_agent)
    print(colored(page_count, 'blue'))
    if page_count % 10 == 0:
        risposta = input("Vuoi terminare lo scraping?: ")
        if risposta == 'si':
            controllo = False



print(page_count)
