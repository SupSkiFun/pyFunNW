from weather import getWeather
from tide import getTide
from mountainpass import getCondition

abc = getCondition(7,'myCoolKey')
print(abc)
print(abc[0])

#retdata = getCondition(12,'myCoolKey')
#getWeather(retdata[0] , retdata [1], 'SupSkiFun')  ##, hoursFC = -1 ,hoursHR=-1)
#getTide(9445882)
#getTide(1843657)
#getTide(9445719 , banner=False)
