import csv
import plotly
import plotly.graph_objects as go
import networkx as nx
# pajek
import matplotlib.pyplot as plt


# Find one user's all comments
def Find_user_comments(user):
    if user in dict_users_to_comments:
        print(dict_users_to_comments[user])
        for i in range(len(dict_users_to_comments[user])):
            dict_comments[dict_users_to_comments[user][i]].print_node()


# def Find_comment_reply(cur_cid):
#     Num_comment = 1000
#     past_cid = ''
#     while Num_comment > 0:
#         G.add_node(cur_cid)
#         if past_cid != '':
#             G.add_edge(cur_cid, past_cid)
#         if cur_cid not in dict_comments:
#             break
#         cur_comment = dict_comments[cur_cid]
#         cur_comment.print_node()
#         past_cid = cur_cid
#         if cur_comment.parent_id[0:2] == 't1':
#             cur_cid = cur_comment.parent_id[3:]
#         else:
#             cur_cid = cur_comment.parent_id
#         Num_comment = Num_comment - 1


# def Find_comment_reply_int(cur_cid):
#     Num_comment = 1000
#     cur_cnt = -1
#     past_cnt = -1
#     while Num_comment > 0:
#         if cur_cid not in dict_comments:
#             break
#         cur_comment = dict_comments[cur_cid]
#         cur_comment.print_node()

#         cur_cnt = cur_cnt+1
#         G.add_node(cur_cnt)

#         if past_cnt >= 0:
#             G.add_edge(past_cnt, cur_cnt)

#         past_cnt = cur_cnt
#         if cur_comment.parent_id[0:2] == 't1':
#             cur_cid = cur_comment.parent_id[3:]
#         else:
#             cur_cid = cur_comment.parent_id
#         Num_comment = Num_comment - 1


class comment_node:
    comment_id = ''
    parent_id = ''
    user_id = ''
    score = 0
    timestamp = ''
    comment_word = ''
    parent_is_post = 0

    def __init__(self):
        self.comment_id = ''
        self.parent_id = ''
        self.user_id = ''
        self.score = 0
        self.timestamp = ''
        self.comment_word = ''
        self.parent_is_post = 0

    def add_to_node(self, cid, pid, uid, t, cw, pip, s):
        self.comment_id = cid
        self.parent_id = pid
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

    def add_to_node(self, target_uid, score):
        if score >= 0.5:
            self.pos_comment += 1
        else:
            self.neg_comment += 1
        if target_uid in self.list_of_users:
            idx = self.list_of_users[target_uid]
            if score >= 0.5:
                self.pos_num[idx] += 1
            else:
                self.neg_num[idx] += 1
            # self.average_score[idx] = self.pos_num[idx] / \
            #     (self.pos_num[idx] + self.neg_num[idx])
        else:
            self.num_of_users += 1
            self.list_of_users[target_uid] = self.num_of_users
            if score >= 0.5:
                self.pos_num.append(1)
                self.neg_num.append(0)
                self.average_score.append(1.0)
            else:
                self.pos_num.append(0)
                self.neg_num.append(1)
                self.average_score.append(0.0)

    # def __del__(self):
    #     self.list_of_users = {}
    #     self.


File_name = '2015-07-politics-sentiment.csv'
Num_input = 1000000
datas = []
tresh_num_comment = 0
dict_user_to_score = {}
users_score = []
# total num 337659

comment_mode = 0
user_mode = 1

timestamp_list = [1435708801, 1436572801, 1437177601, 1437782401, 1438387199]


with open(File_name, encoding='utf-8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        # print(row)
        if len(row) == 9 and row[5] != 'AutoModerator' and row[5] != '[deleted]':
            Num_input = Num_input - 1
            row[6] = row[6].rstrip()
            if Num_input <= 0:
                break
            if row[0] != 'id':
                # link=parent post
                if row[2] == row[3]:
                    datas.append([row[0], row[2][3:], row[5],
                                  row[6], int(row[7]), 1, float(row[8])])
                else:
                    datas.append([row[0], row[2][3:], row[5],
                                  row[6], int(row[7]), 0, float(row[8])])


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
                data[0], data[1], data[2], data[3], data[4], data[5], data[6])
            # print(type(dict_comments), type(new_comment_node))
            dict_comments[data[0]] = new_comment_node
            if data[2] in dict_users_to_comments:
                dict_users_to_comments[data[2]].append(data[0])
            else:
                dict_users_to_comments[data[2]] = [data[0]]

    for data in datas:
        if data[4] >= start_time and data[4] <= end_time and data[1] in dict_comments:
            if data[2] in dict_users:
                target_uid = dict_comments[data[1]].user_id
                dict_users[data[2]].add_to_node(target_uid, data[6])
            else:
                cur_user_node = user_node()
                cur_user_node.user_name = data[2]
                target_uid = dict_comments[data[1]].user_id
                cur_user_node.add_to_node(target_uid, data[6])
                dict_users[data[2]] = cur_user_node

    print('Finish processing')

    Output_Node_File_name = File_name[:-4] + \
        '_output_node_week'+str(num_week+1)+'_thresh=0.csv'
    # print(Output_Node_File_name)
    Output_Edge_File_name = File_name[:-4] + \
        '_output_edge_week'+str(num_week+1)+'_thresh=0.csv'
    # print(Output_Edge_File_name)

    for k, user in dict_users.items():
        # print(user.user_name, user.pos_comment, user.neg_comment)
        user.total_average_score = (
            user.pos_comment) / (user.pos_comment + user.neg_comment)
        for replied_user, idx in user.list_of_users.items():
            user.average_score[idx] = (
                user.pos_num[idx]) / (user.pos_num[idx] + user.neg_num[idx])

    print('Finish calculating')

    with open(Output_Edge_File_name, mode='w', newline='') as output_file:
        output_writer = csv.writer(
            output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(['Source', 'Target', 'Score'])

        for k, user in dict_users.items():
            # print(user.user_name, user.num_of_users)
            if user.pos_comment+user.neg_comment >= tresh_num_comment:
                for user_replied, user_idx in (user.list_of_users).items():
                    if user_replied in dict_users:
                        # print(user.user_name, user.num_of_users, len(user.list_of_users),user_replied, user_idx)
                        output_writer.writerow(
                            [user.user_name, user_replied, user.average_score[user_idx]])

                        # output_writer.writerow(
                        #     [user.user_name, user_replied, user.average_score[user_idx], user.pos_num[user_idx], user.neg_num[user_idx]])

    print('Finish Edge output')

    with open(Output_Node_File_name, mode='w', newline='') as output_file:
        output_writer = csv.writer(
            output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(
            ['Id', 'Score', 'Pos_num', 'Neg_num', 'Total_num'])

        for k, user in dict_users.items():
            if user.pos_comment + user.neg_comment >= tresh_num_comment:
                # output_writer.writerow(
                #     [user.user_name, user.total_average_score])
                output_writer.writerow(
                    [user.user_name, user.total_average_score, user.pos_comment, user.neg_comment, user.pos_comment+user.neg_comment])

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


# for cid, comment in dict_comments.items():
#     user_id = comment.user_id
#     if len(dict_users_to_comments[user_id]) > 5:
#         print(user_id)


# G = nx.Graph()
# start_cid = 'cstb5l2'
# Find_comment_reply_int(start_cid)

# print(G.number_of_nodes())
# print(G.number_of_edges())

# plt.subplot(111)
# nx.draw(G, with_labels=True, font_weight='bold')
# # plt.subplot(122)
# # nx.draw_shell(G, nlist=[range(5, 10), range(5)],
# #               with_labels=True, font_weight='bold')

# plt.show()


# Find those parent in data
# for cid, comment in dict_comments.items():
#     if comment.parent_id in dict_comments:
#         print(cid, comment.parent_id)


# for cid, comment in dict_comments.items():
#     G.add_node(cid)
# print(cid)
# comment.print_node()

# for user in items(dict_users_to_comments):
#     G.add_node(user)
# comment = []
# user = []
# Num = 100000

# with open(File_name, encoding='utf-8') as csvfile:
#     readCSV = csv.reader(csvfile, delimiter=',')
#     for row in readCSV:
#         if len(row) == 6:
#             Num = Num - 1
#             # print(row)
#             comment.append(row[0])
#             user.append(row[1][3:])
#             if Num <= 0:
#                 break

# comments = set(comment)
# users = set(user)

# print('csocqyf' in comments)
# print('csocqyf' in users)
# print('csocqz5' in comments)
# print('csocqz5' in users)
# print('csomuq9' in comments)
# print('csomuq9' in users)
# print('csocind' in comments)
# print('csocind' in users)
# print('csoci48' in comments)
# print('csoci48' in users)
