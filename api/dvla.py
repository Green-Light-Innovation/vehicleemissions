import requests
import os
import dotenv
import json

from config import config

def search_plate_number(plate_number:str) -> dict:
    """ Returns dictionary of car information """

    URL = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"
    API_KEY = config["DVLA_API_TOKEN"] # Get DVLA API key from config file

    response = requests.post(
        url = URL,
        data = json.dumps(dict(registrationNumber = plate_number)),
        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }
    )

    data = json.loads(response.text)
    
    if "errors" in data: return None # Return None value if there was an error
    
    return data