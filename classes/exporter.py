"""Class"""
# Import Local Classes
import csv
import json
import os
from datetime import datetime
from classes.meter_data import MeterData
from classes.consumtion_data import ConsumptionData, ConsumptionEntry


class Exporter:
    """Exporter for Consumption and Meter Data."""

    @staticmethod
    def datetime_converter(o):
        """Convert datetime objects to ISO format strings for JSON serialization."""
        if isinstance(o, datetime):
            return o.isoformat()

    @staticmethod
    def export_to_csv(file_path: str, consumption_data: list[ConsumptionData], meter_data: list[MeterData]) -> bool:
        """Export consumption and meter data to CSV files."""
        try:
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            # Export Consumption Data to CSV
            consumption_file_path = os.path.join(file_path, "consumption_data.csv")
            with open(consumption_file_path, "w", newline="") as file:
                writer = csv.writer(file, delimiter=';')
                # Write headers for consumption data
                writer.writerow(["document_id", "start_date", "end_date", "timestamp", "volume"])
                # Write consumption data rows
                for data in consumption_data:
                    for entry in data.data:
                        writer.writerow([data.document_id,
                                         data.start_date.isoformat(),
                                         data.end_date.isoformat(),
                                         entry.timestamp.isoformat(),
                                         entry.volume])

            meter_file_path = os.path.join(file_path, "meter_data.csv")
            with open(meter_file_path, "w", newline="") as file:
                writer = csv.writer(file, delimiter=';')
                # Write headers for meter data
                writer.writerow(["timestamp", "obis_code", "reading"])
                # Write meter data rows
                for meter in meter_data:
                    for obis_code, reading in meter.data.items():
                        writer.writerow([meter.timestamp.isoformat(),  # Format the timestamp
                                         obis_code,
                                         reading])  # Write the OBIS code and reading

            return True
        except Exception as e:
            print(f"Error writing CSV files: {e}")
            return False

    @staticmethod
    def export_to_json(file_path: str, consumption_data: list[ConsumptionData], meter_data: list[MeterData]) -> bool:
        """Export consumption and meter data to JSON files."""
        try:
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            consumption_file_path = os.path.join(file_path, "consumption_data.json")
            meter_file_path = os.path.join(file_path, "meter_data.json")

            with open(meter_file_path, "w") as file:
                json.dump([x.__dict__ for x in meter_data], file, default=Exporter.datetime_converter, indent=4)

            with open(consumption_file_path, "w") as file:
                json.dump([x.to_dict() for x in consumption_data], file, indent=4)

            return True
        except Exception as e:
            print(f"Error writing JSON files: {e}")
            return False


if __name__ == "__main__":
    pass
