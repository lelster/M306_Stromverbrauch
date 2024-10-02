"""Class"""
# Import Local Classes
from datetime import datetime
from classes.meter_data import MeterData
from classes.consumtion_data import ConsumptionEntry, ConsumptionData

class DataProcessor:
    """Docstring"""
    @staticmethod
    def match_data(sensor_id: str, sdat_data: list[ConsumptionData], date: datetime = None) -> dict:
        """Docstring"""
        combined_data = [i for i in sdat_data if i.document_id == sensor_id]
        date_combined_data = [i for i in combined_data if i.timestamp.year == date.year and i.timestamp.month == date.month] if date != None else None
        if date_combined_data is None:
            result = combined_data
        else:
            result = [i for i in combined_data if i in date_combined_data]

        if len(result) == 0:
            return None
        else:
            return result

    @staticmethod
    def calculate_total_consumption(esl_data: MeterData, sdat_data: ConsumptionData, sensor_id: str) -> float:
        """Docstring"""
        total_consumption = 0.0
        # TODO: Calculate total consumtion
        return total_consumption

    @staticmethod
    def combine_esl_data(data: list[MeterData]) -> list[MeterData]:
        """Docstring"""
        # TODO: combine esl data
        return None
