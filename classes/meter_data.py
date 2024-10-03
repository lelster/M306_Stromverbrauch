"""Class"""
# Import Packages
from datetime import datetime

class MeterData:
    """Docstring"""
    def __init__(self, timestamp: datetime):
        """
        Args:
            timestamp (datetime): The datetime when the meter readings were recorded.
        """
        self.timestamp = timestamp
        self.data: dict[str, float] = {}

    def add_reading(self, obis: str, value: float) -> None:
        """
        Args:
            obis (str): The OBIS code representing the type of reading (e.g., energy, power).
            value (float): The value of the reading to be stored.

        Returns:
            None
        """
        self.data[obis] = value #round(value, 3)

    def get_reading(self, obis: str) -> float:
        """
        Args:
            obis (str): The OBIS code whose reading needs to be retrieved.

        Returns:
            float: The value of the reading associated with the OBIS code. Returns None if the OBIS code is not found.
        """
        return self.data.get(obis)

    def __str__(self) -> str:
        """
        String representation of the MeterData object.
        
        Returns:
            str: A string showing the timestamp and the associated meter readings.
        """
        readings_str = ", ".join(f"{obis}: {value}" for obis, value in self.data.items())
        return f"MeterData(Timestamp: {self.timestamp}, Readings: {{{readings_str}}})"
