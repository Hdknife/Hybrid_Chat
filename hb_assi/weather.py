import requests


def weather_status(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    # Check if the city is found
    if response.status_code == 404:
        return "Wrong City name"
    # Parse the JSON response
    data = response.json()
    # Extract weather status and temperature in Celsius
    weather_status = data['weather'][0]['description']
    temperature_kelvin = data['main']['temp']
    temperature_celsius = temperature_kelvin - 273.15

    return weather_status, temperature_celsius

