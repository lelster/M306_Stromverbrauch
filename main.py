# main.py
"""Main File with Workflow"""
from classes.file_reader import FileReader
from classes.consumtion_data import ConsumptionData
from classes.gui import Gui
from classes.meter_data import MeterData

def read() -> (list[ConsumptionData], list[MeterData]):
    reader = FileReader()
    dataConsumption: list[ConsumptionData] = reader.read_sdat_files("./data/public/SDAT-Files")
    dataMeter: list[MeterData] = reader.read_esl_files("./data/public/ESL-Files")
    return dataConsumption, dataMeter

def main():
    print("Reading data...")
    dataConsumption, dataMeter = read()
    Gui(dataConsumption, dataMeter)

if __name__ == "__main__":
    main()
