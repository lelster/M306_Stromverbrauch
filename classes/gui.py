import tkinter

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from classes.consumtion_data import ConsumptionData
from classes.exporter import Exporter
from classes.meter_data import MeterData
from classes.apprun import apprun


class Gui:
    """GUI zur Auswahl von Visualisierung oder Export mit Formatwahl"""

    def __init__(self, dataConsumption, dataMeter):
        print("Gui initialized")
        self.back_button = None
        self.esl_button = None
        self.sdat_button = None
        self.dataConsumption = dataConsumption
        self.dataMeter = dataMeter
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("green")

        self.root = ctk.CTk()
        self.root.title("Export und Visualisierung")
        self.root.geometry("400x400")
        self.root.eval('tk::PlaceWindow . center')

        self.choice = None
        self.export_format = None
        self.filedialog = None

        self.visualise_button = ctk.CTkButton(self.root, text='Visualisieren', command=self.choose_visualise)
        self.visualise_button.pack(pady=(50, 10))

        self.add_files_button = ctk.CTkButton(self.root, text='Add Files', command=self.show_add_files_options)
        self.add_files_button.pack(pady=(10, 10))

        self.export_button = ctk.CTkButton(self.root, text='Exportieren', command=self.choose_export)
        self.export_button.pack(pady=(10, 10))

        self.obis_var = ctk.StringVar(value="ID742")
        self.obis_label = ctk.CTkLabel(self.root, text="Sensor ID wählen:")
        self.obis_label.pack(pady=(10, 5))
        self.obis_dropdown = ctk.CTkComboBox(self.root, state="readonly", values=["ID735", "ID742"], variable=self.obis_var)
        self.obis_dropdown.pack(pady=5)

        self.export_format_var = ctk.StringVar(value="csv")

        self.label = ctk.CTkLabel(self.root, text="Exportformat wählen:")
        self.label.pack(pady=(10, 5))

        self.format_dropdown = ctk.CTkComboBox(self.root, state="readonly", values=["csv", "json"], variable=self.export_format_var)
        self.format_dropdown.pack(pady=5)

        self.root.mainloop()

    def choose_visualise(self):
        self.root.destroy()
        apprun(self.dataConsumption, self.dataMeter)

    def choose_export(self):
        self.filedialog = tkinter.filedialog.askdirectory()
        if not self.filedialog:
            messagebox.showwarning("No Directory", "Please select a directory to export.")
            return
        self.export_format = self.export_format_var.get()
        self.export(self.filedialog, self.obis_var.get(), self.export_format, self.dataConsumption, self.dataMeter)

    def show_add_files_options(self):
        self.visualise_button.pack_forget()
        self.export_button.pack_forget()
        self.label.pack_forget()
        self.format_dropdown.pack_forget()
        self.add_files_button.pack_forget()
        self.esl_button = ctk.CTkButton(self.root, text="New ESL-File", command=self.add_new_esl_file)
        self.esl_button.pack(pady=(100, 10))
        self.sdat_button = ctk.CTkButton(self.root, text="New SDAT-File", command=self.add_new_sdat_file)
        self.sdat_button.pack(pady=10)
        self.back_button = ctk.CTkButton(self.root, text="<", width=30, height=30, corner_radius=10,
                                    fg_color="white", text_color="black", command=self.show_buttons)
        self.back_button.place(x=10, y=10)

    def add_new_sdat_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            destination = 'data/public/SDAT-Files'
            if not os.path.exists(destination):
                os.makedirs(destination)
            os.rename(file_path, os.path.join(destination, os.path.basename(file_path)))
            self.show_buttons()

    def add_new_esl_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            destination = 'data/public/ESL-Files'
            if not os.path.exists(destination):
                os.makedirs(destination)
            os.rename(file_path, os.path.join(destination, os.path.basename(file_path)))
            self.show_buttons()

    def show_buttons(self):
        self.visualise_button.pack(pady=(50, 10))
        self.add_files_button.pack(pady=(10, 10))
        self.export_button.pack(pady=(10,10))
        self.label.pack(pady=(10, 5))
        self.format_dropdown.pack(pady=5)
        self.sdat_button.pack_forget()
        self.esl_button.pack_forget()
        self.back_button.place_forget()

    def export(self, path: str, obiscode: str, export_type: str, dataConsumption: list[ConsumptionData], dataMeter: list[MeterData]):
        exporter = Exporter()
        if export_type == 'csv':
            exporter.export_to_csv(path, obiscode, dataConsumption, dataMeter)
            print("csv exported")
        elif export_type == 'json':
            exporter.export_to_json(path, obiscode, dataConsumption, dataMeter)
            print("json exported")
        else:
            print(f"Export type {export_type} is not supported.")
