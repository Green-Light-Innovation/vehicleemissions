import cv2 as cv
import time
import datetime
import serialnum

import api.anpr
import api.dvla

from database.objects.carlocation import CarLocation
from database.objects.car import Car
from database.objects.nodeconfig import NodeConfig

def run() -> None:

    # Get node
    node = NodeConfig.load_from_database(serialnum.get())
    location = node.get_location()

    cam = cv.VideoCapture(0)

    while True:
        
        time.sleep(1)

        # Capture image from webcam
        ret, image = cam.read()
        success, image_buffer = cv.imencode('.jpg', image)
        image_bytes = image_buffer.tobytes()

        # Upload image to anpr API
        plate = api.anpr.check_license_plate(image_bytes)
        # If no plate was identified go back to the start of the loop
        if not plate:
            print("ERROR: Plate could not be recognized")
            continue 

        # Take license plate and give it to DVLA API
        data = api.dvla.search_plate_number(plate)
        # If no data was found go back to the start of the loop
        if not data: 
            print("ERROR: Plate could not be found")
            continue

        # Get car data and save to database
        car = Car.load_from_dvla_data(data, location.get_ID())
        car.save_to_database()

        print(f"Car recorded at {datetime.datetime.now()} - PLATE: {car.get_plate()}")
