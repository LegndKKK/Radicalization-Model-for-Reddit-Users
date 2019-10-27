import csv
import plotly
import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import argparse
import calendar


# Find one user's all comments
def Find_user_comments(user):
    if user in dict_users_to_comments:
        print(dict_users_to_comments[user])
        for i in range(len(dict_users_to_comments[user])):
            dict_comments[dict_users_to_comments[user][i]].print_node()


def Find_comment_reply(cur_cid):
    Num_comment = 1000
    past_cid = ''
    while Num_comment > 0:
        G.add_node(cur_cid)
        if past_cid != '':
            G.add_edge(cur_cid, past_cid)
        if cur_cid not in dict_comments:
            break
        cur_comment = dict_comments[cur_cid]
        cur_comment.print_node()
        past_cid = cur_cid
        if cur_comment.parent_id[0:2] == 't1':
            cur_cid = cur_comment.parent_id[3:]
        else:
            cur_cid = cur_comment.parent_id
        Num_comment = Num_comment - 1


def Find_comment_reply_int(cur_cid):
    Num_comment = 1000
    cur_cnt = -1
    past_cnt = -1
    while Num_comment > 0:
        if cur_cid not in dict_comments:
            break
        cur_comment = dict_comments[cur_cid]
        cur_comment.print_node()
        cur_cnt = cur_cnt+1
        G.add_node(cur_cnt)
        if past_cnt >= 0:
            G.add_edge(past_cnt, cur_cnt)

        past_cnt = cur_cnt
        if cur_comment.parent_id[0:2] == 't1':
            cur_cid = cur_comment.parent_id[3:]
        else:
            cur_cid = cur_comment.parent_id
        Num_comment = Num_comment - 1


class comment_node:
    comment_id = ''
    link_id=''
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
        if score ==0:
            self.pos_comment += 1
        else:
            self.neg_comment += 1
        if target_uid in self.list_of_users:
            idx = self.list_of_users[target_uid]
            if score ==0:
                self.pos_num[idx] += 1
            else:
                self.neg_num[idx] += 1
        else:
            self.num_of_users += 1
            self.list_of_users[target_uid] = self.num_of_users
            if score ==0:
                self.pos_num.append(1)
                self.neg_num.append(0)
                self.average_score.append(1.0)
            else:
                self.pos_num.append(0)
                self.neg_num.append(1)
                self.average_score.append(0.0)


parser = argparse.ArgumentParser(description='Process the data and build up the network\n'
                    '<usage> : python Data_reading_Network_building.py -i InputFile_politics.txt -o politics -ts 4 -th 10 -p 0 -nmn 20')
parser.add_argument('-i', dest='Input_File_Name', action='store',default='InputFile.txt',
                    help='The name of input files, one in a row (default = InputFile.txt)')
parser.add_argument('-o', dest='Output_File_Name', action='store',default='OutputFile',
                    help='The name of output file (default = OutputFile)')
parser.add_argument('-ts', dest='Time_step', action='store',default=4, type=int,
                    help='The number of steps to split in one month for calculation (default = 4)')
parser.add_argument('-p', dest='In_Post', action='store',default=0, type=int,
                    help='Open the In Post mode or not (default = 0 connection mode)')
parser.add_argument('-th', dest='Thresh_comment', action='store',default=10, type=int,
                    help='only the users have more comments than threshold will be considered in network (default = 10)')
parser.add_argument('-nmn', dest='num_most_negative', action='store',default=20, type=int,
                    help='number of most negative person we list (default = 20)')
parser.add_argument('-nmc', dest='num_most_changed', action='store',default=20, type=int,
                    help='number of most changed person we list (default = 20)')


args = parser.parse_args()
print('Input file name:', args.Input_File_Name)
print('Output file name:', args.Output_File_Name)
print('Time step:', args.Time_step)
print('In post mode:', args.In_Post)
print('Threshold:', args.Thresh_comment)
print('num of most negative:', args.num_most_negative)
print('num of most changed:', args.num_most_changed)


datas = []
dict_users_history_score = {}
list_most_negative = []

# Generate input file list
File_name_list=[]
with open(args.Input_File_Name, encoding='utf-8') as inputs:
    for row in inputs:
        File_name_list.append(row.rstrip())

#File_name_list=['RC_2015-07-subreddit-toxic-PARSED.csv','RC_2015-08-subreddit-toxic-PARSED.csv','RC_2015-09-subreddit-toxic-PARSED.csv','RC_2015-10-subreddit-toxic-PARSED.csv','RC_2015-11-subreddit-toxic-PARSED.csv','RC_2015-12-subreddit-toxic-PARSED.csv']


#Find the timestamp split list
first_file=File_name_list[0]
year_idx = first_file.find('20')
Date_year = 2000 + int(first_file[year_idx + 2:year_idx + 4])
Date_month = int(first_file[year_idx + 5:year_idx + 7])

timestamp_list=[]
day_step=30/args.Time_step

for i in range(len(File_name_list)):
    Date_day = 1
    timestamp_list.append(int(calendar.timegm(tuple([Date_year, Date_month, Date_day, 0, 0, 0]))))
    for j in range(args.Time_step - 1):
        Date_day += day_step
        timestamp_list.append(int(calendar.timegm(tuple([Date_year, Date_month, Date_day, 0, 0, 0]))))
    Date_month += 1

print(timestamp_list)


for File_name in File_name_list:
    with open(File_name, encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            title = row
            break

        #Find index        
        #comment_id_idx=title.index('id')
        comment_id_idx = -1
        parent_id_idx = -1
        link_id_idx=-1
        user_id_idx = -1
        comment_idx = -1
        timestamp_idx=-1
        toxic_score_idx = -1
       
        for i in range(len(title)):
            if title[i] == 'id' or title[i]=='comment_id':
                comment_id_idx = i
            if title[i] == 'link_id':
                link_id_idx=i
            if title[i] == 'parent_id':
                parent_id_idx = i
            if title[i] == 'author':
                user_id_idx = i
            if title[i] == 'body':
                comment_idx = i
            if title[i] == 'created_utc':
                timestamp_idx = i
            if title[i] == 'sentiment':
                toxic_score_idx=i
                
        print(File_name, title)
        for row in readCSV:
            if row != title and len(row) == len(title) and row[user_id_idx] != 'AutoModerator' and row[comment_idx] != '[deleted]' and row[comment_idx] != '[removed]':
                row[comment_idx] = row[comment_idx].rstrip()
                if row[comment_id_idx] == '' or not row[timestamp_idx].isnumeric() or not row[toxic_score_idx].isnumeric():
                    continue
                # link=parent post
                if row[link_id_idx] == row[parent_id_idx]:
                    datas.append([row[comment_id_idx], row[parent_id_idx][3:],row[user_id_idx],
                                row[comment_idx], int(row[timestamp_idx]), 1, int(row[toxic_score_idx]),row[link_id_idx]])
                else:
                    datas.append([row[comment_id_idx], row[parent_id_idx][3:], row[user_id_idx],
                                row[comment_idx], int(row[timestamp_idx]), 0, int(row[toxic_score_idx]),row[link_id_idx]])


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
            new_comment_node.add_to_node(
                data[0], data[1], data[7],data[2], data[3], data[4], data[5], data[6])
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

    
    Output_Node_File_name = args.Output_File_Name + '_node_week' + str(num_week + 1) + '.csv'    
    Output_Edge_File_name = args.Output_File_Name + '_edge_week' + str(num_week + 1) + '.csv'


    for k, user in dict_users.items():
        user.total_average_score = (
            user.pos_comment) / (user.pos_comment + user.neg_comment)
        for replied_user, idx in user.list_of_users.items():
            user.average_score[idx] = (
                user.pos_num[idx]) / (user.pos_num[idx] + user.neg_num[idx])

    print('Finish calculating')

    with open(Output_Edge_File_name, mode='w', newline='',encoding='utf-8') as output_file:
        output_writer = csv.writer(
            output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(['Source', 'Target', 'Score'])

        for k, user in dict_users.items():
            if user.pos_comment+user.neg_comment >= args.Thresh_comment:
                for user_replied, user_idx in (user.list_of_users).items():
                    if user_replied in dict_users:
                        output_writer.writerow(
                            [user.user_name, user_replied, user.average_score[user_idx]])

    print('Finish Edge output')

    list_user_and_score = []
    list_user_and_changed_score = []

    for k, user in dict_users.items():
        if user.pos_comment + user.neg_comment >= args.Thresh_comment:
            list_user_and_score.append(
                tuple([user.user_name, user.total_average_score]))
            if user.user_name in dict_users_history_score:
                cur_user_history_score = dict_users_history_score[user.user_name]
                while len(cur_user_history_score) < num_week:
                    cur_user_history_score.append(-1)
                cur_user_history_score.append(user.total_average_score)
            else:
                cur_user_history_score = []
                while len(cur_user_history_score) < num_week:
                    cur_user_history_score.append(-1)
                cur_user_history_score.append(user.total_average_score)
                dict_users_history_score[user.user_name] = cur_user_history_score

            if num_week >= 1:
                cur_user_history_score = dict_users_history_score[user.user_name]
                if cur_user_history_score[-2] != -1:
                    list_user_and_changed_score.append(
                        tuple([user.user_name, cur_user_history_score[-2] - cur_user_history_score[-1]]))
                        
    # find most negative users this week
    print(num_week)
    list_user_and_score_nsmallest = heapq.nsmallest(
        args.num_most_negative, list_user_and_score, key=lambda x: x[1])
    list_user_most_negative=[]
    for i in list_user_and_score_nsmallest:
        list_user_most_negative.append(i[0])
    print('N most negative person:')
    print(list_user_most_negative)

    #find most changed users
    list_user_and_changed_score_nlargest = heapq.nlargest(
        args.num_most_changed, list_user_and_changed_score, key=lambda x: x[1])
    list_user_most_changed=[]
    for i in list_user_and_changed_score_nlargest:
        list_user_most_changed.append(i[0])
    print('N most changed person:')
    print(list_user_most_changed)

    #find the list of posts that most negative users in
    if args.In_Post:
        list_posts_most_negative_in=[]
        for user in list_user_most_negative:
            user_n=dict_users[user]
            for post in user_n.list_of_posts:
                list_posts_most_negative_in.append(post)
        set_posts_most_negative_in = set(list_posts_most_negative_in)

    #output to csvfile
    with open(Output_Node_File_name, mode='w', newline='', encoding='utf-8') as output_file:
        output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(['Id', 'Score', 'Pos_num', 'Neg_num', 'Total_num','isMost'])   
        for k, user in dict_users.items():
            if user.pos_comment + user.neg_comment >= args.Thresh_comment:
                user_ischanged = 0
                user_isnegative = 0
                if user.user_name in list_user_most_negative:
                    user_isnegative = 1
                if user.user_name in list_user_most_changed:
                    user_ischanged = 1
                row_to_write = [user.user_name, user.total_average_score, user.pos_comment, user.neg_comment, user.pos_comment + user.neg_comment]
                
                #1 - most changed
                #2 - most negative
                #3 - most changed and negative
                #4 - replied by most neg
                #5 - replying to most neg

                if not user_isnegative and not user_ischanged:
                    if args.In_Post:
                        user_isinpost = 0
                        for post in set_posts_most_negative_in:
                            if post in user.list_of_posts:
                                user_isinpost = 1
                                break
                        if user_isinpost:
                            row_to_write.append(100)
                        else:
                            row_to_write.append(0)
                    else:
                        row_to_write.append(0)
                elif not user_isnegative and user_ischanged:
                    row_to_write.append(1)
                elif user_isnegative and not user_ischanged:
                    row_to_write.append(2)
                else:
                    row_to_write.append(3)
                output_writer.writerow(row_to_write)

    print('Finish Node output')


    # Find_user_comments('Bartiemus')
    # Find_user_comments('Trauermarsch')
    # Find_user_comments('DjHanzelsSunglasses')
    # Find_user_comments('mick4state')

    for k, v in dict_comments.items():
        del v
    for k, v in dict_users_to_comments.items():
        del v
    for k, v in dict_users.items():
        del v
    del dict_comments
    del dict_users_to_comments
    del dict_users

    # output to csv of comments
    # if comment_mode and row[0] != 'id':
    #     output_writer.writerow([row[0], row[1][3:], 'Directed'])
# user = 'TheLightningL0rd'
# user = 'gsfgf'
# Find_user_comments(user)
