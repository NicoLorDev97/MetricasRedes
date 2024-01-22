import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import funciones as f
import desglose as d

class AplicacionInterfaz:
    def __init__(self):
        self.direct = None
        self.spreadsheet_key = None
        self.df_final = None

        self.root = tk.Tk()
        self.root.title("Interfaz para Procesar Datos")
        self.root.geometry("500x250")

        self.crear_interfaz()

    def centrar_ventana(self, ventana):
        ventana.update_idletasks()
        width = ventana.winfo_width()
        height = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (width // 2)
        y = (ventana.winfo_screenheight() // 2) - (height // 2)
        ventana.geometry(f"+{x}+{y}")

    def crear_interfaz(self):
        titulo_label = tk.Label(self.root, text="Carga de Datos", font=("Helvetica", 20, "bold"))
        titulo_label.pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        direct_button = tk.Button(frame, text="Seleccionar Directorio", command=self.seleccionar_directorio,
                                  bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"), padx=20)
        direct_button.grid(row=0, column=0, pady=10)

        process_button = tk.Button(frame, text="Procesar Datos", command=self.procesar_datos,
                                   bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), padx=20, state=tk.DISABLED)
        process_button.grid(row=1, column=0, pady=10)

        self.centrar_ventana(self.root)

    def seleccionar_directorio(self):
        self.direct = filedialog.askdirectory(title="Seleccionar Directorio")
        if not self.direct:
            messagebox.showerror("Error", "Debes seleccionar un directorio.")
            return

        messagebox.showinfo("Éxito", "Directorio seleccionado correctamente.")
        self.spreadsheet_key = "17Ge3iD3xswqericZ135yf33Jt8fqOg-55GZMw4IuQtk"  # ID de base de datos
        self.df_final = self.procesar_datos_originales()

        # Habilita el boton de carga cuando el directorio ya esta seleccionado
        process_button = self.root.children['!frame'].children['!button2']
        process_button.config(state=tk.NORMAL)

    def procesar_datos_originales(self):
        usuarios = f.ObtenerUsers(self.direct)
        data_inicio = f.ObtenerInicios(self.spreadsheet_key)
        df_final = pd.DataFrame(columns=['UserId', 'InteraccionId', 'Cantidad', 'Fecha'])

        for user in usuarios:
            df_aux = pd.DataFrame(columns=['UserId', 'InteraccionId', 'Cantidad', 'Fecha'])
            inicio = f.ObtenerInicio(data_inicio, user)
            df_aux = f.ObtenerDF(user, df_aux, inicio)
            df_final = pd.concat([df_final, df_aux], ignore_index=True)

        return df_final

    def procesar_datos(self):
        worksheet_name = "Interacciones"
        worksheet = f.ConexionCarga(self.spreadsheet_key, worksheet_name)
        f.Carga(worksheet, self.df_final)
        messagebox.showinfo("Éxito", "Datos procesados y cargados correctamente.")

    def ejecutar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AplicacionInterfaz()
    app.ejecutar()
