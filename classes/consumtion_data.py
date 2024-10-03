"""ConsumptionEntry & ConsumtionData Class"""
from datetime import datetime

class ConsumptionEntry:
    """Represents a single consumption entry with volume and timestamp."""
    def __init__(self, volume: float, timestamp: datetime):
        """
        Args:
            volume (float): The consumption volume at the given timestamp.
            timestamp (datetime): The time at which the consumption was recorded.
        """
        self.volume = volume
        self.timestamp = timestamp

    def to_dict(self):
        """
        Convert to dictionary for JSON serialization.
        
        Returns:
            dict: A dictionary representation of the consumption entry, with the volume and
            timestamp converted to an ISO 8601 string format.
        """
        return {
            'volume': self.volume,
            'timestamp': self.timestamp.isoformat()
        }

    def __str__(self):
        """
        Returns:
            str: A string representing the volume and timestamp of the consumption entry.
        """
        return f"ConsumptionEntry(Volume: {self.volume}, Timestamp: {self.timestamp})"

class ConsumptionData:
    """Contains consumption data including document ID and a list of consumption entries."""
    def __init__(self, document_id: str, start_date: datetime, end_date: datetime):
        """
        Args:
            document_id (str): A unique identifier for the consumption data document.
            start_date (datetime): The start date of the consumption period.
            end_date (datetime): The end date of the consumption period.
        """
        self.document_id = document_id
        self.start_date = start_date
        self.end_date = end_date
        self.data: list[ConsumptionEntry] = []

    def add_entry(self, item: ConsumptionEntry) -> None:
        """
        Adds a consumption entry to the data list.
        
        Args:
            item (ConsumptionEntry): The consumption entry to add.

        Returns:
            None
        """
        self.data.append(item)

    def get_consumption(self, date: datetime) -> ConsumptionEntry:
        """
        Retrieves a consumption entry by date.
        
        Args:
            date (datetime): The date for which to retrieve the consumption entry.

        Returns:
            ConsumptionEntry: The consumption entry for the specified date,
            or None if no entry exists.
        """
        for entry in self.data:
            if entry.timestamp == date:
                return entry
        return None

    def to_dict(self):
        """
        Convert to dictionary for JSON serialization.
        
        Returns:
            dict: A dictionary representation of the consumption data, including the document ID,
            start and end dates, and a list of consumption entries (also as dictionaries).
        """
        return {
            'document_id': self.document_id,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'data': [entry.to_dict() for entry in self.data]
        }

    def __str__(self):
        """
        Returns:
            str: A string showing the document ID, the date range,
                and the list of consumption entries.
        """
        entries_str = "\n".join(str(entry) for entry in self.data)
        return (f"ConsumptionData(Document ID: {self.document_id}, "
                f"Start Date: {self.start_date}, End Date: {self.end_date}, "
                f"Entries:\n{entries_str})")
