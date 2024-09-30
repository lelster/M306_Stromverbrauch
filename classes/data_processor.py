"""Class"""
# Import Local Classes
from meter_data import MeterData
from consumtion_data import ConsumptionData

class DataProcessor:
    """Docstring"""
    @staticmethod
    def match_data(sdat_data: ConsumptionData, esl_data: MeterData) -> dict[str, float]:
        """Docstring"""
        combined_data = {}
        # TODO: Match Data
        return combined_data

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
