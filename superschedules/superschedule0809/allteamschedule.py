import os
import csv

###########################################ADD GAMES#######################################################

def addgames(date, team):
	returnstring = ''
	teamname = team.split('.')[0].upper()
	with open(team, 'rb') as csvfile:
		matchfinder = csv.reader(csvfile)
		for row in matchfinder:
			if date[0] == row[2]:
				returnstring = row[1]+'-H' if row[0] == teamname else row[0]+'-A'
	return returnstring
			


###########################################GET FILES#######################################################

files = os.listdir('.') #get file list
indexlist = []
index = 0
for file in files:
	if len(file) != 7 or file[-3:] != 'csv': #all team files are XXX.csv - 7 characters
		indexlist.append(index) #see which need to be removed
		index += 1
	else:
		index += 1

indexlist.sort(reverse=True) #sort largest to smallest (to avoid changing indexes yet to be removed)
for index in indexlist:
	del files[index] #remove each list

teamtonumber = {'ANH':1, 'ARI':2, 'BOS':3, 'BUF':4, 'CGY':5, 'CAR':6, 'CHI':7, 'COL':8, 'CBJ':9, 'DAL':10, 'DET':11, 'EDM':12, 'FLA':13, 'LAK':14, 'MIN':15, 'MON':16, 'NSH':17, 'NJD':18, 'NYI':19, 'NYR':20, 'OTT':21, 'PHI':22, 'PIT':23, 'SJS':24, 'STL':25, 'TBL':26, 'TOR':27, 'VAN':28, 'WSH':29, 'WPG':30}

###########################################################################################################

allteamschedule = []

with open('bigschedule.csv', 'rb') as allgames:
	gamesreader = csv.reader(allgames)
	for row in gamesreader:
		allteamschedule.append(row)

for rwo in allteamschedule:
	if rwo == [] or rwo[0] == 'DATE\\TEAM':
		index = 7
	else:
		for team in files:
			rwo.append(addgames(rwo, team)) #MATCH date[0] & row[2], ADD OPPONENT IF MATCH == TRUE
	print rwo
	
with open('allgames.csv', 'wb') as allgames:
	gamewriter = csv.writer(allgames)
	for row in allteamschedule:
		gamewriter.writerow(row)