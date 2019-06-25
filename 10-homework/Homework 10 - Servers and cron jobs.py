#!/usr/bin/env python
# coding: utf-8

# ## Using APIs/Data Structures
# Using the Dark Sky Forecast API at https://developer.forecast.io/, generate a sentence that describes the weather that day.
# 
# Right now it is TEMPERATURE degrees out and SUMMARY. Today will be TEMP_FEELING with a high of HIGH_TEMP and a low of LOW_TEMP. RAIN_WARNING.
# 
# - TEMPERATURE is the current temperature
# - SUMMARY is what it currently looks like (partly cloudy, etc - it's "summary" in the dictionary). Lowercase, please.
# - TEMP_FEELING is whether it will be hot, warm, cold, or moderate. You will probably use HIGH_TEMP and your own thoughts and feelings to determine this.
# - HIGH_TEMP is the high temperature for the day.
# - LOW_TEMP is the low temperature for the day.
# - RAIN_WARNING is something like "bring your umbrella!" if it is going to rain at some point during the day.
# 
# You can take a look at the documentation, but "current" contains the current conditions and the first element of "daily" is for the current day. But you knew that, right?!
# 
# Feel free to steal your old code! I bet that trying to read it will make you depressed and teaches you the value of naming variables.
# 
# Once you've accomplished that part, use Mailgun to send yourself an email every morning at 8AM telling you the sentence. The subject line of the email should be something like "8AM Weather forecast: January 1, 1970."
# 
# Dates are obtained by doing something like this, using http://strftime.org/ as a reference:
# 
# import datetime
# right_now = datetime.datetime.now()
# date_string = right_now.strftime("%Y-%M")
# 
# BONUS: List the forecasted temperatures as the day goes on.
# 
# BONUS: Set the timezone on your server so emails go out at the right time.

# In[1]:


#from dotenv import load_dotenv
#load_dotenv()
from dotenv import load_dotenv
load_dotenv(".env")
import os

API_KEY = os.getenv("DARKSKY_API_KEY")
import requests


# In[2]:


response = requests.get(f'https://api.darksky.net/forecast/{API_KEY}/40.7829, -73.9654') #NYC
weather = response.json()
weather.keys()


# In[3]:


current = weather['currently']
#print(current)
current['temperature']


# In[4]:


weather['daily']['data']


# In[5]:


current['apparentTemperature']


# In[14]:


subject = "Your Daily Mail Forecast"
daily = weather['daily']['data']
temp_now = current['apparentTemperature']
from datetime import datetime

dates = []
for data in daily:
    date = datetime.utcfromtimestamp(data['time']).strftime('%Y-%m-%d %H:%M:%S')
    dates.append(data['time'])
    
    if min(dates) == data['time']:
        summary = data['summary']
        
        if data['apparentTemperatureHigh'] > 75:
            temp_feeling = "hot"
        elif data['apparentTemperatureHigh'] < 60:
            temp_feeling = "cold"
        else:
            temp_feeling = "warm"
            
        high = data['temperatureHigh']
        low = data['temperatureLow']
        
        if "rain" in data['icon']:
            rain = "Bring your umbrella! It may rain at some point during the day"
        else:
            rain = "It's not supposed to rain today"
        text = f'Right now it is {temp_now} degrees out and {summary.lower()} Today will be {temp_feeling} with a high of {high} and a low of {low}. {rain}.'   
        
        


# In[19]:


response = requests.post(
        "https://api.mailgun.net/v3/sandbox1ded04a1418f4a5cbfa3a5a9ff1975cc.mailgun.org/messages",
        auth=("api", "#####MY-APIKEY-WENT-HERE####"),
        data={"from": "Excited User <mailgun@sandbox1ded04a1418f4a5cbfa3a5a9ff1975cc.mailgun.org>",
              "to": ["aw3230@columbia.edu", "aodaywilliams@gmail.com"],
              "subject": subject,
              "text": text}) 
print(response.text)


# In[ ]:





# In[ ]:




