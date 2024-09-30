"""Class"""
# Import Packages
from datetime import datetime

# Import Local Classes
from meter_data import MeterData
from consumtion_data import ConsumptionEntry, ConsumptionData

class FileReader:
    """Docstring"""
    @staticmethod
    def read_esl_file(filepath: str) -> MeterData:
        """Docstring"""
        result = MeterData("example-id-1", datetime.now())

        # Example of adding a Reading
        result.add_reading("ID742", 8258.1000)

        return result

    @staticmethod
    def read_sdat_file(filepath: str) -> ConsumptionData:
        """Docstring"""
        result = ConsumptionData("dummy_doc", datetime.now())

        # Example of adding an entry of a sequence for consumptions
        result.add_entry(ConsumptionEntry(2.700, datetime.now()))

        return result
