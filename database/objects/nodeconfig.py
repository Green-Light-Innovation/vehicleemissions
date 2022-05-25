import serialnum
import time
from datetime import datetime
from database.engine import DatabaseEngine
from database.objects.carlocation import CarLocation

class NodeConfig:

    @staticmethod
    def load_from_database(ID:str) -> object:
        """ Load NodeConfig object from the database """
        
        query = "SELECT * FROM NodeConfig WHERE `ID` = %s"
        DatabaseEngine.connect()
        DatabaseEngine.cursor.execute(query, (ID,))
        data = DatabaseEngine.cursor.fetchone()
        DatabaseEngine.disconnect

        if not data:
            # Create new node object and put it in the database
            return NodeConfig.create_new_node()

        return NodeConfig(*data)

    @staticmethod
    def create_new_node() -> object:
        sernum = serialnum.get() # Get the serial number of the device

        # gen a 'friendly name for the node'
        name = f"NEW_NODE_{int(time.mktime(datetime.now().timetuple()))}"
        
        # Create a new node object
        node = NodeConfig(
            sernum,
            "",
            name,
            1
        )

        # Save node to the database
        node.save_to_database()

        return node


    def __init__(self, ID:str, location_id:str, friendly_name:str, active:int):

        self.__ID = ID
        self.__location_id = location_id
        self.__friendly_name = friendly_name
        self.__active = bool(active)

    # Getters
    def get_ID(self) -> str: return self.__ID
    def get_location_id(self) -> str: return self.__location_id
    def get_friendly_name(self) -> str: return self.__friendly_name
    def is_active(self) -> bool: return self.__active

    def __update_location_id(self) -> str:
        """ Update location_id from the database """

        query = "SELECT `location_id` FROM NodeConfig WHERE `ID` = %s;"
        DatabaseEngine.connect()
        DatabaseEngine.cursor.execute(query, (self.__ID,))
        data = DatabaseEngine.cursor.fetchone()
        DatabaseEngine.disconnect()

        return data[0]

    def save_to_database(self) -> None:
        """ Save object to the database """

        query = """
        INSERT INTO NodeConfig (`ID`, `location_id`, `friendly_name`) 
        VALUES (%s, %s, %s);
        """

        DatabaseEngine.connect()
        DatabaseEngine.cursor.execute(query, (self.__ID, self.__location_id, self.__friendly_name))
        DatabaseEngine.commit()
        DatabaseEngine.disconnect()


    def get_location(self) -> CarLocation:
        """ Gets car location object, method waits until it can find it """

        # get loction object from database
        location = CarLocation.load_from_database(self.__location_id)
        
        # If no location is found, constantly check database for updated location
        while not location:

            print("Waiting for location")
            # Check for updated location id
            self.__location_id = self.__update_location_id()

            # Check for location
            location = CarLocation.load_from_database(self.__location_id)

            time.sleep(5)

        return location

    def check_if_active(self) -> None:
        """ Check to see if the node is active """
        
        query = "SELECT active FROM NodeConfig WHERE ID = %s;"
        DatabaseEngine.connect()
        DatabaseEngine.cursor.execute(query, (self.__ID,))
        data = DatabaseEngine.cursor.fetchone()[0]
        DatabaseEngine.disconnect()

        self.__active = bool(int(data))