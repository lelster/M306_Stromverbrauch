# Import Packages
from datetime import datetime, timedelta

class ConsumptionEntry:
    """Represents a single consumption entry with volume and timestamp."""
    def __init__(self, volume: float, timestamp: datetime):
        self.volume = volume
        self.timestamp = timestamp

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'volume': self.volume,
            'timestamp': self.timestamp.isoformat()
        }

    def __str__(self):
        return f"ConsumptionEntry(Volume: {self.volume}, Timestamp: {self.timestamp})"

class ConsumptionData:
    """Contains consumption data including document ID and a list of consumption entries."""
    def __init__(self, document_id: str, start_date: datetime, end_date: datetime):
        self.document_id = document_id
        self.start_date = start_date
        self.end_date = end_date
        self.data: list[ConsumptionEntry] = []

    def add_entry(self, item: ConsumptionEntry) -> None:
        """Adds a consumption entry to the data list."""
        self.data.append(item)

    def get_consumption(self, date: datetime) -> ConsumptionEntry:
        """Retrieves a consumption entry by date."""
        for entry in self.data:
            if entry.timestamp == date:
                return entry
        return None

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'document_id': self.document_id,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'data': [entry.to_dict() for entry in self.data]
        }

    def __str__(self):
        entries_str = "\n".join(str(entry) for entry in self.data)
        return (f"ConsumptionData(Document ID: {self.document_id}, "
                f"Start Date: {self.start_date}, End Date: {self.end_date}, "
                f"Entries:\n{entries_str})")
