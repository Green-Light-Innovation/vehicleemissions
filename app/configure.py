import app.main
from database.objects.carlocation import CarLocation

""" 
First step of the application
The ANPR system needs to be configured with the correct location
"""

def run() -> None:
    """ Run the configure script """
    command_line()



def command_line() -> None:
    """ Configure the app using command line """
    
    location_name = str(input("Please enter location name: "))
    
    print("\nPlease enter location co-ordinates...")
    lat = float(input("\tLatitude:\t"))
    lon = float(input("\tLongitude:\t"))

    print("\nPlease enter ther direction that the camera is facing")
    print("Valid options: N, NE, E, SE, S, SW, W, NW")
    facing = str(input("> "))

    valid = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    while facing not in valid:
        print("\nERROR: Inavlid Choice\n")
        print("\nPlease enter ther direction that the camera is facing")
        print("Valid options: N, NE, E, SE, S, SW, W, NW")
        facing = str(input("> "))

    location = CarLocation(None, lat, lon, location_name, facing)
    location.save_to_database()
 
    app.main.run(location)


def gui() -> None:
    """ Configure the app using a GUI """