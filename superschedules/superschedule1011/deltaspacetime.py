import csv
import os

##############################LOOK AT TIMES BETWEEN GAMES##################################################

def calculatehours(currentgame, seasonstart, prevtime):
	gamemonth = int(currentgame[2].split('/')[0])
	gameday = int(currentgame[2].split('/')[1])
	gameyear = int(currentgame[2].split('/')[2])
	gamehourstring = currentgame[3].split(' ')[0]
	gamehour = float(gamehourstring.split(':')[0]) + (0.5 if gamehourstring.split(':')[1] == '30' else 0.0)
	if currentgame[3].split(' ')[1] == 'PM' and gamehour != 12.0:
		gamehour += 12
	
	seasonopener = seasonstart[0] #unpack list
	seasonstarttime = seasonstart[1]
	
	startmonth = int(seasonopener.split('/')[0])
	startday = int(seasonopener.split('/')[1])
	startyear = int(seasonopener.split('/')[2])
	starthourstring = seasonstarttime.split(' ')[0]
	starthour = float(starthourstring.split(':')[0]) + (0.5 if starthourstring.split(':')[1] == '30' else 0.0)
	if seasonstarttime.split(' ')[1] == 'PM':
		starthour += 12
	
	hoursinfeb = 28*24 #minimum hours in feb
	if gameyear % 4 == 0 and not ((gameyear % 100 == 0) and (gameyear % 400 != 0)):
		hoursinfeb += 24
	
	hoursinmonth = [0, 31*24.0, float(hoursinfeb), 31*24.0, 30*24.0, 31*24.0, 30*24.0, 31*24.0, 31*24.0, 30*24.0, 31*24.0, 30*24.0, 31*24.0]
	#indeces set so hoursinmonth[1] gives hours in january, etc...
	
	#HOURS FROM SEASON OPENER TO NEW YEARS
	prior_chunk = 0 
	for x in range(startmonth, 13):
		prior_chunk += hoursinmonth[x] #add hours in months before new years
	prior_chunk -= (startday - 1)*24.0 #subtract extra days prior to opening day in start month
	prior_chunk -= starthour #subtract hours before puck drop on opening day
		
	###################HOURS IN A MONTH HAS BEEN SET.  NOW START TO ACTUALLY CALCULATE TIMES###############
	#SEASON START -- startmonth, startday, startyear, starthour (ALL INTS BUT starthour)
	# GAME START  -- gamemonth,  gameday,  gameyear,  gamehour   (ALL INTS BUT gamehour)
	if gameyear == startyear:
		#CALCULATIONS ONE WAY
		for x in range(startmonth, gamemonth): #don't include startmonth
			gamehour += hoursinmonth[x]
		
		gamehour -= (startday - 1)*24.0 #subtract days before opening puck drop
		gamehour -= starthour #subtract hours before opening puck drop on opening day
		
		gamehour += (gameday - 1) * 24.0 #don't include gameday itself.  only some of it (in gamehour)
		#above adds days in current month that've already elapsed
	else:
		#CALCULATIONS ANOTHER WAY
		for x in range(1, gamemonth): #add months before game month
			gamehour += hoursinmonth[x] 
		gamehour += (gameday - 1) * 24.0 #days before gameday, started with hours before puckdrop on gameday
		gamehour += prior_chunk
	return (gamehour - prevtime)

##############################FIND DISTANCES, CREATE NEW FILE##############################################

def processdistance(team):
	with open(team, 'rb') as distancefinder:
		distancereader = csv.reader(distancefinder)
		teamsched = [ ['HOME', 'AWAY' , 'DATE', 'LOCAL TIME', 'DIST FROM', 'TIME SINCE'] ]
		currentgame = []
		prevlocation = team.split('.')[0].upper() #assume starting at home, include travel to season opener
		fromprev = 0
		prevtime = 0
		for game in distancereader:
			if game[0] == 'HOME': #ignore this row
				continue
			else:
				currentgame = game
				if len(teamsched) == 1: #Set season start date and time
					seasonopener = game[2]
					seasonstarttime = game[3]
				#distancematrix[teamtonumber[prevlocation]] gets the number index from teamtonumber
				#and the second index from teamtonumber[game[0]]
				currentgame.append( distancematrix[teamtonumber[prevlocation]][teamtonumber[game[0]]] ) #add distance to game entry
				currentgame.append( calculatehours(currentgame, [seasonopener, seasonstarttime], prevtime) ) #add time since last game to game entry
				prevtime += currentgame[5] #ADD TIME SINCE LAST GAME
				prevlocation = game[0] #update previous game
				teamsched.append(currentgame) #add game to schedule
	
	with open('deltaspacetime-'+team, 'wb') as csvfile:
		distancewriter = csv.writer(csvfile)
		for game in teamsched:
			distancewriter.writerow(game)
				
			

##########################################GET FILES########################################################

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

#Dictionary - team abbreviation to index in distancematrix
teamtonumber = {'ANH':1, 'ARI':2, 'BOS':3, 'BUF':4, 'CGY':5, 'CAR':6, 'CHI':7, 'COL':8, 'CBJ':9, 'DAL':10, 'DET':11, 'EDM':12, 'FLA':13, 'LAK':14, 'MIN':15, 'MON':16, 'NSH':17, 'NJD':18, 'NYI':19, 'NYR':20, 'OTT':21, 'PHI':22, 'PIT':23, 'SJS':24, 'STL':25, 'TBL':26, 'TOR':27, 'VAN':28, 'WSH':29, 'ATL':30}
distancematrix = []

#######################################READ ALL DISTANCES##################################################

with open('distances.csv', 'rb') as distances:
	distancereader = csv.reader(distances)
	for row in distancereader:
		distancematrix.append(row)

for item in files:
	processdistance(item)
		
