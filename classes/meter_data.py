"""Class"""
# Import Packages
from datetime import datetime

class MeterData:
    """Docstring"""
    def __init__(self, timestamp: datetime):
        self.timestamp = timestamp
        self.data: dict[str, float] = {}

    def add_reading(self, obis: str, value: float) -> None:
        """Docstring"""
        self.data[obis] = value #round(value, 3)

    def get_reading(self, obis: str) -> float:
        """Docstring"""
        return self.data.get(obis)

    def __str__(self) -> str:
        """String representation of the MeterData object"""
        readings_str = ", ".join(f"{obis}: {value}" for obis, value in self.data.items())
        return f"MeterData(Timestamp: {self.timestamp}, Readings: {{{readings_str}}})"
