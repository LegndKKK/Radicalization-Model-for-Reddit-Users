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
dict_users_history_score = {}

File_name_list = ['RC_2015-07-politics-toxic.csv']

start_time = int(calendar.timegm(tuple([2015, 7, 5, 0, 0, 0])))
end_time = int(calendar.timegm(tuple([2015, 7, 12, 0, 0, 0])))

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

dict_comments = {}
list_user = []

# loop over comments
for data in datas:
    if data[4] >= start_time and data[4] <= end_time:
        new_comment_node = comment_node()
        new_comment_node.add_to_node(
            data[0], data[1], data[7], data[2], data[4], data[3], data[5], data[6])
        dict_comments[data[0]] = new_comment_node
        list_user.append(data[2])

set_user = set(list_user)
list_user = list(set_user)

print(len(list_user))

random_index = random.sample(range(len(list_user)), 100)
list_random_user = []
for i in random_index:
    list_random_user.append(list_user[i])

list_edge = []
list_comment = []
for k, v in dict_comments.items():
    if v.user_id in list_random_user:
        list_comment.append(v.comment_id)
        if v.parent_id not in dict_comments:
            continue
        list_comment.append(v.parent_id)
        list_edge.append([v.comment_id, v.parent_id])
set_comment = set(list_comment)
list_comment = list(set_comment)


with open('Comment_network_Node.csv', mode='w') as Node_Output:
    node_writer = csv.writer(
        Node_Output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    node_writer.writerow(['Id', 'Author_id', 'Score'])
    for cur_comment in list_comment:
        node_writer.writerow(
            [cur_comment, dict_comments[cur_comment].user_id, dict_comments[cur_comment].score])

with open('Comment_network_Edge.csv', mode='w') as Edge_Output:
    edge_writer = csv.writer(
        Edge_Output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    edge_writer.writerow(['Source', 'Target'])
    for i in list_edge:
        edge_writer.writerow(i)


# with open('Comment_network_Node.csv', mode='w') as Output:
#     output_writer = csv.writer(
#         Output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     output_writer.writerow(['Id', 'Author_id', 'Score'])
#     for k, v in dict_comments.items():
#         output_writer.writerow([v.comment_id, v.user_id, v.score])


# with open('Comment_network_Edge.csv', mode='w') as Output:
#     output_writer = csv.writer(
#         Output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     output_writer.writerow(['Source', 'Target'])
#     for k, v in dict_comments.items():
#         if v.parent_id in dict_comments:
#             output_writer.writerow([v.comment_id, v.parent_id])
