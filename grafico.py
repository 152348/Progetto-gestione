import matplotlib.pyplot as plt
import numpy as np
import pickle

categories = ['query 1', 'query 2', 'query 3', 'query 4', 'query 5', 'query 6', 'query 7', 'query 8', 'query 9', 'query 10']
with open('dcg.pkl', 'rb') as us:
    ratings= pickle.load(us)
x = np.arange(len(categories))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0
ratings_n = {'positive':[],'neutral':[],'negative':[]}

#for item, value in ratings.items():
    #value = dict(sorted(value.items()))
   # ratings[item] = value

#for items, values in ratings.items():
    #for item, value in values.items():
        #ratings_n[items].append(value)

#plt.style.use("fivethirtyeight")
fig, ax = plt.subplots(constrained_layout=True)

for attribute, measurement in ratings.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('DCG value')
ax.set_title('DCG calculated with different models')
ax.set_xticks(x + width, categories)
ax.legend(loc='upper right', ncols=3)
ax.set_ylim(0, 15.763483535311375)
plt.show()