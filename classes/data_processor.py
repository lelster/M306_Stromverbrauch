"""Class"""
# Import Local Classes
from datetime import datetime
from classes.meter_data import MeterData
from classes.consumtion_data import ConsumptionEntry, ConsumptionData

class DataProcessor:
    """Docstring"""

    @staticmethod
    def filter_data(sdat_data: list[ConsumptionData]) -> list[ConsumptionData]:
        """Eliminates duplicate consumption data and entries from the data."""
        filtered_data = []
        seen_data = set()

        for data in sdat_data:
            data_key = (data.document_id, data.start_date, data.end_date)

            if data_key not in seen_data:
                seen_data.add(data_key)

                unique_entries = []
                seen_entries = set()

                for entry in data.data:
                    entry_key = (entry.timestamp, entry.volume)
                    if entry_key not in seen_entries:
                        seen_entries.add(entry_key)
                        unique_entries.append(entry)
                filtered_data_item = ConsumptionData(data.document_id, data.start_date, data.end_date)
                filtered_data_item.data = unique_entries
                filtered_data.append(filtered_data_item)

        return filtered_data

    @staticmethod
    def get_data(sensor_id: str, sdat_data: list[ConsumptionData], start_date: datetime = None,
                   end_date: datetime = None) -> list[ConsumptionData]:
        """Finds and returns all ConsumptionData that match the sensor ID and fall within the specified date range."""
        new_data = DataProcessor.filter_data(sdat_data)
        combined_data = [data for data in new_data if data.document_id == sensor_id]

        if start_date and end_date:
            date_filtered_data = [
                data for data in combined_data
                if (data.start_date >= start_date and data.end_date <= end_date)
            ]
        else:
            date_filtered_data = combined_data

        if len(date_filtered_data) == 0:
            return None
        else:
            return date_filtered_data

    @staticmethod
    def calculate_total_consumption(esl_data: MeterData, sdat_data: ConsumptionData, sensor_id: str) -> float:
        """Docstring"""
        total_consumption = 0.0
        # TODO: Calculate total consumtion
        return total_consumption


