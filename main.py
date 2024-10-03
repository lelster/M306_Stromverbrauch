import threading
import multiprocessing
from classes.file_reader import FileReader
from classes.gui import Gui
from classes.apprun import apprun

def read():
    """Function to read data."""
    reader = FileReader()
    data_consumption = reader.read_sdat_files("./data/public/SDAT-Files")
    data_meter = reader.read_esl_files("./data/public/ESL-Files")
    return data_consumption, data_meter

def run_flask():
    """Run Flask/Dash app in a separate process."""
    data_consumption, data_meter = read()  # Initialize inside the Flask process
    apprun(data_consumption, data_meter)

def main():
    print("Initiating...")
    print("Loading data...")

    data_consumption, data_meter = read()

    # Start Flask/Dash in a separate process (without passing data)
    flask_process = multiprocessing.Process(target=run_flask)
    flask_process.start()

    # Run GUI on the main thread
    Gui(data_consumption, data_meter)

    # Wait for Flask process to finish
    flask_process.join()

if __name__ == "__main__":
    main()
