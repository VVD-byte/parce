import requests
import logging
import re
import sqlite3
from sqlite3 import Error

logging.getLogger(__name__)
logging.basicConfig (level = logging.INFO)

class data_base:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('dat')
        except Error:
            logging.info(Error)
            return False
        self.cur = self.conn.cursor()

    def add_data(self, data):
        for i in data:
            dat = self.get_data(i)
            for j in data[i]:
                if self.url(j) not in dat:
                    dat += self.url(j) + ', '
            if dat != '':
                self.cur.execute("""INSERT INTO urls(one, two) values(?,?);""", (self.url(i), dat))
                self.conn.commit()
                logging.info(f'{self.url(i)} add db')
                self.del_data(i)

    def get_data(self, i):
        dat = ''
        self.cur.execute("""select * from urls where one=?;""", (self.url(i),))
        for q in self.cur.fetchall():
            dat += q[1]
        return dat

    def del_data(self, name):
        self.cur.execute("delete from urls where one='%s'" % self.url(name))
        self.conn.commit()

    def url(self, q):
        return '/'.join(q.split('/')[:3])

    def test(self):
        self.cur.execute('SELECT * FROM urls')
        for i in self.cur.fetchall():
            logging.info(i)

class parcer:
    def __init__(self):
        self.start_url = 'https://bbs.archlinux.org/viewtopic.php?id=134927'
        self.db = data_base()

    def main(self):
        all_url = self.get(self.start_url)
        self.db.add_data({self.start_url:all_url})
        while 1:
            end = {i:self.get(i) for i in all_url}
            all_url = [j for i in end.values() for j in i]
            self.db.add_data(end)


    def get(self, url):
        logging.info(url)
        html = requests.get(url)
        urls = [i.split('"')[0].split("'")[0].split('<')[0] for i in self.get_url(html.text)]
        return urls

    def get_url(self, text):
        return re.findall(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})', text)

if __name__ == '__main__':
    a = parcer()
    a.main()