import os
import csv

#######################################CREATE SINGLE TEAM SCHEDULE#########################################

#create schedule from big all league sched, write to csv
def createsched(team, sched):
	files = os.listdir('.')
	timezone = sched[0][3].split('IME ')[1]
	game = []
	for file in files:
		if 'leaguesched' in file:
			schedule = file
			
	zonetohour = { '(ET)':0, '(CT)':1, '(MT)':2, '(PT)':3 }
	
	with open(schedule, 'rb') as csvfile:
		csvreader = csv.reader(csvfile)
		for row in csvreader:
			if (team in row[0]) or (team in row[1]):
				game = row
				hour = game[3].split(':')[0]
				therest = game[3].split(':')[1]
				newhour = (int(hour) - zonetohour[timezone]) % 12
				if newhour > hour and 'PM' in therest: #IF CHANGED FROM PM TO AM, REMOVE PM.  ADD AM
					therest = therest.split(' PM')[0] + ' AM'
				elif newhour > hour and 'AM' in therest: #IF CHANGED FROM AM TO PM, REMOVE AM.  ADD PM
					therest = therest.split(' AM'[0]) + ' PM'
				gametime = str(newhour)+':'+therest
				game[3] = gametime
				###PUT TIME BACK TOGETHER FIRST
				
				month = game[2].split(' ')[0] #TURN DATE INTO MM/DD/YYYY FORMAT
				year = game[2].split(' ')[2]
				day = game[2].split(' ')[1].split(',')[0]
				monthtoint = { 'JAN':'1', 'FEB':'2', 'MAR':'3', 'APR':'4', 'MAY':'5', 'JUN':'6', 'JUL':'7', 'AUG':'8', 'SEP':'9', 'OCT':'10', 'NOV':'11', 'DEC':'12' }
				game[2] = monthtoint[month.upper()]+'/'+day+'/'+year
				
				sched.append(game) #sched got the header line before this function
	
	with open(team.lower()+'.csv', 'wb') as csvfile:
		csvwriter = csv.writer(csvfile)
		for game in sched:
			csvwriter.writerow(game)
	
	sched = [ ['HOME', 'AWAY', 'DATE', 'TIME'] ]
	return sched

################################################REARRANGE##################################################

def rearrange(row):
	line = []
	line.append(row[2])#HOME -- [0]
	line.append(row[1])#AWAY -- [1]
	line.append(row[0])#DATE -- [2]
	line.append(row[3])#TIME -- [3]
	
	print line
	return line
	
############################################CLEAN UP########################################################

def clean(line):	
	if line[2] != 'DATE':
		line[2] = line[2][4:] #REMOVE MON/TUE/WED/THU/FRI/SAT/SUN FROM DATE
	
	if line[3] == 'TIME':
		line[3] = 'TIME (ET)' #PUT TIME ZONE IN HEADER
	
	if 'ET' in line[3]:
		line[3] = line[3].split(' ET')[0] #REMOVE TIME ZONE FROM ENTRY
		
	teamtoabbrev = {'HOME TEAM':'HOME', 'VISITING TEAM':'AWAY', 'ATLANTA':'ATL', 'ANAHEIM':'ANH', 'PHOENIX':'ARI', 'ARIZONA':'ARI', 'BOSTON':'BOS', 'BUFFALO':'BUF',  'CALGARY':'CGY', 'CAROLINA':'CAR', 'CHICAGO':'CHI', 'COLORADO':'COL', 'COLUMBUS':'CBJ', 'DALLAS':'DAL', 'DETROIT':'DET', 'EDMONTON':'EDM', 'FLORIDA':'FLA', 'LOS ANGELES':'LAK', 'MINNESOTA':'MIN', 'MONTREAL':'MON', 'NASHVILLE':'NSH', 'NEW JERSEY':'NJD', 'NY ISLANDERS':'NYI', 'NY RANGERS':'NYR', 'OTTAWA':'OTT', 'PHILADELPHIA':'PHI', 'PITTSBURGH':'PIT', 'SAN JOSE':'SJS', 'ST. LOUIS':'STL', 'TAMPA BAY':'TBL', 'TORONTO':'TOR', 'VANCOUVER':'VAN', 'WASHINGTON':'WSH', 'WINNIPEG':'WPG'}
	line[0] = teamtoabbrev[line[0].upper()]
	line[1] = teamtoabbrev[line[1].upper()]
	return line

###########################################################################################################

files = os.listdir('.')
schedule = ''

for file in files:
	if 'nhlsched' in file:
		schedule = file
		print schedule
		break

leaguesched = []
empty = ['','','','']
csvfile = open(schedule, 'rb') #open reader
csvreader = csv.reader(csvfile)
line = []

with open('leaguesched'+schedule.split('sched')[1], 'wb') as csvfile2:
	csvwriter = csv.writer(csvfile2)
	for row in csvreader: #read first file
		if row != empty: #if row isn't empty
			line = rearrange(row) #rearrange row	
			line = clean(line)
			csvwriter.writerow(line) #write to file
csvfile.close()

singleteamsched = [ ['HOME', 'AWAY', 'DATE', 'TIME'] ]
teamtimezone = {'ATL':'ET', 'ANH':'PT', 'ARI':'MT', 'BOS':'ET', 'BUF':'ET', 'CGY':'MT', 'CAR':'ET', 'CHI':'CT', 'COL':'MT', 'CBJ':'CT', 'DAL':'CT', 'DET':'CT', 'EDM':'MT', 'FLA':'ET', 'LAK':'PT', 'MIN':'CT', 'MON':'ET', 'NSH':'CT', 'NJD':'ET', 'NYI':'ET', 'NYR':'ET', 'OTT':'ET', 'PHI':'ET', 'PIT':'ET', 'SJS':'PT', 'STL':'CT', 'TBL':'ET', 'TOR':'ET', 'VAN':'PT', 'WSH':'ET', 'WPG':'CT'}

for entry in teamtimezone:
	singleteamsched[0][3] = singleteamsched[0][3]+' ('+teamtimezone[entry]+')'
	singleteamsched = createsched(entry, singleteamsched)