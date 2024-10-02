"""Class"""
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Import Local Classes
from classes.meter_data import MeterData
from classes.consumtion_data import ConsumptionEntry, ConsumptionData

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

            for key, value in reading_data.items():
                meter_data.add_reading(key, value)

            return meter_data

        except Exception as e:
            print(f"An error occurred while parsing the file {filepath}: {e}")
            return None

    @staticmethod
    def read_sdat_files(dirpath: str) -> list[ConsumptionData]:
        """Reads all SDAT files in the given directory and returns a list of ConsumptionData."""
        files = [os.path.join(dirpath, f) for f in os.listdir(dirpath)
                 if os.path.isfile(os.path.join(dirpath, f)) and f.endswith(".xml")]
        files.sort()
        result_data: list[ConsumptionData] = []
        for file in files:
            new_data = FileReader.read_sdat_file(file)
            if new_data is not None:
                result_data.append(new_data)
            else:
                raise SystemError(f"An error occurred while reading SDAT file {file}")
        return result_data

    @staticmethod
    def read_sdat_file(filepath: str) -> ConsumptionData:
        """Reads an SDAT file and returns a ConsumptionData object."""
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()

            ns = {'rsm': 'http://www.strom.ch'}

            ET.register_namespace('rsm', 'http://www.strom.ch')
            ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')

            header_info = root.find('rsm:ValidatedMeteredData_HeaderInformation', ns)
            if header_info is None:
                return None
            instance_doc = header_info.find('rsm:InstanceDocument', ns)
            if instance_doc is None:
                return None
            document_id_elem = instance_doc.find('rsm:DocumentID', ns)
            if document_id_elem is None:
                return None
            document_id_text = document_id_elem.text
            if document_id_text is None:
                return None

            document_id_parts = document_id_text.split('_')
            id_code = document_id_parts[-1] if len(document_id_parts) > 0 else document_id_text

            metering_data = root.find('rsm:MeteringData', ns)
            if metering_data is None:
                return None
            interval = metering_data.find('rsm:Interval', ns)
            if interval is None:
                return None
            start_datetime_elem = interval.find('rsm:StartDateTime', ns)
            end_datetime_elem = interval.find('rsm:EndDateTime', ns)
            if start_datetime_elem is None or end_datetime_elem is None:
                return None
            start_datetime_str = start_datetime_elem.text
            end_datetime_str = end_datetime_elem.text

            start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%dT%H:%M:%SZ")
            end_datetime = datetime.strptime(end_datetime_str, "%Y-%m-%dT%H:%M:%SZ")

            consumption_data = ConsumptionData(document_id=id_code, start_date=start_datetime, end_date=end_datetime)

            resolution_elem = metering_data.find('rsm:Resolution', ns)
            if resolution_elem is None:
                return None
            resolution_value_elem = resolution_elem.find('rsm:Resolution', ns)
            resolution_unit_elem = resolution_elem.find('rsm:Unit', ns)
            if resolution_value_elem is None or resolution_unit_elem is None:
                return None
            resolution_value = int(resolution_value_elem.text)
            resolution_unit = resolution_unit_elem.text

            if resolution_unit == 'MIN':
                resolution_timedelta = timedelta(minutes=resolution_value)
            elif resolution_unit == 'H':
                resolution_timedelta = timedelta(hours=resolution_value)
            else:
                resolution_timedelta = timedelta(minutes=resolution_value)

            observations = metering_data.findall('rsm:Observation', ns)
            if not observations:
                return None

            current_timestamp = start_datetime

            for obs in observations:
                volume_elem = obs.find('rsm:Volume', ns)
                if volume_elem is None:
                    continue
                volume_str = volume_elem.text
                if volume_str is None:
                    continue
                volume = float(volume_str)

                consumption_entry = ConsumptionEntry(volume=volume, timestamp=current_timestamp)
                consumption_data.add_entry(consumption_entry)

                current_timestamp += resolution_timedelta

            return consumption_data

        except Exception as e:
            print(f"An error occurred while parsing the file {filepath}: {e}")
            return None
