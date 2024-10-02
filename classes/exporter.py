"""Class"""
# Import Local Classes
from classes.meter_data import MeterData
from classes.consumtion_data import ConsumptionEntry, ConsumptionData

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
