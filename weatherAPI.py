# Get historical weather data from wunderground API

from datetime import date, datetime
from dateutil.rrule import rrule, DAILY
import requests
import pandas as pd
from collections import OrderedDict

url_start = 'http://api.wunderground.com/api/19959fbd0ad1e9cf/history_'
url_end = '/q/NY/New_York.json'

date_start = date(2017,1,1)
date_end = date(2017,12,31)

weather = {'Date':pd.Series(['']), 'Maxtemp (Celsius)':pd.Series(['']), 'Mintemp (Celsius)': pd.Series(['']),
           'Meantemp (Celsius)':pd.Series(['']), 'Rain':pd.Series(['']), 'Fog':pd.Series(['']), 'Snow': pd.Series(['']),
           'Hail': pd.Series(['']), 'Thunder':pd.Series(['']), 'Tornado':pd.Series(['']), 'SnowFall (meter)': pd.Series(['']),
           'MaxWind (km/h)':pd.Series(['']), 'MinWind (km/h)':pd.Series(['']), 'MeanWind (km/h)': pd.Series(['']),
           'MaxVisibility (meter)': pd.Series(['']), 'MinVisibility (meter)':pd.Series(['']), 'MeanVisibility (meter)': pd.Series([''])}
weather_dataframe = pd.DataFrame(weather)

for dt in rrule(DAILY, dtstart=date_start, until=date_end):
    gooddate = dt.strftime("%Y%m%d")
    url = url_start+str(gooddate)+url_end
    json_data = requests.get(url).json()
    for items in json_data['history']['dailysummary']:
        daily_record = {'Date':dt.strftime("%m/%d/%Y"), 'Maxtemp (Celsius)': items['maxtempm'], 'Mintemp (Celsius)': items['mintempm'],
                        'Meantemp (Celsius)':items['meantempm'], 'Rain': items['rain'], 'Fog': items['fog'], 'Snow': items['snow'],
                        'Hail': items['hail'], 'Thunder': items['thunder'], 'Tornado': items['tornado'], 'SnowFall (meter)': items['snowfallm'],
                        'MaxWind (km/h)': items['maxwspdm'], 'MinWind (km/h)': items['minwspdm'], 'MeanWind (km/h)':items['meanwindspdm'],
                        'MaxVisibility (meter)':items['maxvism'], 'MinVisibility (meter)': items['minvism'], 'MeanVisibility (meter)': items['meanvism']}
        weather_dataframe = weather_dataframe.append(daily_record, ignore_index=True)

weather_dataframe.to_csv('Weather2017.csv', columns=['Date','Maxtemp (Celsius)','Mintemp (Celsius)','Meantemp (Celsius)','Rain', 'Fog','Snow',
                                                            'Hail','Thunder','Tornado','SnowFall (meter)','MaxWind (km/h)','MinWind (km/h)','MeanWind (km/h)',
                                                            'MaxVisibility (meter)','MinVisibility (meter)','MeanVisibility (meter)'])
