import requests
import datetime
import argparse

parser = argparse.ArgumentParser(description="""Return Tide Predictions For Eagle Harbor
by default, or for seven station in proximity of Eagle Harbor if -all specified.""")
parser.add_argument('-all', action='store_true' , required=False ,
	help="""Returns Tide Predictions for 7 stations in proximity of Eagle Harbor.
	Absence of this parameter will provide Tide Predictions for Eagle Harbor only.""")
args = vars(parser.parse_args())

dt = datetime.datetime.today().strftime('%Y%m%d')

#  For Adding Lat and Long to below
#  https://tidesandcurrents.noaa.gov/tide_predictions.html?gid=1415
#  https://www.tidesandcurrents.noaa.gov/api/

stations = {
	9445882 : "Eagle Harbor" ,
	9445753 : "Port Madison - North of Island" ,
	9445913 : "Port Blakely - Blakely Harbor" ,
	9445938 : "Clam Bay, Rich Passage - South of Island" ,
	9445832 : "Brownsville - West of Island" ,
	9445958 : "Bremerton, Sinclair Inlet" ,
	9445719 : "Poulsbo, Liberty Bay" ,
}

def getTideTable(staID,staName):
	'''Retrieve and Marshal JSON data for submitted Station IDs'''
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
		print("Problem Accessing the below URL:")
		print(err)
	else:
		jrd = res.json()
		printTideTable(jrd,staName)

def printTideTable(jrd,staName):
	'''Parse and Print JSON Data along with the Station Name'''
	print("\nTide Predictions " +staName+ "\n")
	for j in jrd['predictions']:
		if j['type'] == "H":
			tidetype = "High"
		elif j['type'] == "L":
			tidetype = "Low"
		else:
			tidetype = "Unknown"
		print(j['t']+"\t"+tidetype+"\t"+j['v'])

def main():
	if args['all']:
		for staID , staName in stations.items():
			getTideTable(staID , staName)
	else:
		getTideTable(9445882,"Eagle Harbor")

if __name__ == "__main__":
	main()

#  https://www.tidesandcurrents.noaa.gov/api/