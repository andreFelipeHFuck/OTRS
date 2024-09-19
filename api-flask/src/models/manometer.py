from influxdb_client import Point 
from datetime import datetime

class Manometer():
    def __init__(
            self, 
            manometer_id:int, 
            measurement_name: str,
            location: str,
        ) -> None:
        self._manometer_id = manometer_id
        self._measumerement_name = measurement_name
        self._location = location

    def create_point(self, state: bool, value: float, timestamp=None):
        if timestamp == None:
            timestamp = datetime.now()

        point = (Point(self._measumerement_name) 
                     .tag("manometer_id", self._manometer_id) 
                     .tag("location", self._location) 
                     .field("manometer_state", state) 
                     .field("manometer_value", value)
        )
        
        return point
    
                     
