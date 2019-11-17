import csv
import heapq
import calendar
import random


class comment_node:
    comment_id = ''
    link_id = ''
    parent_id = ''
    user_id = ''
    score = 0
    timestamp = ''
    comment_word = ''
    parent_is_post = 0

    def __init__(self):
        self.comment_id = ''
        self.parent_id = ''
        self.link_id = ''
        self.user_id = ''
        self.score = 0
        self.timestamp = ''
        self.comment_word = ''
        self.parent_is_post = 0

    def add_to_node(self, cid, pid, lid, uid, t, cw, pip, s):
        self.comment_id = cid
        self.parent_id = pid
        self.link_id = lid
        self.user_id = uid
        self.timestamp = t
        self.comment_word = cw
        self.parent_is_post = pip
        self.score = s

    def print_node(self):
        print('Comment ID: ', self.comment_id)
        print('Parent ID: ', self.parent_id)
        print('User ID: ', self.user_id)
        print('Timestamp: ', self.timestamp)
        print('Comment: ', self.comment_word)
        print('\n')


Total_comment = 0
Total_toxic_comment = 0
datas = []

# Generate input file list
File_name_list = []
with open('InputFile_politics.txt', encoding='utf-8') as inputs:
    for row in inputs:
        File_name_list.append(row.rstrip())

# File_name_list=['RC_2015-07-subreddit-toxic-PARSED.csv','RC_2015-08-subreddit-toxic-PARSED.csv','RC_2015-09-subreddit-toxic-PARSED.csv','RC_2015-10-subreddit-toxic-PARSED.csv','RC_2015-11-subreddit-toxic-PARSED.csv','RC_2015-12-subreddit-toxic-PARSED.csv']


# Find the timestamp split list
first_file = File_name_list[0]
year_idx = first_file.find('20')
Date_year = 2000 + int(first_file[year_idx + 2:year_idx + 4])
Date_month = int(first_file[year_idx + 5:year_idx + 7])

timestamp_list = []
day_step = 30

for i in range(len(File_name_list)):
    Date_day = 1
    timestamp_list.append(
        int(calendar.timegm(tuple([Date_year, Date_month, Date_day, 0, 0, 0]))))
    for j in range(1 - 1):
        Date_day += day_step
        timestamp_list.append(
            int(calendar.timegm(tuple([Date_year, Date_month, Date_day, 0, 0, 0]))))
    Date_month += 1

if Date_month > 12:
    Date_year += 1
    Date_month = 1

print(Date_year, Date_month)
timestamp_list.append(
    int(calendar.timegm(tuple([Date_year, Date_month, 1, 0, 0, 0]))))
print(timestamp_list)

for File_name in File_name_list:
    with open(File_name, encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            title = row
            break

        # Find index
        # comment_id_idx=title.index('id')
        comment_id_idx = -1
        parent_id_idx = -1
        link_id_idx = -1
        user_id_idx = -1
        comment_idx = -1
        timestamp_idx = -1
        toxic_score_idx = -1

        for i in range(len(title)):
            if title[i] == 'id' or title[i] == 'comment_id':
                comment_id_idx = i
            if title[i] == 'link_id':
                link_id_idx = i
            if title[i] == 'parent_id':
                parent_id_idx = i
            if title[i] == 'author':
                user_id_idx = i
            if title[i] == 'body':
                comment_idx = i
            if title[i] == 'created_utc':
                timestamp_idx = i
            if title[i] == 'sentiment':
                toxic_score_idx = i

        print(File_name, title)
        for row in readCSV:
            if row != title and len(row) == len(title) and row[user_id_idx] != 'AutoModerator' and row[comment_idx] != '[deleted]' and row[comment_idx] != '[removed]' and row[user_id_idx] != 'MAGABrickBot':
                row[comment_idx] = row[comment_idx].rstrip()
                if row[comment_id_idx] == '' or not row[timestamp_idx].isnumeric() or not row[toxic_score_idx].isnumeric():
                    continue
                # link=parent post
                if row[link_id_idx] == row[parent_id_idx]:
                    datas.append([row[comment_id_idx], row[parent_id_idx][3:], row[user_id_idx],
                                  row[comment_idx], int(row[timestamp_idx]), 1, int(row[toxic_score_idx]), row[link_id_idx]])
                else:
                    datas.append([row[comment_id_idx], row[parent_id_idx][3:], row[user_id_idx],
                                  row[comment_idx], int(row[timestamp_idx]), 0, int(row[toxic_score_idx]), row[link_id_idx]])
                Total_comment += 1
                if row[toxic_score_idx] == '2':
                    Total_toxic_comment += 1

with open('Overall_Analysis.csv', mode='w') as output_file:
    output_writer = csv.writer(
        output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    output_writer.writerow(['Toxic_to_Toxic', 'Nontoxic_to_Toxc', 'Toxic_to_Nontoxic',
                            'Nontoxic_to_Nontoxic', 'Total_Number', 'Ratio_Toxic_Parents', 'Ratio_Nontoxic_Parents'])

    for num_week in range(len(timestamp_list) - 1):
        dict_comments = {}

        start_time = timestamp_list[num_week]
        end_time = timestamp_list[num_week + 1]
        t2t = 0
        t2n = 0
        n2t = 0
        n2n = 0
        total = 0

        # loop over comments
        for data in datas:
            if data[4] >= start_time and data[4] <= end_time:
                new_comment_node = comment_node()
                new_comment_node.add_to_node(
                    data[0], data[1], data[7], data[2], data[4], data[3], data[5], data[6])
                dict_comments[data[0]] = new_comment_node

        for k, v in dict_comments.items():
            if v.parent_id in dict_comments:
                total += 1
                if v.score == 0:
                    if dict_comments[v.parent_id].score == 0:
                        n2n += 1
                    else:
                        n2t += 1
                else:
                    if dict_comments[v.parent_id].score == 0:
                        t2n += 1
                    else:
                        t2t += 1

        print('Total:', total)
        print('Toxic to Toxic:', t2t)
        print('Toxic to Nontoxic:', t2n)
        print('Nontoxic to Toxc:', n2t)
        print('Nontoxic to Nontoxic:', n2n)

        output_writer.writerow(
            [t2t, n2t, t2n, n2n, total, t2t/(t2t+n2t), t2n/(t2n+n2n)])

        for k, v in dict_comments.items():
            del v
        del dict_comments
