from mountainpass import getCondition
from weather import getWeather

retdata = getCondition(12,'myCoolKey')
getWeather(retdata[0] , retdata [1], 'SupSkiFun')  ##, hoursFC = -1 ,hoursHR=-1)

