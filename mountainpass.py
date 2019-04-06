import requests
from datetime import datetime
from collections import namedtuple

'''Obtains Current Conditions and Weather Information for submitted Mountain Passes.'''

def _getPassCondition(passID , apiCode):
    '''Retrieve Pass Conditions from WSDOT'''
    baseUrl = 'http://www.wsdot.wa.gov/Traffic/api/MountainPassConditions/MountainPassConditionsREST.svc/GetMountainPassConditionAsJon?'
    payload = {
        'AccessCode' : apiCode ,
        'PassConditionID' : str(passID)
    }
    try:
        res=requests.get(baseUrl , params = payload)
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return "Problem Accessing the below URL for mountain pass conditions:\n" + str(err)
    else:
        jrd = res.json()
        tup = namedtuple('CondInfo',['passInfo','lat','lon'])
        t1 = datetime.fromtimestamp(int(jrd['DateUpdated'].split('(')[1][:10])).strftime('%d-%b-%Y %H:%M')
        passInfo = [
            str(jrd['ElevationInFeet'])+' Feet',
            str(jrd['TemperatureInFahrenheit'])+' Fahrenheit',
            jrd['WeatherCondition'],
            jrd['RoadCondition'],
            jrd['RestrictionOne']['TravelDirection'] + ":\t" + jrd['RestrictionOne']['RestrictionText'],
            jrd['RestrictionTwo']['TravelDirection'] + ":\t" + jrd['RestrictionTwo']['RestrictionText'],
            jrd['MountainPassName'],
            t1,
        ]
        lat = jrd['Latitude']
        lon = jrd['Longitude']
        ctup = tup(passInfo , lat , lon)    # Use lat and lon return to get weather
        return ctup

def _printPassCondition(passInfo):
    '''Print Weather Forecast from WSDOT'''
    print("---------------------------------------------\n")
    print("\t" + passInfo[-2] +" Condition at " + passInfo[-1] + "\n")
    for y in passInfo[:-2]:
        print(y)

def getCondition(passID, apiCode):
    '''
    Retrieve and Print Mountain Pass Condition for passID from WSDOT.
    Returns tuple of Latitude and Longitude from the Mountain Pass.
    Example: retVal=getCondition(4,code) - conditions print to screen -
    retVal[0]=latitude & retval[1]=longitude

    Arguments:

    apiCode: Your access code.  http://www.wsdot.com/traffic/api/

    passID:  Pass number. https://www.wsdot.com/traffic/passes/

    '''
    passCondition = _getPassCondition(passID , apiCode)
    if "Problem" in passCondition:
        print(passCondition)
    else:
        _printPassCondition(passCondition.passInfo)
        return passCondition.lat, passCondition.lon