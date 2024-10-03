"""Class"""
# Import Local Classes
from datetime import datetime
from classes.meter_data import MeterData
from classes.consumtion_data import ConsumptionEntry, ConsumptionData
from collections import defaultdict

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
    def filter_meter_data(meter_data: list[MeterData]) -> list[MeterData]:
        """Eliminates duplicate meter data entries."""
        filtered_data = []
        seen_data = set()

        for data in meter_data:
            data_key = data.timestamp

            if data_key not in seen_data:
                seen_data.add(data_key)

                unique_readings = {}
                for obis_code, value in data.data.items():
                    # Use the OBIS code as a unique key for meter readings
                    if obis_code not in unique_readings:
                        unique_readings[obis_code] = value

                filtered_meter_data = MeterData(data.timestamp)
                filtered_meter_data.data = unique_readings
                filtered_data.append(filtered_meter_data)

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
    def get_data_by_time(sensor_id: str, sdat_data: list[ConsumptionData]) -> dict[str, dict[str, dict[str, list[tuple[datetime, float]]]]]:
        """
        Organizes the consumption data by year, month, and day.
        :return: A nested dictionary where the first level keys are years, second level keys are months,
                 and third level keys are days, with lists of (timestamp, volume) for 15-minute intervals.
        """
        time_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        # Filter data based on sensor_id
        new_data = DataProcessor.filter_data(sdat_data)
        combined_data = [data for data in new_data if data.document_id == sensor_id]

        for data in combined_data:
            for entry in data.data:
                year = entry.timestamp.strftime("%Y")  # Get year as string
                month = entry.timestamp.strftime("%b")  # Get abbreviated month name
                day = entry.timestamp.strftime("%d")  # Get day as string

                # Store the 15-minute interval data (timestamp, volume) in the time_data dictionary
                time_data[year][month][day].append((entry.timestamp, entry.volume))

        return dict(time_data)

    @staticmethod
    def group_meter_data_by_month(meter_data: list[MeterData]) -> dict[tuple[int, int], list[MeterData]]:
        """Groups MeterData by year and month after filtering duplicates."""
        # Filter duplicates before grouping
        filtered_meter_data = DataProcessor.filter_meter_data(meter_data)

        grouped_data = defaultdict(list)  # Create a dictionary with (year, month) as keys

        for data in filtered_meter_data:
            year = data.timestamp.year
            month = data.timestamp.month
            grouped_data[(year, month)].append(data)

        return grouped_data


