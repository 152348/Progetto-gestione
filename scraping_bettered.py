import requests, pandas, time, random, re
from bs4 import BeautifulSoup
from termcolor import colored

#The program checks if a "page_number.txt" file exists and if it doesn't, it is created and initialized to the number one
try:
    with open('page_number.txt', 'x') as number:
        number.write(str(1))
except FileExistsError:
    pass

#It checks for a csv for the reviews and if it doesn't exist, it is created with the necessary headers
try:
    with open('Reviews_MAL.csv', 'x'):
        df = pandas.DataFrame(list(), columns = ['Title', 'User', 'Text', 'Rating', 'Recommendation'])
        df.to_csv('Reviews_MAL.csv', index=False)
except FileExistsError:
    pass

#It creates the URL starting from the page stated in the page_number file and it issues the request to the site adding the
#user agent in the header of the request
with open('page_number.txt', 'r') as number:
    page_count = int(number.read())
URL = f"https://myanimelist.net/reviews.php?t=manga&filter_check=&filter_hide=&preliminary=on&spoiler=on&p={page_count}"
user_agent = {'User-Agent'  : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'}
response = requests.get(URL, headers = user_agent)
controll = True #variable used later to stop the flow of the code if the user so desires

#while cycle that continues to request and extract reviews from the pages until it receives a 404 error as a response from the
#server or the user decides to stop the scraping
while response.status_code != 404 and controll:
    response = response.content
    soup = BeautifulSoup(response, 'html.parser') #extraction of the html from the response
    div_content = soup.find('div', id = 'content') #extraction of element that contains all the reviews
    page_reviews = div_content.find_all('div', class_= 'review-element js-review-element') #extraction of only the reviews

    for page_review in page_reviews:
        title = [page_review.find('a', class_= 'title ga-click').text]
        user = [page_review.find('div', class_= 'username').find('a', class_= 'ga-click').text] 
        text = [re.sub("\s{2,}\.{3}\n", " ", page_review.find('div', class_= 'text').text.strip())] 
        rating = [page_review.find('div', class_= 'rating mt20 mb20 js-hidden').find('span', class_= 'num').text] 
        recommendation = [page_review.find('div', class_= ['tag recommended btn-label js-btn-label', 'tag not-recommended '\
        'btn-label js-btn-label', 'tag mixed-feelings btn-label js-btn-label']).text]
        reviews = {'Title': title, 'User': user, 'Text': text, 'Rating': rating, 'Recommendation': recommendation}
        df = pandas.DataFrame(reviews)
        df.to_csv('Reviews_MAL.csv', mode = 'a', index=False, header=False)

    page_count += 1
    with open('page_number.txt', 'w') as number:
        number.write(str(page_count))

    URL = f"https://myanimelist.net/reviews.php?t=manga&filter_check=&filter_hide=&preliminary=on&spoiler=on&p={page_count}"
    time.sleep(random.randint(3, 10))
    response = requests.get(URL, headers = user_agent)
    print(colored(page_count, 'blue'))

    if page_count % 100 == 0:
        answer = input("Do you want to end the scraping?: ")
        if answer == 'yes':
            controll = False