"""
Application to get the airport weather status for major U.S. airports,
including known delays and weather data from NOAA.

The JSON data comes from http://weather.gov and the NOAA's National Weather
Service vis the FAA's API(instructions for the API can be found at
http://services.faa.gov/).
"""

__author__ = 'Ken W. Alger'
__version__ = '1.0.0'
__email__ = "kenalger@comcast.net"


import argparse
import requests


parser = argparse.ArgumentParser(description='Get current weather data from '
                                             'U.S. airports.')
parser.add_argument('-a',
                    '--airport',
                    required=True,
                    type=str,
                    help='IATA code for U.S. airport'
                    )
airport_code = parser.parse_args()


def print_message(airport,
                  name,
                  delay,
                  updated,
                  weather,
                  temp,
                  wind,
                  visibility,
                  delay_reason,
                  delay_time):
    if delay == 'true':
        message = "\n \nAs of {}, {} ({}) is currently delayed due to {}. \n" \
                  "The average delay time is {}. \n" \
                  "There are {} conditions and {} miles of visibility. \n" \
                  "The temperature is {} with wind from the {}. \n \n".format(
                   updated, name, airport.upper(), delay_reason, delay_time,
                   weather, visibility, temp, wind)
        print(message)
    else:
        message = "\n \nAs of {}, {} ({}) is not currently delayed. \n" \
                  "There are {} conditions and {} miles of visibility. \n" \
                  "The temperature is {} with wind from the {}. \n \n".format(
                   updated, name, airport.upper(), weather, visibility, temp,
                   wind)
        print(message)


def get_airport_info(airport):

    try:
        data = requests.get(
            "http://services.faa.gov/airport/status/" +
            airport +
            "?format=JSON"
        )
        if data.status_code == 200:
            output = data.json()

            print_message(output['IATA'],
                          output['name'],
                          output['delay'],
                          output['weather']['meta']['updated'],
                          output['weather']['weather'],
                          output['weather']['temp'],
                          output['weather']['wind'],
                          output['weather']['visibility'],
                          output['status']['reason'],
                          output['status']['avgDelay']
                          )
        else:
            print("There was an error in getting information about {}"
                  .format(airport))
    except requests.exceptions.RequestException as error:
        print("Error in getting information for {}. {}".format(airport, error))


if __name__ == '__main__':
    get_airport_info(airport_code.airport)
