import json
import sys
import os
import heapq
import csv


list_input_file = ['RC_2017-05']
list_subreddit = ['politics', 'MadeMeSmile', 'Incels', 'The_Donald', 'gaming']
dict_user = {}

for cur_file in list_input_file:
    Input_file = open(cur_file, 'r')
    for line in Input_file:
        j = json.loads(line)
        if j['author'] != '[deleted]' and j['subreddit'] in list_subreddit:
            cur_author = j['author']
            # print(cur_author,j['subreddit'])
            if cur_author not in dict_user:
                dict_user[cur_author] = [0, 0, 0, 0, 0]
            idx = list_subreddit.index(j['subreddit'])
            dict_user[cur_author][idx] += 1
            print(cur_author, dict_user[cur_author])

list_count = [[], [], [], [], []]
for k, v in dict_user.items():
    for i in range(5):
        if v[i]:
            list_count[i].append([k, v[i]])

for i in range(5):
    list_count[i] = heapq.nlargest(1000, list_count[i], key=lambda e: e[1])
    Output_file = open('1000Authors_' + list_subreddit[i] + '.txt', 'w')
    for cur_author in list_count[i]:
        Output_file.write(cur_author[0])
        Output_file.write('\n')
