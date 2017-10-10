import csv
import sent_api.preprocessing as process
import os

# script_dir = os.path.dirname(os.getcwd())
# full_path = os.path.join(os.getcwd(), '/test/test_data.csv')

# print(full_path)

with open('C:\\Users\Brian Mwathi\Code\Final Year 2017\sentalytics-backend\sent_api\\test\\labelled_tweets.csv', 'rt', encoding="UTF-8") as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin, delimiter=",") # comma is default delimiter
    # to_db = [(i['id'], i['username'], i['text'], i['geo'], i['date']) for i in dr]
    new_line = "\n"
    for row in dr:
        # Write negative text to a negative.txt file
        if row['polarity'] == 'negative':
            neg_text = process.process_text(row['text'])
            # print(neg_text)
            with open("negative.txt", "a+", encoding='utf-8') as negative_file:
                negative_file.write(neg_text + new_line)
            # print(row['id'], row['text'], row['polarity'])
        # Write positive text to a positive.txt file
        elif row['polarity'] == 'positive':
            pos_text = process.process_text(row['text'])
            with open("positive.txt", "a+", encoding='utf-8') as positive_file:
                positive_file.write(pos_text + new_line)
        elif row['polarity'] == 'neutral':
            neutral_text = process.process_text(row['text'])
            with open("neutral.txt", "a+", encoding='utf-8') as neutral_file:
                neutral_file.write(neutral_text + new_line)
        #     print(row['id'], row['text'], row['polarity'])
        # print(row['id'], row['text'], row['polarity'])