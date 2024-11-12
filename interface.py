import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

class proyect:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto II ADA II")

        self.select_file_button = tk.Button(root, text="Seleccionar archivo", command=self.select_file)
        self.select_file_button.pack(pady=10)

        self.file_label = tk.Label(root, text="Ningún archivo seleccionado")
        self.file_label.pack(pady=5)

        self.run_model_button = tk.Button(root, text="Ejecutar en MiniZinc", command=self.run_model, state=tk.DISABLED)
        self.run_model_button.pack(pady=10)

        self.result_text = tk.Text(root, height=10, width=50)
        self.result_text.pack(pady=10)
        self.result_text.insert(tk.END, "Aquí se mostrará el resultado de MiniZinc.\n")

        self.file_path = ""

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=(("Archivos MPL", "*.mpl"),))
        if file_path:
            self.file_path = file_path
            self.file_label.config(text=f"Archivo seleccionado: {os.path.basename(file_path)}")
            self.convert_file()

    def convert_file(self):
        if self.file_path and self.file_path.endswith(".mpl"):
            dzn_file_path = self.file_path.replace(".mpl", ".dzn")
            try:
                with open(self.file_path, "r") as mpl_file:
                    data = mpl_file.read()

                with open(dzn_file_path, "w") as dzn_file:
                    dzn_file.write(data)  

                self.result_text.insert(tk.END, f"Archivo elegido: {dzn_file_path}\n")
                self.run_model_button.config(state=tk.NORMAL)
                print(f"Archivo .dzn creado en: {dzn_file_path}") 
            except Exception as e:
                messagebox.showerror("Error", f"Error al convertir archivo: {str(e)}")
        else:
            messagebox.showerror("Error", "Por favor, selecciona un archivo .mpl válido.")

    def run_model(self):
        dzn_file_path = self.file_path.replace(".mpl", ".dzn")
        if os.path.exists(dzn_file_path):
            try:
           
                minizinc_executable = "minizinc"  #"C:\\Program Files\\MiniZinc\\minizinc.exe"
                minizinc_model_path = "proyecto.mzn"
                
                result = subprocess.run([minizinc_executable, minizinc_model_path, dzn_file_path], capture_output=True, text=True)

                if result.returncode == 0:
                    self.result_text.insert(tk.END, f"Resultado de MiniZinc:\n{result.stdout}\n")
                else:
                    self.result_text.insert(tk.END, f"Error en MiniZinc:\n{result.stderr}\n")
                    print(f"Error en MiniZinc: {result.stderr}")  
            except Exception as e:
                messagebox.showerror("Error", f"Error al ejecutar MiniZinc: {str(e)}")
                print(f"Error en ejecución de MiniZinc: {str(e)}")
        else:
            messagebox.showerror("Error", "No se encontró el archivo .dzn.")


if __name__ == "__main__":
    root = tk.Tk()
    app = proyect(root)
    root.mainloop()

