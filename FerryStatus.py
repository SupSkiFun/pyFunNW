import requests
from datetime import datetime

def getFerrySchedule(terminal):
    '''Retrieves the Next 4 Departing Ferries from submitted terminals'''
    urlbase = 'http://www.wsdot.wa.gov/Ferries/API/Terminals/rest/terminalsailingspace/'
    schedURL = urlbase+str(terminal)+'?'+urlcode
    try:
        res4 = requests.get(schedURL , headers = header)
        res4.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("Problem Accessing the below URL for sailing space status:")
        print(err)
    else:
        jrd4 = res4.json()
        printFerrySchedule(jrd4)

def getFerryStatus(vesselID):
    '''Retrives status of first ferry in list of departing ferries from submitted terminals'''
    urlbase2 = 'http://www.wsdot.wa.gov/Ferries/API/Vessels/rest/vessellocations/'
    url = urlbase2+vesselID+urlcode
    try:
        res = requests.get(url , headers = header)
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("Problem Accessing the below URL for current ferry status:")
        print(err)
    else:
        jrd = res.json()
        printFerryStatus(jrd)

def printFerrySchedule(jrd4):
    '''Prints the Next 4 Departing Ferries from submitted terminals.'''
    # Used counter instead of slices; Seattle has ferries to BI and Bremerton; BI only has ferries to Seattle.
    tcount = 1
    checkFerry = True
    print("\n\t" + jrd4['TerminalName'] + " Terminal Ferry Departure Schedule" +"\n")
    for x in jrd4['DepartingSpaces']:
        for y in x['SpaceForArrivalTerminals']:
            if tcount < 5:
                if "Bainb" in y['TerminalName'] or "Seattle" in y['TerminalName']:
                    print(datetime.fromtimestamp(int(x['Departure'].split('(')[1][:10])).strftime('%d-%b-%Y %H:%M'))
                    print(y['VesselName'])
                    print(y['DriveUpSpaceCount'])
                    if x['IsCancelled']:
                            print("Ferry is cancelled")
                    if checkFerry:
                        getFerryStatus(str(y['VesselID'])+'?')
                        checkFerry = False
                    print("------------------")
                    tcount += 1
            else:
                break

def printFerryStatus(jrd):
    '''Prints status of first ferry in list of departing ferries from submitted terminals'''
    if jrd['AtDock']:
        #if jrd['ScheduledDeparture'] is None:   ORIGINAL LINE
        if None in (jrd['ScheduledDeparture'] , jrd['DepartingTerminalName'] , jrd['ArrivingTerminalName']):
            #print("No Departure Time from " + jrd['DepartingTerminalName'] + " available.  Try again in 90 seconds.")  ORIGINAL LINE
            print("No Departure Time available.  Try again in 90 seconds.")
        else:
            vdtd = datetime.fromtimestamp(int(jrd['ScheduledDeparture'].split('(')[1][:10])).strftime('%d-%b-%Y %H:%M')
            print("At Dock in "+ jrd['DepartingTerminalName'] + '.  Scheduled Departure to ' + jrd['ArrivingTerminalName']   + ' at ' + vdtd )
    else:
        if jrd['Eta'] is None:
            print("No Arrival Time to " + jrd['ArrivingTerminalName'] + " available.  Try again in 90 seconds.")
        else:
            vdta = datetime.fromtimestamp(int(jrd['Eta'].split('(')[1][:10])).strftime('%d-%b-%Y %H:%M')
            print("Estimated Arrival to " + jrd['ArrivingTerminalName']   + " from " + jrd['DepartingTerminalName'] + " at " + vdta)

def main():
    terminals = {
        3 : "Bainbridge Island" ,
        7 : "Seattle" ,
	}
    for t in terminals:
        getFerrySchedule(t)

urlcode = 'apiaccesscode=myCoolKey'
header = {'Accept' : 'application/json'}

if __name__ == "__main__":
    main()

