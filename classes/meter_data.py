"""Class"""
# Import Packages
from datetime import datetime

class MeterEntry:
    """Docstring"""
    def __init__(self, totalcost: float = 0.0, highcost: float = 0.0, lowcost: float = 0.0) -> None:
        """
        Initialize a MeterEntry object with total, high, and low costs.

        Args:
            totalcost (float): The total cost of the reading. Defaults to 0.0.
            highcost (float): The cost during high usage periods. Defaults to 0.0.
            lowcost (float): The cost during low usage periods. Defaults to 0.0.
        """
        self.totalcost = totalcost
        self.highcost = highcost
        self.lowcost = lowcost

    def __str__(self) -> str:
        """
        String representation of the MeterEntry object.

        Returns:
            str: A string showing the total, high, and low costs.
        """
        return (f"MeterEntry(Total Cost: {self.totalcost}, "
                f"High Cost: {self.highcost}, Low Cost: {self.lowcost})")

class MeterData:
    """Docstring"""
    def __init__(self, timestamp: datetime):
        """
        Args:
            timestamp (datetime): The datetime when the meter readings were recorded.
        """
        self.timestamp = timestamp
        self.data: dict[str, MeterEntry] = {}

    def add_reading(self, obis: str, value: MeterEntry) -> None:
        """
        Args:
            obis (str): The OBIS code representing the type of reading (e.g., energy, power).
            value (MeterEntry): The value of the reading to be stored.

        Returns:
            None
        """
        self.data[obis] = value

    def get_reading(self, obis: str) -> MeterEntry:
        """
        Args:
            obis (str): The OBIS code whose reading needs to be retrieved.

        Returns:
            MeterEntry: The value of the reading associated with the OBIS code.
            Returns None if the OBIS code is not found.
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
