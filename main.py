from wordcloud import WordCloud
import matplotlib.pyplot as plt
from rottentomatoes import Rottentomatoes

r = Rottentomatoes('wonder_woman_2017', debug=True)
res = r.get()
print('---- Top 20 ----')
top20 = ''
for i in res[20:]:
    print(i)
    top20 += i[0]

print('---- Bottom 20 ----')
bottom20 = ''
for i in res[:20]:
    print(i)
    bottom20 += i[0]

stopwords = open('stopwords.txt', 'r').read().split('\n')
stopwords = set(stopwords)
wordcloud = WordCloud(stopwords=stopwords, max_words=1000, width=1000, height=800)


fig = plt.figure()

figtop = fig.add_subplot(1, 2, 1)
figtop.set_title('top20 word cloud')
figtop.axis('off')
wordcloud.generate(top20)
figtop.imshow(wordcloud)

figbottom = fig.add_subplot(1, 2, 2)
figbottom.set_title('bottom20 word cloud')
figbottom.axis('off')
wordcloud.generate(bottom20)
figbottom.imshow(wordcloud)

plt.show()
