import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

class Proyecto:
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
            directory = "archivos"
            if not os.path.exists(directory):
                os.makedirs(directory)

            dzn_file_path = os.path.join(directory, os.path.basename(self.file_path).replace(".mpl", ".dzn"))
            try:
                with open(self.file_path, "r") as mpl_file:
                    lines = mpl_file.readlines()

                n = int(lines[0].strip())  # Número de personas
                m = int(lines[1].strip())  # Número de opiniones posibles
                pi = list(map(int, lines[2].strip().split(',')))  # Distribución de personas
                vi = list(map(float, lines[3].strip().split(',')))  # Opiniones posibles
                cei = list(map(float, lines[4].strip().split(',')))  # Costos extras
                c = [list(map(float, line.strip().split(','))) for line in lines[5:5 + m]]  # Costos de desplazamiento
                ct = float(lines[5 + m].strip())  # Costo total máximo permitido
                max_movs = int(lines[6 + m].strip())  # Límite de movimientos
               

                with open(dzn_file_path, "w") as dzn_file:
                    dzn_file.write(f"n = {n};\n")
                    dzn_file.write(f"m = {m};\n")
                    dzn_file.write(f"p = {pi};\n")
                    dzn_file.write(f"v = {vi};\n")
                    dzn_file.write(f"c = array2d(1..{m}, 1..{m}, [\n    " + ",\n    ".join([", ".join(map(str, row)) for row in c]) + "\n]);\n")
                    dzn_file.write(f"ce = {cei};\n")
                    dzn_file.write(f"ct = {ct};\n")
                    dzn_file.write(f"maxMovs = {max_movs};\n")

                self.result_text.insert(tk.END, f"Archivo .dzn creado en: {dzn_file_path}\n")
                self.run_model_button.config(state=tk.NORMAL)
                print(f"Archivo .dzn creado en: {dzn_file_path}") 
            except Exception as e:
                messagebox.showerror("Error", f"Error al convertir archivo: {str(e)}")
        else:
            messagebox.showerror("Error", "Por favor, selecciona un archivo .mpl válido.")

    def run_model(self):
        # Ruta del archivo de datos .dzn que se va a usar
        dzn_file_path = os.path.join("archivos", os.path.basename(self.file_path).replace(".mpl", ".dzn"))
        print(f"Ruta del archivo .dzn: {dzn_file_path}")
        
        if os.path.exists(dzn_file_path):
            try:
                minizinc_executable = "minizinc"  # Asegúrate de que MiniZinc esté en el PATH del sistema o usa la ruta completa si es necesario.
                minizinc_model_path = "Proyecto.mzn"  # Ruta del archivo del modelo de MiniZinc (.mzn)
                
                if os.path.exists(minizinc_model_path):
                    # Ejecutar el modelo de MiniZinc con el archivo .dzn
                    result = subprocess.run(
                        [minizinc_executable, minizinc_model_path, dzn_file_path], 
                        capture_output=True, 
                        text=True
                    )

                    # Verificar si el proceso se ejecutó correctamente
                    if result.returncode == 0:
                        self.result_text.insert(tk.END, f"Resultado de MiniZinc:\n{result.stdout}\n")
                    else:
                        # Si hay un error en la ejecución, mostrar el mensaje de error
                        self.result_text.insert(tk.END, f"Error en MiniZinc:\n{result.stderr}\n")
                        print(f"Error en MiniZinc: {result.stderr}")
                else:
                    messagebox.showerror("Error", f"No se encontró el archivo de modelo: {minizinc_model_path}")
                    print(f"Error: No se encontró el archivo de modelo: {minizinc_model_path}")
            except Exception as e:
                # Manejo de excepciones si algo falla al ejecutar MiniZinc
                messagebox.showerror("Error", f"Error al ejecutar MiniZinc: {str(e)}")
                print(f"Error en ejecución de MiniZinc: {str(e)}")
        else:
            # Mostrar error si no se encuentra el archivo de datos .dzn
            messagebox.showerror("Error", "No se encontró el archivo .dzn.")
            print("Error: No se encontró el archivo .dzn.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Proyecto(root)
    root.mainloop()


