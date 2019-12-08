import csv

folder ="MadeMeSmile"
users = dict()
n1 =13
n2 =15
for i in range(6):
	with open(folder+"/"+"Author_result_"+str(i)+".csv") as readfile:
		csvreader= csv.reader(readfile)
		seen = set()
		for line in csvreader:
			if(line[0] == "Id"):
				continue
			if(line[0] in seen):
				continue
			else:
				seen.add(line[0])
			if line[0] not in users:

				if(float(line[n1]) == -1):
					users[line[0]] = ["Null"]
					continue
				else:
					num1=float(line[n1])

				if(float(line[n2]) == -1):
					users[line[0]] = ["Null"]
					continue
				else:
					num2=float(line[n2])
				users[line[0]] = [(num1, num2)]
			else:
				if(float(line[n1]) == -1):
					users[line[0]].append("Null")
					continue
				else:
					num1=float(line[n1])

				if(float(line[n2]) == -1):
					users[line[0]].append("Null")
					continue
				else:
					num2=float(line[n2])
				users[line[0]].append((num1, num2))

for user in users:
	if(len(users[user])!=6):
		print(user)
		print(len(users[user]))

with open("mademesmileratio.csv", "w") as writefile:
	csvwriter = csv.writer(writefile)
	for user in users:
		row = [user, ""]
		row += users[user]
		csvwriter.writerow(row)