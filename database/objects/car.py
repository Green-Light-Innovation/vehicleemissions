from datetime import datetime

from database.engine import DatabaseEngine
from database.objects.carlocation import CarLocation

class Car:

    @staticmethod
    def load_from_database(plate:str) -> object:
        query = "SELECT * FROM Cars WHERE plate = %s"
        
        DatabaseEngine.connect()
        DatabaseEngine.cursor.execute(query, (plate,))
        data = DatabaseEngine.cursor.fetchone()
        DatabaseEngine.disconnect()

        if not data: return # Return None if no car is found
        
        return Car(*data)

    @staticmethod
    def load_from_dvla_data(data:dict, locationID:str) -> object:
        """ Create a car object using DVLA API data """

        return Car(
            None, # ID
            data["registrationNumber"], # number plate
            None, # recorded datetime
            data["make"], # car make
            data["yearOfManufacture"], # manufacture year
            data["co2Emissions"], # emission levels
            data["fuelType"], # fuel type
            locationID # location ID
        )

    @staticmethod
    def load_all() -> list:pass # TODO Implement this

    @classmethod
    def __get_unix_time(cls) -> int:
        """ Get current datetime in unix time format"""
        return round(datetime.timestamp(datetime.now()))

    def __init__(self, ID:str, plate:str, recorded_datetime:int, make:str, manufacture_year:int, emissions:float, fuel_type:str, car_location:str) -> object:
        self.__ID = ID
        if not ID: self.__ID = DatabaseEngine.gen_id() # If no ID is specified, gen a new one

        self.__plate = plate
        
        # If datetime is specified as None, get current datetime in unix format
        self.__recorded_datetime = recorded_datetime
        if not recorded_datetime: self.__recorded_datetime = Car.__get_unix_time()
        
        self.__make = make
        self.__manufacture_year = manufacture_year
        self.__emissions = emissions
        self.__fuel_type = fuel_type
        self.__car_location = CarLocation.load_from_database(car_location) # TODO CHANGE TO CAR LOCATION OBJECT

    # Getters
    def get_ID(self) -> str: return self.__ID
    def get_plate(self) -> str: return self.__plate
    def get_recorded_datetime(self) -> int: return self.__recorded_datetime
    def get_make(self) -> str: return self.__make
    def get_manufacture_year(self) -> int: return self.__manufacture_year
    def get_emissions(self) -> float: return self.__emissions
    def get_fuel_type(self) -> str: return self.__fuel_type
    def get_car_location(self) -> CarLocation: return self.__car_location

    def is_recorded(self) -> bool:
        """ Checks if the plate has been recorded previously in the data base within the last 5 minutes """
        car = Car.load_from_database(self.__plate)
        
        if not car: return False # if no record was found, return false

        # check if previously recorded car has been recorded at least 5 minutes
        # before being recorded again
        if car.get_recorded_datetime() + (5*60) < self.__recorded_datetime:
            return False

        return True

    
    def save_to_database(self) -> None:
        """ Save the object's data to the database """

        if self.is_recorded(): return # Dont record car is already recorded

        # SQL query to insert new record into Cars table
        query = """
        INSERT INTO Cars (ID, plate, recorded_datetime, make, manufacture_year, emissions, fuel_type, car_location)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """

        DatabaseEngine.connect() # Connect to the database
        
        # Execute the SQL query with given parameters
        DatabaseEngine.cursor.execute(query, (
            self.__ID,
            self.__plate,
            self.__recorded_datetime,
            self.__make,
            self.__manufacture_year,
            self.__emissions,
            self.__fuel_type,
            self.__car_location.get_ID()
        ))

        DatabaseEngine.commit() # Commit changes made to the table
        DatabaseEngine.disconnect() # Disconnect from the database

    def __repr__(self) -> str:
        return f"<Car - {self.__plate}>"

    

