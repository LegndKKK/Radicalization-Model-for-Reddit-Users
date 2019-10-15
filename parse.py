import json
import sys
import os
import argparse
import csv

def main():
    if(len(sys.argv) < 4):
        raise Exception("usage: python3 parse.py {json file of reddit} {object to parse by} {text file containing things to parse} e.g. python3 parse.py RC_2017-10 subreddit subreddits-to-parse.txt")
    f = open(sys.argv[1], "r")
    g = open(sys.argv[3], "r")
    target = sys.argv[2]
    

    subreddits = []
    for line in g:
        subreddits.append(line.strip())
    print(subreddits)

    folder = sys.argv[1] + "-" + sys.argv[2] + "-Parsed"
    os.mkdir(folder)
    csv_writers = dict()
    for sub in subreddits:
        csv_writers[sub] = csv.writer(open(folder+"/"+sub+'-PARSED.csv', 'w', encoding="utf-8"))
        row = ["id", "parent_id", "link_id", "subreddit", "author", "body", "created_utc"]
        csv_writers[sub].writerow(row)
    cur_line = 0
    for line in f:
        cur_line+=1
        if(cur_line%10000 == 0):
            print(cur_line)
        j = json.loads(line)
        if(j[target] in subreddits):
            comment_id = j["id"]
            parent_id = j["parent_id"]
            author = j["author"]
            body = j["body"]
            subreddit = j["subreddit"]
            ups = j["score"]
            utc = j["created_utc"]
            link = j["link_id"]
            row = [comment_id, parent_id, link, subreddit, author, body, str(utc)]
            csv_writers[j[target]].writerow(row)
    return

main()