# Json, math & file IO, request

# Imports
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout
import json
import math
import os

# Use the requests library to collect weather data from weather api

# weather_api_url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true"


# response = requests.get(weather_api_url)
# status_code = response.status_code


# error handling
# try:
#     # what we want to run and check for errors
#     # call the api and get the response
#     print(f"Response data from weather api: {response.json()}")
#     if status_code == 200:
#         print("Request successful.")
# except json.JSONDecodeError:
#     print("Error decoding JSON response.")
# except HTTPError:
#     print(f"HTTP error occurred: {status_code}")
# except ConnectionError:
#     print("Connection error occurred.")
# except Timeout:
#     print("The request timed out.")
# except ConnectionError:
#     print(f"A connection error occurred: {status_code}")
# else:
#     print("No errors occurred.")
# finally:
#     print("Execution completed.")

# define a weather api function

def get_weather_data(latitude, longitude, past_days=0):
    """
    Get weather data from the weather api for a given latitude and longitude.
    :param latitude: Latitude of the location
    :param longitude: Longitude of the location
    :param past_days: Number of past days to get data for (default is 0)
    :return: Weather data as a dictionary
    """
    try:
        # construct the api url with the given parameters
        weather_api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&past_days={past_days}"
        response = requests.get(weather_api_url)
        response.raise_for_status()  # Raise an error for bad responses
        return str(response.json())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching weather data: {e}")
        return None

# Create a json/txt file and store the weather data into 
def create_file(file_name: str):
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)

    file_path = os.path.join(data_dir, file_name)

    try:
        if os.path.exists(file_path):
            print(f"File already exists: {file_path}")
        else:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write('')
            print(f"Created file: {file_path}")
        return file_path
    except FileNotFoundError:
        print("File not found")

    


def write_or_read_file(action, file_path, content:str):

    if action == 'r':
        with open(file_path, 'r', encoding='utf-8') as file:
                    file.read()
    else:
         with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
                    




if __name__ == "__main__":
    data_path = create_file("examplefile.json")
    data = get_weather_data(52.52, 13.41, 5)
    write_or_read_file('r',data_path,data)





