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


def export(export_type: str, dataConsumption: list[ConsumptionData], dataMeter: list[MeterData]):
    exporter = Exporter()
    if export_type == 'csv':
        exporter.export_to_csv("./data/public/csv", dataConsumption, dataMeter)
        print("csv exported")
    elif export_type == 'json':
        exporter.export_to_json("./data/public/json", dataConsumption, dataMeter)
        print("json exported")
    else:
        print(f"Export type {export_type} is not supported.")



def main():
    print("reading data...")
    dataConsumption, dataMeter = read()

    print("What file format would you like to export? Options: csv, json")
    export_type = input("Enter export type: ").lower()

    export(export_type, dataConsumption, dataMeter)


if __name__ == "__main__":
    main()
