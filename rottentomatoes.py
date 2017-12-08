# to make function `eval` can return `double` rather than `int`
from __future__ import division
import re
import urllib2
from BeautifulSoup import BeautifulSoup


class Rottentomatoes:
    def __init__(self, movie, debug=False):
        self.movie = movie
        self.debug = debug
        self.page = self.get_page()

    def get(self):
        """
        :return: a list of lists [review, score]
        """
        # https://www.rottentomatoes.com/m/wonder_woman_2017/reviews
        ls = []
        for i in range(1, self.page + 1):
            if not self.debug:
                r = urllib2.urlopen('https://www.rottentomatoes.com/m/{movie}/reviews/?page={page}'
                                    .format(movie=self.movie, page=i))
            else:
                r = open('./{movie}/{page}.html'.format(movie=self.movie, page=i))
            soup = BeautifulSoup(r.read())
            for soup in (soup.findAll('div', 'col-xs-16 review_container')):
                review = soup.find('div', 'the_review').contents
                score = soup.find('div', 'small subtle').contents
                if len(score) < 2:
                    # throw away review has not grade
                    continue

                review = Rottentomatoes.format_review((review[0]))
                score = Rottentomatoes.format_score(score[-1])
                if not score:
                    continue
                ls.append([review, score])
        # sort by score
        ls.sort(key=lambda x: x[1], reverse=True)
        return ls

    def get_page(self):
        """
        :type return: int
        """
        if not self.debug:
            r = urllib2.urlopen('https://www.rottentomatoes.com/m/{movie}/reviews'.format(movie=self.movie))
        else:
            r = open('./{movie}/1.html'.format(movie=self.movie))
        soup = BeautifulSoup(r.read())
        page = soup.find('span', 'pageInfo').contents[0]
        page = page.split()[3]
        page = int(page)
        return page

    @staticmethod
    def format_review(review):
        """
        :type review: str
        :return: str
        """
        # print(type(review))
        review = re.sub(
            '\n *',
            ' ',
            review
        )
        review = review.strip()
        return review

    @staticmethod
    def format_score(score):
        """
        :type score: str
        :return: str
        """
        score = (score
            .replace('\n', '')
            .replace(' ', '')
            .replace('|OriginalScore:', ''))
        if score.find('/') > 0:
            # found `/`
            # calculate score
            score = eval(score)
            score = '%.2f' % (score)
        else:
            # not found `/`
            score = Rottentomatoes.nominal2per(score)
        return score

    @staticmethod
    def nominal2per(nominal):
        """ translate nominal score to percentage
        :type nominal: str
        :return: return None when cannot the key not in dict
        """
        d = {
            'A+': 1,
            'A': 0.96,
            'A-': 0.92,
            'B+': 0.89,
            'B': 0.86,
            'B-': 0.82,
            'C+': 0.79,
            'C': 0.76,
            'C-': 0.72,
            'D+': 0.69,
            'D': 0.66,
            'D-': 0.62,
        }
        if not d.has_key(nominal):
            return None
        return d[nominal]


if __name__ == '__main__':
    r = Rottentomatoes('wonder_woman_2017', debug=True)
    res = r.get()
    for i in range(20):
        print(res[i])
