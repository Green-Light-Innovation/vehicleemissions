from database.engine import DatabaseEngine

class CarLocation:

    @staticmethod
    def load_from_database(ID:int) -> object:
        """ Create a new CarLocation object using data loaded from the database """
        
        query = "SELECT * FROM CarLocations WHERE ID = ?;" # SQL query executed on the database

        DatabaseEngine.connect() # Connect to the database

        # Fetch data from the database using the ID parameter
        # Only one item should be returned so the fetchone() function is used
        data = DatabaseEngine.cursor.execute(query, (ID,)).fetchone()
        DatabaseEngine.disconnect() # Disconnect from the database

        if not data: return None # If no data could be found, return None object

        return CarLocation(*data) # Return the data

    def __init__(self, ID:str, lat:float, lon:float, location_name:str, facing:str) -> object:
        self.__ID = ID
        if not ID: self.__ID = DatabaseEngine.gen_id() # If no ID is specified, gen a new one
        
        self.__lat = lat
        self.__lon = lon
        self.__location_name = location_name
        self.__facing = facing

    # Getters
    def get_ID(self) -> str: return self.__ID
    def get_latitude(self) -> float: return self.__lat
    def get_longitude(self) -> float: return self.__lon
    def get_location_name(self) -> str: return self.__location_name
    def get_facing(self) -> str: return self.__facing

    def save_to_database(self) -> None:
        """ Save the object's data to the database """

        # SQL query to insert new record into CarLocations table
        query = """
        INSERT INTO CarLocations (ID, lat, lon, location_name, facing)
        VALUES (?, ?, ?, ?, ?);
        """

        DatabaseEngine.connect() # Connect to the database
        
        # Execute SQL query with parameters
        DatabaseEngine.cursor.execute(query, (
            self.__ID,
            self.__lat,
            self.__lon,
            self.__location_name,
            self.__facing
        ))

        DatabaseEngine.commit() # Commit the changes made
        DatabaseEngine.disconnect() # Disconnect from the database

    def __repr__(self) -> str:
        return f"<CarLocation - Lat: {self.__lat} Lon: {self.__lon}>"