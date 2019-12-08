import json
import sys
import os
import argparse
import csv

FILE = "RC_2017-"
SAVENAME = "RC_2017-"
authorfiles = ["1000Authors_gaming.txt", "1000Authors_The_Donald.txt",
               "1000Authors_Incels.txt", "1000Authors_MadeMeSmile.txt", "1000Authors_politics.txt"]
subreddits = ["gaming", "The_Donald", "Incels", "MadeMeSmile", "politics"]


def main():
    authors = dict()
    parents = dict()
    for i in range(len(subreddits)):
        with open(authorfiles[i]) as f:
            for line in f:
                if line.strip() not in authors:
                    authors[line.strip()] = set()
                authors[line.strip()].add(subreddits[i])

    print(authors)

    for number in ["05", "06"]:

        f = open(FILE+number, "r")

        target = "subreddit"

        cur_line = 0
        for line in f:
            cur_line += 1
            if(cur_line % 10000 == 0):
                print(number, cur_line,  len(parents))
            j = json.loads(line)

            if(j["author"] in authors):
                if(j["parent_id"][3:] not in parents):
                    parents[j["parent_id"][3:]] = set()
                parents[j["parent_id"][3:]].update(authors[j["author"]])

        csv_writers = dict()
        for s in subreddits:
            csv_writer = csv.writer(
                open(SAVENAME+number+"-"+s+"-FoundAuthorsCorrect.csv", 'w', encoding="utf-8"))
            row = ["id", "parent_id", "link_id",
                   "subreddit", "author", "body", "created_utc"]
            csv_writer.writerow(row)
            csv_writers[s] = csv_writer
        #authors = set()
        #unwanted_authors = ["AutoModerator", "deleted"]
        #num_authors = 0
        # for line in f:
        #    j = json.loads(line)
        #    if(j[target] in subreddits):
        #        if(j["author"] not in unwanted_authors and j["author"] not in authors):
        #            num_authors += 1
        #            if(num_authors%1000==0):
        #                print(num_authors)
        #            authors.add(j["author"])
        #visited_ids = set()

        f = open(FILE+number, "r")
        cur_line = 0
        for line in f:
            cur_line += 1
            if(cur_line % 10000 == 0):
                print(number, cur_line)
            j = json.loads(line)

            if(j["author"] in authors or j["id"] in parents):
                comment_id = j["id"]
                parent_id = j["parent_id"]
                author = j["author"]
                body = j["body"]
                subreddit = j["subreddit"]
                #stickied = j["stickied"]
                #score = j["score"]
                ups = j["score"]
                utc = j["created_utc"]
                link = j["link_id"]
                #name = j["name"]
                # str(stickied), str(score), str(ups), str(utc)]
                row = [comment_id, parent_id, link,
                       subreddit, author, body, str(utc)]
                if author in authors:
                    for s in authors[author]:
                        csv_writers[s].writerow(row)
                if comment_id in parents:
                    for s in parents[comment_id]:
                        csv_writers[s].writerow(row)


            # visited_ids.add(j["id"])
main()
