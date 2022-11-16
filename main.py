import os

import requests
from twilio.rest import Client

url = "https://api.openweathermap.org/data/2.5/onecall?"
api_key = os.environ.get("OWN_API_KEY")
LAT = 53.544388
LNG = -113.490929
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

weather_params = {
    "lat": LAT,
    "lon": LNG,
    "appid": api_key,
    "exclude": "current,minutely,daily",
}

connection = requests.get(url, params=weather_params)
connection.raise_for_status()
data = connection.json()

hourly = data["hourly"]

# loop through all hourly weather data
twelve_hour = hourly[:12]
id_list = [condition["id"] for hour in twelve_hour for condition in hour["weather"]]

# 6xx = Snow
# 5xx = Rain
# 3xx = Drizzle
# 2xx = Thunderstorm

snow = False
rain = False
drizzle = False
thunderstorm = False
for code in id_list:
    if 600 <= code < 700:
        snow = True
    elif 500 <= code < 600:
        rain = True
    elif 300 <= code < 400:
        drizzle = True
    elif 200 <= code < 300:
        thunderstorm = True


if snow:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="Forecast says it's going to snow today. Remember to dress warm when going out!",
        from_="+13465455630",
        to="+15875012008",
    )
    print(message.status)
elif rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="Forecast says it's going to rain today. Remember to bring an umbrella!",
        from_="+13465455630",
        to="+15875012008",
    )
    print(message.status)
elif drizzle:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="Forecast says it's going to slightly drizzle today. Remember to bring an umbrella!",
        from_="+13465455630",
        to="+15875012008",
    )
    print(message.status)
elif thunderstorm:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="There's going to be a thunderstorm today. Be careful out there!",
        from_="+13465455630",
        to="+15875012008",
    )

    print(message.status)
else:
    print("No current weather condition to report")
