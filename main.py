"""Main File with Workflow"""
from classes.file_reader import FileReader
from classes.data_processor import DataProcessor
from classes.data_visualizer import DataVisualizer
from classes.meter_data import MeterData
from classes.consumtion_data import ConsumptionData, ConsumptionEntry
from classes.exporter import Exporter
from classes.gui import Gui


def read() -> (list[ConsumptionData], list[MeterData]):
    reader = FileReader()
    dataConsumption: list[ConsumptionData] = reader.read_sdat_files("./data/public/SDAT-Files")
    dataMeter: list[MeterData] = reader.read_esl_files("./data/public/ESL-Files")
    return dataConsumption, dataMeter


def export(path: str, export_type: str, dataConsumption: list[ConsumptionData], dataMeter: list[MeterData]):
    exporter = Exporter()
    if export_type == 'csv':
        exporter.export_to_csv(path, dataConsumption, dataMeter)
        print("csv exported")
    elif export_type == 'json':
        exporter.export_to_json(path, dataConsumption, dataMeter)
        print("json exported")
    else:
        print(f"Export type {export_type} is not supported.")



def main():
    print("reading data...")
    dataConsumption, dataMeter = read()
    gui = Gui()
    if gui.choice == 'visualise':
        pass
    elif gui.choice == 'export':
        path = str(gui.filedialog)
        export_type = str(gui.export_format).lower()
        export(path, export_type, dataConsumption, dataMeter)

if __name__ == "__main__":
    main()
