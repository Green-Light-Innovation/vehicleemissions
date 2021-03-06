import cv2 as cv
import time
import datetime
import serialnum
import network

import api.anpr
import api.dvla

from database.objects.carlocation import CarLocation
from database.objects.car import Car
from database.objects.nodeconfig import NodeConfig

def run() -> None:

    network.wait_for_connection()

    # Get node
    node = NodeConfig.load_from_database(serialnum.get())
    location = node.get_location()

    cam = cv.VideoCapture(0)

    while True:

        network.wait_for_connection()

        node.check_in()
        node.check_if_active()
        
        if node.is_active():
            time.sleep(1)

            # Capture image from webcam
            ret, image = cam.read()

            # If the software is running on the pi, flip the webcam image upsidown
            # This is done because the camera is mounted upsidown
            if serialnum.get_os() == "linux":
                image = cv.flip(image, 0)
                image = cv.flip(image, 1)


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
                print(f"ERROR: Plate [ {plate} ] could not be found")
                continue

            # Get car data and save to database
            car = Car.load_from_dvla_data(data, location.get_ID())
            car.save_to_database()

            print(f"Car recorded at {datetime.datetime.now()} - PLATE: {car.get_plate()}")
