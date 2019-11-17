import csv
import plotly
import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import argparse
import calendar


class comment_node:
    comment_id = ''
    link_id = ''
    parent_id = ''
    user_id = ''
    score = 0
    timestamp = ''
    comment_word = ''
    parent_is_post = 0
    subreddit = ''

    def __init__(self):
        self.comment_id = ''
        self.parent_id = ''
        self.link_id = ''
        self.user_id = ''
        self.score = 0
        self.timestamp = ''
        self.comment_word = ''
        self.parent_is_post = 0
        self.subreddit = ''

    def add_to_node(self, cid, pid, lid, uid, t, cw, pip, s, subr):
        self.comment_id = cid
        self.parent_id = pid
        self.link_id = lid
        self.user_id = uid
        self.timestamp = t
        self.comment_word = cw
        self.parent_is_post = pip
        self.score = s
        self.subreddit = subr

    def print_node(self):
        print('Comment ID: ', self.comment_id)
        print('Parent ID: ', self.parent_id)
        print('Link ID: ', self.link_id)
        print('User ID: ', self.user_id)
        print('Timestamp: ', self.timestamp)
        print('Comment: ', self.comment_word)
        print('Score:', self.score)
        print('Subreddit:', self.subreddit)
        print('\n')


class user_node:
    user_name = ''
    pos_comment = 0
    neg_comment = 0
    total_average_score = 0.0
    num_of_users = -1
    list_of_users = {}
    pos_num = []
    neg_num = []
    average_score = []
    list_of_posts = set()

    def __init__(self):
        self.user_name = ''
        self.pos_comment = 0
        self.neg_comment = 0
        self.total_average_score = 0.0
        self.num_of_users = -1
        self.list_of_users = {}
        self.pos_num = []
        self.neg_num = []
        self.average_score = []
        self.list_of_posts = set([])

    def add_to_node(self, target_uid, score, post_lid):
        self.list_of_posts.add(post_lid)
        if score == 0:
            self.pos_comment += 1
        else:
            self.neg_comment += 1
        if target_uid in self.list_of_users:
            idx = self.list_of_users[target_uid]
            if score == 0:
                self.pos_num[idx] += 1
            else:
                self.neg_num[idx] += 1
        else:
            self.num_of_users += 1
            self.list_of_users[target_uid] = self.num_of_users
            if score == 0:
                self.pos_num.append(1)
                self.neg_num.append(0)
                self.average_score.append(1.0)
            else:
                self.pos_num.append(0)
                self.neg_num.append(1)
                self.average_score.append(0.0)


parser = argparse.ArgumentParser(description='Process the data and build up the network\n'
                                 '<usage> : python Data_reading_Network_building.py -i InputFile_politics.txt -o politics -ts 4 -th 10 -p 0 -nmn 20')
parser.add_argument('-i', dest='Input_File_Name', action='store', default='InputFile.txt',
                    help='The name of input files, one in a row (default = InputFile.txt)')
parser.add_argument('-o', dest='Output_File_Name', action='store', default='OutputFile',
                    help='The name of output file (default = OutputFile)')
parser.add_argument('-ts', dest='Time_step', action='store', default=4, type=int,
                    help='The number of steps to split in one month for calculation (default = 4)')
parser.add_argument('-p', dest='In_Post', action='store', default=0, type=int,
                    help='Open the In Post mode or not (default = 0 connection mode)')
parser.add_argument('-th', dest='Thresh_comment', action='store', default=10, type=int,
                    help='only the users have more comments than threshold will be considered in network (default = 10)')
parser.add_argument('-nmn', dest='num_most_negative', action='store', default=20, type=int,
                    help='number of most negative person we list (default = 20)')
parser.add_argument('-nmc', dest='num_most_changed', action='store', default=20, type=int,
                    help='number of most changed person we list (default = 20)')
parser.add_argument('-thc', dest='Thresh_changed', action='store', default=0.5, type=float,
                    help='threshold of changed score to track (default = 0.5)')
parser.add_argument('-thn', dest='Thresh_negative', action='store', default=0.8, type=float,
                    help='threshold to define most negative user comparing to average score (default = 0.8)')
parser.add_argument('-thm', dest='Thresh_mode', action='store', default=1, type=int,
                    help='to decide we determine most negative and most changed user by a number or by threshold (default = 1)')


args = parser.parse_args()
print('Input file name:', args.Input_File_Name)
print('Output file name:', args.Output_File_Name)
print('Time step:', args.Time_step)
print('In post mode:', args.In_Post)
print('Threshold:', args.Thresh_comment)
print('num of most negative:', args.num_most_negative)
print('num of most changed:', args.num_most_changed)
print('Threshold of changed score:', args.Thresh_changed)
print('Threshold of negative score:', args.Thresh_negative)
print('Threshold mode:', args.Thresh_mode)

Total_comment = 0
Total_toxic_comment = 0
datas = []
list_authors_names = []
dict_users_history_score = {}

# Generate input file list
File_name_list = []
with open(args.Input_File_Name, encoding='utf-8') as inputs:
    for row in inputs:
        File_name_list.append(row.rstrip())

# File_name_list=['RC_2015-07-subreddit-toxic-PARSED.csv','RC_2015-08-subreddit-toxic-PARSED.csv','RC_2015-09-subreddit-toxic-PARSED.csv','RC_2015-10-subreddit-toxic-PARSED.csv','RC_2015-11-subreddit-toxic-PARSED.csv','RC_2015-12-subreddit-toxic-PARSED.csv']


# Find the timestamp split list
first_file = File_name_list[0]
year_idx = first_file.find('20')
Date_year = 2000 + int(first_file[year_idx + 2:year_idx + 4])
Date_month = int(first_file[year_idx + 5:year_idx + 7])

timestamp_list = []
day_step = 30/args.Time_step

for i in range(len(File_name_list)):
    Date_day = 1
    timestamp_list.append(
        int(calendar.timegm(tuple([Date_year, Date_month, Date_day, 0, 0, 0]))))
    for j in range(args.Time_step - 1):
        Date_day += day_step
        timestamp_list.append(
            int(calendar.timegm(tuple([Date_year, Date_month, Date_day, 0, 0, 0]))))
    Date_month += 1

if Date_month > 12:
    Date_year += 1
    Date_month = 1

timestamp_list.append(
    int(calendar.timegm(tuple([Date_year, Date_month, 1, 0, 0, 0]))))

print(timestamp_list)

with open('targetAuthors.txt', encoding='utf-8', mode='r') as authorfile:
    for row in authorfile:
        list_authors_names.append(row.rstrip())

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
        subreddit_idx = -1

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
            if title[i] == 'toxicity':
                toxic_score_idx = i
            if title[i] == 'subreddit':
                subreddit_idx = i

        print(File_name, title)
        # print(comment_id_idx,parent_id_idx,link_id_idx,user_id_idx,comment_idx,timestamp_idx,toxic_score_idx,subreddit_idx)
        for row in readCSV:

            if row != title and len(row) == len(title) and row[user_id_idx] != 'AutoModerator' and row[comment_idx] != '[deleted]' and row[comment_idx] != '[removed]' and row[user_id_idx] != 'MAGABrickBot':
                row[comment_idx] = row[comment_idx].rstrip()

                # if row[comment_id_idx] == 't3_3km3gd' or row[comment_id_idx] == '3km3gd' or row[comment_id_idx] == 't3_3kmc0y' or row[comment_id_idx] == '3kmc0y':
                #     print(row)

                # link=parent post
                if row[link_id_idx] == row[parent_id_idx]:
                    datas.append([row[comment_id_idx], row[parent_id_idx][3:], row[user_id_idx], row[comment_idx], int(
                        row[timestamp_idx][:-2]), 1, int(row[toxic_score_idx]), row[link_id_idx], row[subreddit_idx]])
                else:
                    datas.append([row[comment_id_idx], row[parent_id_idx][3:], row[user_id_idx], row[comment_idx], int(
                        row[timestamp_idx][:-2]), 0, int(row[toxic_score_idx]), row[link_id_idx], row[subreddit_idx]])
                Total_comment += 1
                if row[toxic_score_idx] == '1':
                    Total_toxic_comment += 1

Overall_average_score = args.Thresh_negative * \
    (Total_comment-Total_toxic_comment)/Total_comment
print(Total_toxic_comment, Overall_average_score, Total_comment)

# loop over week
for num_week in range(len(timestamp_list) - 1):
    dict_comments = {}
    dict_users_to_comments = {}
    dict_users = {}

    start_time = timestamp_list[num_week]
    end_time = timestamp_list[num_week + 1]

    # loop over comments
    for data in datas:
        if data[4] >= start_time and data[4] <= end_time:
            new_comment_node = comment_node()
            # def add_to_node(self, cid, pid, lid, uid, t, cw, pip, s, subr):
            new_comment_node.add_to_node(
                data[0], data[1], data[7], data[2], data[4], data[3], data[5], data[6], data[8])
            dict_comments[data[0]] = new_comment_node
            if data[2] in dict_users_to_comments:
                dict_users_to_comments[data[2]].append(data[0])
            else:
                dict_users_to_comments[data[2]] = [data[0]]

    for data in datas:
        if data[4] >= start_time and data[4] <= end_time and data[1] in dict_comments:
            if data[2] in dict_users:
                target_uid = dict_comments[data[1]].user_id
                dict_users[data[2]].add_to_node(target_uid, data[6], data[7])
            else:
                cur_user_node = user_node()
                cur_user_node.user_name = data[2]
                target_uid = dict_comments[data[1]].user_id
                cur_user_node.add_to_node(target_uid, data[6], data[7])
                dict_users[data[2]] = cur_user_node

    print('Finish processing')

    author_num_comment = []
    author_parent_num_comment = []

    with open('Author_result_'+str(num_week)+'.csv', mode='w', newline='', encoding='utf-8') as output_file:
        output_writer = csv.writer(
            output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(
            ['Id', 'Pos_num_in', 'Neg_num_in', 'Pos_num_not_in', 'Neg_num_not_in','Parent_pos_num_in', 'Parent_neg_num_in','Parent_pos_num_not_in','Parent_neg_num_not_in','Score_in','Score_not_in','Parent_score_in','Parent_score_not_in','Total_score','Parent_Total_score','Ratio'])
        for cur_author in list_authors_names:
            new_row=[0,0,0,0,0,0,0,0]
            for data in datas:
                if data[2] == cur_author and data[4] >= start_time and data[4] <= end_time:
                    if data[8] == 'politics':
                        if data[6] == 1:
                            new_row[1] += 1
                        else:
                            new_row[0] +=1
                    else:
                        if data[6] == 1:
                            new_row[3] += 1
                        else:
                            new_row[2] += 1
                    cur_parent = data[1]
                    if cur_parent not in dict_comments:
                        continue
                    parent_node = dict_comments[cur_parent]
                    if parent_node.timestamp < start_time or parent_node.timestamp > end_time:
                        continue
                    if parent_node.subreddit == 'politics':
                        if parent_node.score == 1:
                            new_row[5] += 1
                        else:
                            new_row[4] += 1
                    else:
                        if parent_node.score == 1:
                            new_row[7] += 1
                        else:
                            new_row[6] += 1
            
            #print(new_row)
            # Calculating score
            if new_row[0] + new_row[1] == 0:
                new_row.append(-1)
            else:
                new_row.append(new_row[1] / (new_row[0] + new_row[1]))
            if new_row[2] + new_row[3] == 0:
                new_row.append(-1)
            else:
                new_row.append(new_row[3] / (new_row[2] + new_row[3]))
            if new_row[4] + new_row[5] == 0:
                new_row.append(-1)
            else:
                new_row.append(new_row[5] / (new_row[4] + new_row[5]))
            if new_row[6] + new_row[7] == 0:
                new_row.append(-1)
            else:
                new_row.append(new_row[7] / (new_row[6] + new_row[7]))
            #total_score
            if new_row[0] + new_row[1] + new_row[2] + new_row[3] == 0:
                new_row.append(-1)
            else:
                new_row.append((new_row[1] + new_row[3]) / (new_row[0] + new_row[1] + new_row[2] + new_row[3]))
            if new_row[4] + new_row[5] + new_row[6] + new_row[7] == 0:
                new_row.append(-1)
            else:
                new_row.append((new_row[5] + new_row[7]) / (new_row[4] + new_row[5] + new_row[6] + new_row[7]))
            if new_row[2] + new_row[3] == 0:
                new_row.append(-1)
            else:
                new_row.append((new_row[0]+new_row[1])/(new_row[0]+new_row[1]+new_row[2]+new_row[3]))
            write_row = [cur_author]
            for i in new_row:
                write_row.append(str(i))

            output_writer.writerow(write_row)


    for k, v in dict_comments.items():
        del v
    for k, v in dict_users_to_comments.items():
        del v
    for k, v in dict_users.items():
        del v
    del dict_comments
    del dict_users_to_comments
    del dict_users

# user = 'TheLightningL0rd'
# user = 'gsfgf'
# Find_user_comments(user)
