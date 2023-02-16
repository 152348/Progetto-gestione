import csv
import pickle
def count():
    """Simple function dad iterates through the file "Reviews_MAL.csv" and saves in dictionary the number of
    reviews written by every user. It then saves the dictionary to a pickle file"""
    user_c = {}
    with open ('Reviews_MAL.csv', 'r', encoding='utf8') as rev:
        df = csv.DictReader(rev)
        for line in df:
            user_c[line['User']] = user_c.get(line['User'], 0) + 1

    with open('User_count.pkl', 'wb') as us:
        pickle.dump(user_c, us)

if __name__ == '__main__':
    count()