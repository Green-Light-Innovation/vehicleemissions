from database.engine import DatabaseEngine

class NodeConfig:

    def __init__(self, ID:str, location_id:str, friendly_name:str):

        self.__ID = ID
        # Gen new ID if None is specified
        if ID == None: self.__ID = DatabaseEngine.gen_id()

        self.__location_id = location_id
        self.__friendly_name = friendly_name

    # Getters
    def get_ID(self) -> str: return self.__ID
    def get_location_id(self) -> str: return self.__location_id
    def get_friendly_name(self) -> str: return self.__friendly_name