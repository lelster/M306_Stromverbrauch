"""Class"""
# Import Packages
from datetime import datetime

class ConsumptionEntry:
    """Docstring"""
    def __init__(self, volume: float, timestamp: datetime):
        self.volume = volume
        self.timestamp = timestamp

class ConsumptionData:
    """Docstring"""
    def __init__(self, document_id: str, timestamp: datetime):
        self.document_id = document_id
        self.timestamp = timestamp
        self.data: list[ConsumptionEntry] = []

    def add_entry(self, item: ConsumptionEntry) -> None:
        """Docstring"""
        self.data.append(item)

    def get_consumption(self, date: datetime) -> ConsumptionEntry:
        """Docstring"""
        for entry in self.data:
            if entry.timestamp == date:
                return entry
        return None
