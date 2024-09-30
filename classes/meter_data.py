"""Class"""
# Import Packages
from datetime import datetime

class MeterData:
    """Docstring"""
    def __init__(self, meter_id: str, timestamp: datetime):
        self.meter_id = meter_id
        self.timestamp = timestamp
        self.data: dict[str, float] = {}

    def add_reading(self, obis: str, value: float) -> None:
        """Docstring"""
        self.data[obis] = value

    def get_reading(self, obis: str) -> float:
        """Docstring"""
        return self.data.get(obis)
