import requests
from twilio.rest import Client
import keys

def fetch_weather_forecasts(latitude, longitude, api_key, count=4):
    endpoint = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": api_key,
        "cnt": count
    }
    response = requests.get(url=endpoint, params=params)
    response.raise_for_status()
    return response.json()

def format_forecast_message(weather_data):
    description = []
    time_list = []
    for data_point in weather_data["list"]:
        description.append(data_point["weather"][0]["description"])
        time_list.append(data_point["dt_txt"].split(" ")[1].split(":")[0])
    forecast_message = "\n".join(f"Weather condition: {desc}. Hour: {hour}" for desc, hour in zip(description, time_list))
    return forecast_message

def send_sms(message, from_number, to_number):
    try:
        client = Client(keys.account_sid, keys.auth_token)
        message = client.messages.create(body=message, from_=from_number, to=to_number)
        print(message.body)
    except Exception as e:
        print(f"Error sending SMS: {e}")

def main():
    latitude = 51.484170
    longitude = -3.181982 
    api_key = "cce3dc52c5113de0063bae3adb768543"
    from_number = keys.twilio_number
    to_number = keys.target_number

    try:
        weather_data = fetch_weather_forecasts(latitude, longitude, api_key)
        forecast_message = format_forecast_message(weather_data)
        if forecast_message:
            send_sms(forecast_message, from_number, to_number)
    except requests.RequestException as req_err:
        print(f"Request Error: {req_err}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()