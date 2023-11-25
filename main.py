# This script checks the weather forecast using the OpenWeatherMap API and sends an SMS alert if rain is predicted.
# Author: Guson Ulysse
# Date: 11/24/2023

import requests
import os
from twilio.rest import Client # Twilio library for sending SMS messages

# OpenWeatherMap Forecast API endpoint
endpoint = "https://api.openweathermap.org/data/2.5/forecast"

# Load sensitive data from environment variables
api_key = os.getenv('OPENWEATHER_API_KEY') # API key for OpenWeatherMap
account_sid = os.getenv('TWILIO_ACCOUNT_SID') # Twilio Account SID
auth_token = os.getenv('TWILIO_AUTH_TOKEN') # Twilio Auth Token

# Phone numbers for SMS alert
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER') # Sender's number registered with Twilio
my_phone_number = os.getenv('MY_PHONE_NUMBER') # Recipient's phone number

# Coordinates for the location to check weather forecast (here, Denver, CO, USA)
lat = 39.738449
lon = -104.984848

# Parameters for the API request
parameters = {
    "lat": lat,
    "lon": lon,
    "appid": api_key,
    "cnt": 4, # Number of timestamps to return in the forecast

}

# Perform the API request to get the weather forecast
data = requests.get(url=endpoint, params=parameters)
data.raise_for_status() # Raise an exception for HTTP errors
weather_data = data.json() # Parse the JSON response

# Check the upcoming weather conditions
will_rain = False
for forecast in weather_data["list"][:4]: # Check the first four time periods
    weather_id = forecast["weather"][0]["id"]
    if weather_id < 700: # Weather codes below 700 indicate some form of precipitation
        will_rain = True

# If rain is forecasted, send an SMS alert
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="Bring an umbrella ☔☔☔", # Message content
        from_=twilio_phone_number,
        to=my_phone_number
    )
    print(message.status) # Print the message status for logging
