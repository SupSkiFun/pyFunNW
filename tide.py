import requests
import datetime

def _getTideTable(staID):
	'''Retrieve and Unmarshal JSON data within a 48 hour window'''
	dt = datetime.datetime.today().strftime('%Y%m%d')
	url = 'https://tidesandcurrents.noaa.gov/api/datagetter'
	params = {
		"product" : "predictions" ,
		"application" : "SupSkiFun" ,
		"begin_date" : dt ,
		"range" : 48 ,
		"datum" : "MLLW" ,
		"station" : staID ,
		"time_zone" : "lst_ldt" ,
		"units" : "english" ,
		"interval" : "hilo" ,
		"format" : "json" ,
		}
	try:
		res = requests.get(url,params=params)
		res.raise_for_status()
	except requests.exceptions.HTTPError as err:
		return "Problem accessing the below URL for " +staID+ " tides:\n" + str(err)
	else:
		if "error" in str(res.content):
			return "Problem accessing data for Station" +staID+ " tides:\n" + str(res.content)
		else:
			jrd = res.json()
			return jrd

def _printTideTable(tideData , staID , banner):
	'''Parse and Print JSON Data'''
	if banner:
		print("\nTide Charts for Station " +staID+ ":\n")
	for j in tideData['predictions']:
		if j['type'] == "H":
			tidetype = "High"
		elif j['type'] == "L":
			tidetype = "Low"
		else:
			tidetype = "Unknown"
		print(j['t']+"\t"+tidetype+"\t"+j['v'])
	print("\n")

def getTide(staID , banner = True):
	''' Retrieve Weather from submitted Station ID

	Arguments:

	staID:  7 digit station ID - https://tidesandcurrents.noaa.gov/stations.html

	banner:  set to False to supress printing station banner info with tide charts
	'''
	staID = str(staID)
	tideData = _getTideTable(staID)
	if "Problem" in tideData:
		print(tideData)
		print("\n")
	else:
		_printTideTable(tideData , staID , banner)


