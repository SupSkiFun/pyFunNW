# from weather import getWeather
# from tide import getTide
# from mountainpass import getCondition
from ferrystatus import getSchedule

code = '3f910268-4452-47f1-9f03-3b31e48af62d'

getSchedule(3,code)
getSchedule(7,code)


# abc = getCondition(7,'myCoolKey')
# print(abc)
# print(abc[0])

#retdata = getCondition(12,'myCoolKey')
#getWeather(retdata[0] , retdata [1], 'SupSkiFun')  ##, hoursFC = -1 ,hoursHR=-1)
#getTide(9445882)
#getTide(1843657)
#getTide(9445719 , banner=False)
