"""Main File with Workflow"""
from classes.file_reader import FileReader
from classes.data_processor import DataProcessor
from classes.data_visualizer import DataVisualizer
from classes.meter_data import MeterData
from classes.consumtion_data import ConsumptionData, ConsumptionEntry
from classes.exporter import Exporter
from classes.gui import Gui

def main():
    """
    Main Workflow
    """
    reader = FileReader()
    dataConsumption: list[ConsumptionData] = reader.read_sdat_files("./data/public/SDAT-Files")
    dataMeter: list[MeterData] = reader.read_esl_files("./data/public/ESL-Files")

    exporter = Exporter()

    exporter.export_to_json("./data/public/json", dataConsumption, dataMeter)
    print("cum")


if __name__ == "__main__":
    main()
