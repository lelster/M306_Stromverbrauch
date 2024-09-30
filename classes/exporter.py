"""Class"""
# Import Local Classes
from meter_data import MeterData
from consumtion_data import ConsumptionData

class Exporter:
    """Docstring"""
    @staticmethod
    def export_to_csv(file_path: str, consumption_data: list[ConsumptionData], meter_data: list[MeterData]) -> bool:
        """Docstring"""
        return False

    @staticmethod
    def export_to_json(file_path: str, consumption_data: list[ConsumptionData], meter_data: list[MeterData]) -> bool:
        """Docstring"""
        return False
