import config
import requests
import time

def test() -> bool:
    """ Test connection by get requesting a server """
    try: requests.get(config.config["CONNECTION_TEST_SERVER"])
    except: return False
    return True
    

def wait_for_connection() -> None:
    """ Loop until conneciton is made"""
    while not test():
        print("ERROR: Node not connected to network")
        time.sleep(1)