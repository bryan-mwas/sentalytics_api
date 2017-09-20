import csv, sqlite3

con = sqlite3.connect("../db.sqlite3")
cur = con.cursor()

with open('.\Jumia-6-9-2017.csv','rt', encoding="UTF-8") as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin, delimiter=";") # comma is default delimiter
    to_db = [(i['id'], i['username'], i['text'], i['geo'], i['date']) for i in dr]

cur.executemany("INSERT INTO sent_api_jumiatweet (tweet_id,username,text,geo,date) VALUES (?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()