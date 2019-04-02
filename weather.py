import requests
import datetime
import collections

def _trimToFour(s):
    """Convert input to String and Trim input to 4 decimal places
       Using only 4 decimal places avoids 301 redirect delay"""
    s = str(s)
    try:
        i = s.index(".")
    except:
        return s
    else:
        return (s[:(i+5)])

def _getWeatherEndPoint(latitude,longitude,heads):
    '''Retrieve Weather EndPoints and Location from NOAA

    Arguments:
    latitude:  latitude needed - string or float ok
    longitude:  longitude needed - string or float ok
    heads:  header information
    '''
    # Use only 4 decimal places to avoid redirect delay: trimToFour.  Use this URL to get ultimate URL.
    urlEP = 'https://api.weather.gov/points/'+_trimToFour(latitude) +','+ _trimToFour(longitude)
    tupEP = collections.namedtuple('tupEP', ['forecast', 'hourly', 'city', 'state'])
    try:
        wret1 = requests.get(urlEP , headers = heads)
        wret1.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return "Problem Accessing the below URL for weather endpoint:\n" + str(err)
    else:
        wjrdA = wret1.json()
        dataEP = tupEP(wjrdA['properties']['forecast'] ,
            wjrdA['properties']['forecastHourly'] ,
            wjrdA['properties']['relativeLocation']['properties']['city'] ,
            wjrdA['properties']['relativeLocation']['properties']['state'] ,
        )
        return dataEP

def _getWeatherForecast(urlFC, heads, hoursFC):
    '''Retrieve Weather Forecast from NOAA'''
    try:
        wret2 = requests.get(urlFC , headers = heads)
        wret2.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return "Problem Accessing the below URL for weather conditions:\n" + str(err)
    else:
        wjrdB = wret2.json()
        tnow = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(days=-1, seconds=61200)))
        tfut = tnow + datetime.timedelta(hours=hoursFC)
        wtup = []
        for x in wjrdB['properties']['periods']:
            tstr = datetime.datetime.fromisoformat(x['startTime'])
            if tstr <= tfut:
                wtup.append([x['name'], x['detailedForecast'],])
            else:
                break
        return wtup

def _getWeatherHourly(urlHR , heads):
    '''Retrieve Weather Forecast by Hour from NOAA'''
    try:
        wret3 = requests.get(urlHR , headers = heads)
        wret3.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return "Problem Accessing the below URL for weather conditions:\n" + str(err)
    else:
        wjrdC = wret3.json()
        return wjrdC

def _printWeatherHourly(wjrdC , hoursHR):
    '''Print Hourly Weather Forecast from NOAA'''
    for x in wjrdC['properties']['periods'][:(hoursHR + 1)]:
        dt = datetime.datetime.fromisoformat(x['startTime']).strftime('%d-%b-%Y %H:%M')
        tf = str(x['temperature']) + x['temperatureUnit']
        print(dt,tf,x['shortForecast'],x['windSpeed'],x['windDirection'])

def _printWeatherForecast(weather ,city , state):
    '''Print Weather Forecast from NOAA'''
    print("\n\n\t" + city + ", " + state + " Forecast\n")
    for z in weather:
        print("   ".join([str(s) for s in list(z)]))


def getWeather(latitude, longitude, userAgent, hoursFC = 48, hoursHR = 12):
    '''Retrieve Weather from submitted Latitude and Longitude

    Arguments:

    latitude:  Latitude - string or float ok
    longitude: Longitude - string or float ok
    userAgent: Company or Application or Your Name
    hoursFC:   Hours of Weather Forecast by periods (e.g. morning, evening).
        -1 for no results.
    hoursHR:   Hours of Weather Forecast by the hour.
        -1 for no results.
    '''

    heads ={
    'User-Agent' : userAgent,
    'Accept' : 'application/geo+json',
    }
    EPdata = _getWeatherEndPoint(latitude , longitude, heads)
    if "Problem" in EPdata:
        print(EPdata)
        print("\n" + "Terminating due to lack of EndPoint Data")
        raise SystemExit()
    else:
        WFdata = _getWeatherForecast(EPdata.forecast , heads , hoursFC)

    if "Problem" in WFdata:
        print(WFdata)
        print("\n")
    else:
        _printWeatherForecast(WFdata , EPdata.city , EPdata.state)

    WHdata = _getWeatherHourly(EPdata.hourly , heads)
    if "Problem" in WHdata:
        print(WHdata)
        print("\n")
    else:
        _printWeatherHourly(WHdata, hoursHR)


