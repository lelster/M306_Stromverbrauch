"""Class"""
import os
from datetime import datetime
import xml.etree.ElementTree as ET

# Import Local Classes
from meter_data import MeterData
from consumtion_data import ConsumptionEntry, ConsumptionData

class FileReader:
    """FileReader class to read ESL files and parse meter data."""
    @staticmethod
    def read_esl_files(dirpath: str) -> list[MeterData]:
        """Reads all ESL files in the given directory and returns a list of MeterData."""
        files = [os.path.join(dirpath, f) for f in os.listdir(dirpath)
                 if os.path.isfile(os.path.join(dirpath, f)) and f.endswith(".xml")]
        files.sort()
        result_data: list[MeterData] = []
        for file in files:
            new_data = FileReader.read_esl_file(file)
            if new_data is not None:
                result_data.append(new_data)
            else:
                raise SystemError(f"An error occurred while reading ESL file {file}")
        return result_data

    @staticmethod
    def read_esl_file(filepath: str) -> MeterData:
        """Reads one ESL file and returns the first MeterData found."""
        obis_id_codes: dict[str, str] = {
            "1-1:1.8.1": "ID742", "1-1:1.8.2": "ID742",
            "1-1:2.8.1": "ID735", "1-1:2.8.2": "ID735",
        }
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()

            meter_elem = root.find('Meter')
            if meter_elem is None:
                return None

            time_period_elems = meter_elem.findall('TimePeriod')
            if not time_period_elems:
                return None
            time_period_elem = time_period_elems[0]

            end_date_str = time_period_elem.get('end')
            if end_date_str is None:
                return None
            end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M:%S")

            meter_data = MeterData(end_date)

            reading_data: dict[str, float] = {"ID742": 0.000, "ID735": 0.000}

            value_rows = time_period_elem.findall('ValueRow')
            if not value_rows:
                return None

            for value_row in value_rows:
                obis = value_row.get('obis')
                status = value_row.get('status')
                value_str = value_row.get('value')

                if obis is None or status is None or value_str is None:
                    continue

                sensor_id = obis_id_codes.get(obis)
                if sensor_id is not None:
                    if status == 'V':
                        value = float(value_str)
                        reading_data[sensor_id] += value
                    else:
                        raise ValueError(f"Obis has invalid data; {filepath}; {obis}")

            # Add readings to meter_data
            for key, value in reading_data.items():
                meter_data.add_reading(key, value)

            return meter_data

        except Exception as e:
            print(f"An error occurred while parsing the file {filepath}: {e}")
            return None

    @staticmethod
    def read_sdat_files(dirpath: str) -> list[MeterData]:
        """Reads all SDAT files in the given directory and returns a list of MeterData."""
        files = [os.path.join(dirpath, f) for f in os.listdir(dirpath)
                 if os.path.isfile(os.path.join(dirpath, f)) and f.endswith(".xml")]
        files.sort()
        result_data: list[MeterData] = []
        for file in files:
            new_data = FileReader.read_esl_file(file)
            if new_data is not None:
                result_data.append(new_data)
            else:
                raise SystemError(f"An error occurred while reading SDAT file {file}")
        return result_data

    @staticmethod
    def read_sdat_file(filepath: str) -> ConsumptionData:
        """Docstring"""
        result = ConsumptionData("dummy_doc", datetime.now())

        # Example of adding an entry of a sequence for consumptions
        result.add_entry(ConsumptionEntry(2.700, datetime.now()))

        return result

if __name__ == "__main__":
    reader = FileReader()
    data: list[MeterData] = reader.read_esl_files("C:\\Users\\KSH\\Downloads\\M306\\M306_Stromverbrauch\\data\\ESL-Files\\")
    for i in data:
        print(i)
