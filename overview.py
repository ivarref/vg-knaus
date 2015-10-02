#!/usr/bin/python
# -*- coding: utf-8 -*-


def generate_db():
  import sqlite3
  conn = sqlite3.connect(':memory:')
  c = conn.cursor()
  c.execute('''CREATE TABLE comments (id text, dato text, timestamp text, likes real, word_count real, char_count real, article_category_names text)''')

  import codecs
  with open('comments.csv', 'r') as fd:
    import csv
    reader = csv.reader(fd, delimiter=',', quotechar='"')
    for (idx, line) in enumerate(reader):
      if (idx==0):
        continue
      (iid,timestamp,likes,word_count,char_count,article_category_names) = [unicode(x, 'utf-8') for x in line]
      dato = timestamp.split('T')[0]
      if dato >= '2013-12-16' and dato <= '2014-07-17':
        c.execute('insert into comments values (?, ?, ?, ?, ?, ?,?)', [iid, dato, timestamp, likes, word_count, char_count, article_category_names])
  c.close()
  return conn

def show_sql(c, s):
  print s
  for (idx, row) in enumerate(c.execute(s)):
    print row

if __name__=="__main__":
  conn = generate_db()
  c = conn.cursor()
  # One knaus = 450 * 400 = 180 000
  #show_sql(c, 'select sum(word_count) / 180000.0 from comments')
  #show_sql(c, 'select dato, sum(word_count) from comments group by dato order by dato asc')
  #show_sql(c, 'select id, sum(word_count) from comments group by id order by sum(word_count) desc')
  #show_sql(c, "select count(*) from comments where id = '965f8f61-9ab9-4bdc-95f6-eeae4f27b087' group by id")
  show_sql(c, "select id, count(*) from comments group by id order by count(*) desc")

  c.close()
  #print total_words

