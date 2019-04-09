import requests
from datetime import datetime

def _getFerrySchedule(terminal , header , param):
    '''Retrieves the Next 4 Departing Ferries from submitted terminals'''
    urlbase = 'http://www.wsdot.wa.gov/Ferries/API/Terminals/rest/terminalsailingspace/'
    schedURL = urlbase+str(terminal)
    try:
        res4 = requests.get(schedURL , headers = header, params = param)
        res4.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return "Problem Accessing the below URL for terminal " +terminal+ " status:\n" +str(err)
    else:
        jrd4 = res4.json()
        return jrd4

def _getFerryStatus(vesselID , header, param):
    '''Retrives status of first ferry in list of departing ferries from submitted terminals'''
    urlbase2 = 'http://www.wsdot.wa.gov/Ferries/API/Vessels/rest/vessellocations/'
    url = urlbase2+vesselID

    try:
        res = requests.get(url , headers = header, params= param)
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return "Problem Accessing the below URL for ferry " +vesselID+ " status:\n" + str(err)
    else:
        jrd = res.json()
        return jrd

def _printFerrySchedule(fdata , sailings , status , header , param):
    '''Prints the Next 4 Departing Ferries from submitted terminals.'''
    print("\n\t" + fdata['TerminalName'] + " Terminal Ferry Departure Schedule" +"\n")
    for x in fdata['DepartingSpaces'][:sailings]:
        for y in x['SpaceForArrivalTerminals']:
            dt = datetime.fromtimestamp(int(x['Departure'].split('(')[1][:10])).strftime('%d-%b-%Y %H:%M')
            print("Scheduled Departure:  " + dt)
            print("Destination:  " + y['TerminalName'])
            print("Ferry:  " + y['VesselName'])
            print("Available Car Spaces:  " + str(y['DriveUpSpaceCount']))
            if x['IsCancelled']:
                print("Sailing is cancelled")
                status = False
            if status:
                status = False
                jrd = _getFerryStatus(str(y['VesselID']) , header , param)
                _printFerryStatus(jrd)
            print("------------------")


def _printFerryStatus(jrd):
    '''Prints status of first ferry in list of departing ferries from submitted terminals'''
    if jrd['AtDock']:
        if None in (jrd['ScheduledDeparture'] , jrd['DepartingTerminalName'] , jrd['ArrivingTerminalName']):
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

def getSchedule(terminal, apiCode, sailings = 4, status = True):
    '''
    Retrieve and Print Ferry Schedule and Status for terminal from WSDOT.

    Arguments:

    terminal:  Terminal number. See VariousInfo.txt or http://www.wsdot.com/traffic/api/

    apiCode: Your access code.  http://www.wsdot.com/traffic/api/

    sailings: Number of departing ferries to list

    status: Obtain next ferry's current status

    '''

    header = {'Accept' : 'application/json'}
    param = {'apiaccesscode' : apiCode }

    fdata = _getFerrySchedule(terminal, header, param)
    if "Problem" in fdata:
        print(fdata)
        print("\n" + "Terminating due to lack of Terminal Information")
        raise SystemExit()
    else:
        _printFerrySchedule(fdata, sailings, status, header, param)
