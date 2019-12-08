# Radicalization-Model-for-Reddit-Users

This is the course project of Networks in Real World.
This project aims to create an equation to predict how Reddit users get radicalized. We define radical users as users who say mostly if not all negative comments. We use a NLP sentiment analysis model to determine the negativity of a comment. This data is used to formulate a network that shows the progression of negative users which will ultimately allow us to come up with an equation for radicalization.

You can set up input file, output file, tune step, number of most changed user, number of most negative user, thresholds. For detailed explanation of code usage

##### python Data_reading_Network_building.py -h

### Data_reading_Network_building.py

This code is for chronological method in user appraoch. It reads the data extracted from raw data file and find out the most changed users and most negative users in each time step. It outputs the edge and node files for network building which can be read in Gephi. The output network data includes each user as a node and the interactions between uesrs as edges.

##### python Data_reading_Network_building.py -i InputFile_politics.txt -o politics -ts 1 -th 10 -nmc 50 -nmn 50 -thc 0.18 -thm 1 -thn 0.75

### Data_reading_Network_building_Backtracking.py

This code is for backtracking method in user appraoch. It reads the data extracted from raw data file and find out the most changed users over 6 months. Then try to find out the connection between the most changed users and the most negative users in each time step. It outputs the edge and node files for network building which can be read in Gephi. The output network data includes each user as a node and the interactions between uesrs as edges.

##### python Data_reading_Network_building_Backtracking.py -i InputFile_politics.txt -o politics -ts 1 -th 10 -nmc 50 -nmn 50 -thc 0.18 -thm 1 -thn 0.75

### Data_reading_Network_building_OverallAnalysis.py

This code analyzes the parent-child pair in given data. It will generate the count of four different parent-child pairs in input data.

##### python Data_reading_Network_building_OverallAnalysis.py -i InputFile_politics.txt

### Data_reading_Network_building_Comment.py

This code is for network building in comment approach. It reads the extracted data from raw data and outputs the network data including nodes and edges which can be read in Gephi. It takes each comment as a node and the edge exists if there is a parent-child connection.

##### python Data_reading_Network_building_Comment.py -i InputFile_politics.txt

### Data_reading_Network_building_Authors.py

This code is for further score analysis in  comment approach. It reads the extracted data after sentiment analysis and outputs the file containing user score in current subreddit, parent score in current subreddit, user score not in current subreddit, parent score not in current subreddit and ratio that the user speaks in current subreddit. In out project, we get top 1000 active users in five different subreddits r/politics, r/The_Donald, r/MakeMeSmile. r/gaming and r/Incels. We track those users' comments and calculate their scores by this script.

##### python Data_reading_Network_building_Authors.py -i InputFile_politics.txt

### parseauthorresults.py
Parses the data generated from the comment approach into a format readable by graph.py. Set variables to be read in the script


#### python parseauthorresults.py

### graph.py
Visualizes the data generated parseauthorsresults.py. Set variables to be read in the script

#### python graph.py

### NLPTrain.py
Trains and saves a CNN model for toxic classification using the kaggle toxic dataset. Set variables to be read in the script


#### python NLPTrain.py

### NLPClassify.py 
Classifies reddit comments as toxic or not toxic. Set variables to be read in the script


#### python NLPClassify.py


Joseph Wang and Jikai Zhang
