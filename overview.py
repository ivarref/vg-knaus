#!/usr/bin/python
# -*- coding: utf-8 -*-


def generate_db():
  import sqlite3
  conn = sqlite3.connect(':memory:')
  c = conn.cursor()
  c.execute('''CREATE TABLE comments (id text, dato text, timestamp text, likes real, word_count real, char_count real, category text)''')

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
        for cat in article_category_names.split("|"):
          cat = cat.strip()
          c.execute('insert into comments values (?, ?, ?, ?, ?, ?,?)', [iid, dato, timestamp, likes, word_count, char_count, cat])
        c.execute('insert into comments values (?, ?, ?, ?, ?, ?,?)', [iid, dato, timestamp, likes, word_count, char_count, 'Alle'])
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
  #show_sql(c, "select id, count(*) from comments group by id order by count(*) desc")
  from datetime import date
  def get_date(q):
    s = [x for x in c.execute(q)][0][0].split('-')
    return date(int(s[0]), int(s[1]), int(s[2]))
    
  start_date = get_date('select min(dato) from comments')
  stop_date = get_date('select max(dato) from comments')
  delta = stop_date - start_date
  weeks = delta.days / 7.0
  with open('overview.md', 'w') as fd:
    fd.write("""
# VG-Knausgård

I kommentarfeltet på VG sine nettsider vert det produsert ein del tekst.
For å gjera dette meir forståeleg, har eg sett på dette i form av antall Knausgård-romaner.
Ein `Knausgård` vert definert som `450 sider ganger 400 ord` eller `180 000 ord`.
Side 136 i Min Kamp 1 (hardback, 2009) er brukt som referanse (388 ord, runda oppover til 400).

Takk til Jari Bakken i VG for anonymiserte data.

Dataene går over %.0f veker (%d dager).

| Kategori | Sider per dag | Knausgård-romaner per veke   | Totalt antall Knausgård-romaner |
| -------- | ------------: | -----: | -----: |\n""" % (weeks, delta.days))

    for (idx, row) in enumerate(c.execute("""select category, 
             round(sum(word_count) / (?*400),1) as pages_per_day,
             round(sum(word_count) / (?*450*400),1) as knaus_per_week,
             round(sum(word_count) / (450*400),1) as total_knaus
             from comments 
             group by category 
             order by sum(word_count) desc""", [delta.days, weeks])):
      fd.write("| ")
      fd.write(row[0].encode('utf-8'))
      fd.write(" | ")
      fd.write(" | ".join([str(x) for x in row[1:]]))
      fd.write(" |")
      fd.write("\n")

  c.close()
  #print total_words

