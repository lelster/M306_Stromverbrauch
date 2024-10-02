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
    data: list[ConsumptionData] = reader.read_sdat_files("C:\\Users\\Leonardo Mocci\\Desktop\\XML-Files\\SDAT-Files")
    data: list[MeterData] = reader.read_esl_files("C:\\Users\\Leonardo Mocci\\Desktop\\XML-Files\\ESL-Files")


if __name__ == "__main__":
    main()
