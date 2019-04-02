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
    '''Retrieve Mountain Pass Condition for submitted passID from WSDOT

    Arguments:

    apiCode: Your access code.  http://www.wsdot.com/traffic/api/
    passID:  Pass number. https://www.wsdot.com/traffic/passes/

    Returns Latitude and Longitude of Mountain Pass

        1 Blewett Pass US97
        2 Cayuse Pass SR123
        3 Chinook Pass SR410
        5 Crystal to Greenwater SR410
        6 Mt. Baker Hwy SR542
        7 North Cascade Hwy SR20
        8 Satus Pass US97
        9 Sherman Pass SR20
        10 Stevens Pass US2
        11 Snoqualmie Pass I-90
        12 White Pass US12
        13 Manastash Ridge I-82
        14 Loup Loup Pass SR20
        15 Disautel Pass SR 155
        16 Wauconda Pass SR20
        '''
    passCondition = _getPassCondition(passID , apiCode)
    if "Problem" in passCondition:
        print(passCondition)
    else:
        _printPassCondition(passCondition.passInfo)
        return passCondition.lat, passCondition.lon