"""Class"""
# Import Local Classes
import json
import os
from meter_data import MeterData
from consumtion_data import ConsumptionData, ConsumptionEntry


class Exporter:
    """Docstring"""
    @staticmethod
    def export_to_csv(file_path: str, consumption_data: list[ConsumptionData], meter_data: list[MeterData]) -> bool:
        """Docstring"""
        return False

    @staticmethod
    def export_to_json(file_path: str, consumption_data: list[ConsumptionData], meter_data: list[MeterData]) -> bool:
        """Docstring"""
        try:
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            consumption_file_path = os.path.join(file_path, "consumption_data.json")
            meter_file_path = os.path.join(file_path, "meter_data.json")

            with open(meter_file_path, "w") as file:
                json.dump(([x.__dict__ for x in meter_data]), file, indent=4)

            with open(consumption_file_path, "w") as file:
                json.dump(([x.__dict__ for x in consumption_data]), file, indent=4)

            return True
        except Exception as e:
            print(f"Error writing JSON files: {e}")
            return False

if __name__ == "__main__":
    pass
