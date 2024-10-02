import customtkinter as ctk

class Gui:
    """GUI zur Auswahl von Visualisierung oder Export mit Formatwahl"""

    def __init__(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("green")

        self.root = ctk.CTk()
        self.root.title("Export und Visualisierung")
        self.root.geometry("400x300")

        self.choice = None
        self.export_format = None
        self.filedialog = ctk.filedialog.askdirectory

        self.visualise_button = ctk.CTkButton(self.root, text='Visualisieren', command=self.choose_visualise)
        self.visualise_button.pack(pady=(70, 10))

        self.export_button = ctk.CTkButton(self.root, text='Exportieren', command=self.choose_export)
        self.export_button.pack(pady=(10, 10))

        self.label = ctk.CTkLabel(self.root, text="Exportformat wählen:")
        self.label.pack(pady=(10, 5))

        self.export_format_var = ctk.StringVar(value="csv")

        self.csv_radio = ctk.CTkRadioButton(self.root, text='CSV', variable=self.export_format_var, value='csv')
        self.csv_radio.pack(pady=5)

        self.json_radio = ctk.CTkRadioButton(self.root, text='JSON', variable=self.export_format_var, value='json')
        self.json_radio.pack(pady=5)

        self.root.mainloop()

    def choose_visualise(self):
        self.choice = 'visualise'
        self.root.destroy()

    def choose_export(self):
        self.choice = 'export'
        self.filedialog = self.filedialog()
        self.export_format = self.export_format_var.get()
        self.root.destroy()
