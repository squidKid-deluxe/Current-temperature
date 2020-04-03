"""
A script that gets the current temperature, among
other things.
"""

import json
from time import sleep
import requests as requ
from colorize import bold
from banner_3d import convert


def get_info():
    """
    Webscrape data from darksky.net.
    """
    # Get data.
    ret = requ.get("https://darksky.net/forecast/42.0631,-75.4224/us12/en")# (30, -90) = New Orleans
    # Find the current stats among the data.
    ret = ret.text.split("current")[10]
    # Make the data json.loads-able.
    ret = ret.strip("ly = ").split("},")
    final_ret = ret[0]
    final_ret += "}"
    # Turn the data into a dictionary.
    ret = json.loads(final_ret)
    # Return the data.
    return ret

def pprint(data, final_summary):
    """
    Print out all the data in a user-friendly way.
    """
    # Clear the screen
    print("\033c")

    # Test for what color the 'temperature' tag should be.
    temp_color = ""
    if data["temperature"] > 50:
        temp_color = "red"
    else:
        temp_color = "blue"

    # Test for what color the 'feels like' tag should be.
    feels_color = ""
    if data["apparentTemperature"] > 50:
        feels_color = "red"
    else:
        feels_color = "blue"

    # Test for what color the 'humidity' tag should be.
    humid_color = ""
    if data["humidity"] < 0.50:
        humid_color = "yellow"
    else:
        humid_color = "blue"

    # Test for what unicode symbol for the 'Summary' tag should be.
    weather_icon = ""
    if ("Cloud" in data["summary"]) or ("Overcast" in data["summary"]):
        weather_icon = u"\u2601"
    elif ("Sun" in data["summary"]) or ("Clear" in data["summary"]):
        weather_icon = u"\u2600"
    elif data["precipProbability"] > 0.5:
        weather_icon = u"\u26C6"
    elif "Snow" in data["summary"]:
        weather_icon = u"\u2603"

    # Banner_3d title.
    convert("Weather status:", "blue", "green")

    # Print the temperature in the specified color.
    print(bold(temp_color, ("\n\nTemperature: " + str(data["temperature"]))))
    # Print the feels like temperature in the specified color.
    print(bold(feels_color, ("Feels like: " + str(data["apparentTemperature"]))))
    # Print the humidity in the specified color.
    print(bold(humid_color, ("Humidity:  " + str(data["humidity"] * 100) + "%")))
    # Print the probibility of precipitation in green.
    print(
        bold(
            "green", ("Probibility of precipitation: " + str(data["precipProbability"]))
        )
    )
    # Print the intensity of precipitation in green.
    print(
        bold("green", ("Intensity of precipitation: " + str(data["precipIntensity"])))
    )
    # Print the dew point in green.
    print(bold("green", ("Dew point: " + str(data["dewPoint"]))))
    # Print the summary in green, along with white unicode symbols describing the weather.
    print(bold("green", ("Summary: " + data["summary"])), " ", weather_icon * 5)
    # Print the wind gust speed in green.
    print(
        bold("green", ("Wind gust speed: " + str(data["windGust"]) + " miles per hour"))
    )
    # Print the wind speed in green.
    print(bold("green", ("Wind speed: " + str(data["windSpeed"]) + " miles per hour")))
    # Print the miles of visibility in green.
    print(bold("green", ("Visibility: " + str(data["visibility"]) + " miles")))
    # Print the appropriate face(smiley/frownie/crying).
    print(bold("green", "\nMy summary: "), end="")
    print(final_summary)


def main():
    """
    Fire up the rest of the script and initalize the 'final_summary' faces.
    """

    # Define the hair for all the figures.
    hair = "\n\tX*X*X*X*X*X*X\n"

    # Define the sad face.
    sad_no = """\t#############
        #           #
        #   0   0   #
        #     v     #
        #    ___    #
        #   /   \\   #
        #           #
        #############
    """

    # Add the hair to the sad face.
    sad = bold("yellow", hair)
    sad += bold("white", sad_no)

    # Define the happy face.
    happy_no = """\t#############
        #           #
        #   0   0   #
        #     v     #
        #           #
        #   \\___/   #
        #           #
        #############
    """

    # Add hair to the happy face.
    happy = bold("yellow", hair)
    happy += bold("white", happy_no)

    # Define the crying face.
    not_happy_no = """\t#############
        #           #
        #   0   0   #
        #  '  v     #
        #    ___    #
        #   /   \\   #
        #           #
        #############
    """

    # Add hair to the crying face.
    not_happy = bold("yellow", hair)
    not_happy += bold("white", not_happy_no)

    while True:
        # Get the data.
        info = get_info()

        # Choose the the appropriate face(smiley/frownie/crying).
        final_summary = ''
        if ("Cloud" in info["summary"]) or ("Overcast" in info["summary"]):
            final_summary = sad
        if ("Sun" in info["summary"]) or ("Clear" in info["summary"]):
            final_summary = happy
        if (info["precipProbability"] > 0.5) or ("Snow" in info["summary"]):
            final_summary = not_happy
        if "Rain" in info["summary"]:
            final_summary = not_happy
        # Print the info.
        pprint(info, final_summary)
        # Sleep before beginning again.
        sleep(60)


# Start program
if __name__ == "__main__":
    main()
