import requests
import os
import json

from config import config


def check_license_plate(image:bytes) -> str:
    """ Takes image bytes, returns plate number  """
    URL = "https://api.platerecognizer.com/v1/plate-reader/" # API endpoint
    API_KEY = config["ANPR_API_TOKEN"] # Load API key from config file

    # Make request
    response = requests.post(
        url = URL,
        data = dict ( regions = ["gb"] ),
        files = dict( upload = image),
        headers = {"Authorization": f"Token {API_KEY}"}
    )

    data = json.loads(response.text)
    
    # Return None if no results are found
    if not data['results']: return None 

    # Parse the plate number from the JSON response and return
    return data["results"][0]["plate"]

    
    
