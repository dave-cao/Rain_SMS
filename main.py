import os

import requests
from twilio.rest import Client

url = "https://api.openweathermap.org/data/2.5/onecall?"
api_key = os.environ.get("OWN_API_KEY")
LAT = 39.338711
LNG = -74.481194
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

bring_umbrella = False
for code in id_list:
    if code < 700:
        bring_umbrella = True


if bring_umbrella:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella!",
        from_="+13465455630",
        to="+15875012008",
    )

    print(message.status)
