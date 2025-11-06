import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import traceback
from PIL import Image, ImageTk  # Importa PIL para manejar la imagen
import webbrowser
import sys
from pathlib import Path
from main import main as run_generator


class XSDToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("XSDtoCODE")
        
        # Tamaño de la ventana
        window_width = 400
        window_height = 520
        
        # Obtener dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calcular la posición para centrar la ventana
        position_top = int(screen_height / 2 - window_height / 2)
        position_left = int(screen_width / 2 - window_width / 2)

        # Establecer la geometría de la ventana
        self.root.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')
        
        self.root.resizable(False, False)  # Esto hace que la ventana no sea redimensionable

        self.xsd_path = tk.StringVar()
        self.language = tk.StringVar(value="java")
        self.output_dir = tk.StringVar()

        self.build_ui()

    def build_ui(self):
        # Crear un contenedor para centrar los elementos
        center_frame = tk.Frame(self.root)
        center_frame.pack(expand=True)

        # Cargar y redimensionar el logo
        if getattr(sys, 'frozen', False):
            # Si está empaquetado, se accede a los recursos desde _MEIPASS
            base_path = Path(sys._MEIPASS)
            icon_path = Path(sys._MEIPASS) / "iconogui.ico"
        else:
            # Si está en desarrollo, usa la ruta actual
            base_path = Path(__file__).parent
            icon_path = "iconogui.ico"

        try:
            self.root.iconbitmap(default=str(icon_path))
            
            logo = Image.open(base_path/"logo.png")  # Abre el archivo de imagen
            logo = logo.resize((150, 150))  # Redimensiona el logo a 150x150 píxeles (ajusta según sea necesario)
            logo = ImageTk.PhotoImage(logo)  # Convierte la imagen a un formato compatible con Tkinter

             # Mostrar el logo de la empresa
            logo_label = tk.Label(self.root, image=logo)
            logo_label.image = logo  # Guardar una referencia para evitar que la imagen se elimine
            logo_label.pack(pady=10)
            logo_label.bind("<Button-1>", self.open_services_page)  # Asocia la función al clic en el logo
        except Exception as e:
            print(f"No se pudo cargar el ícono o el logo: {e}")    


        # Nombre de la empresa debajo del logo
        company_name_label = tk.Label(self.root, text="A&G Programación y Desarrollo de Sistemas Informáticos S.A.",
                                      fg="blue", cursor="hand2")
        company_name_label.pack(pady=5)
        company_name_label.bind("<Button-1>", self.open_services_page)  # Asocia la función al clic en el nombre

        # Agregar el enlace a los servicios de la empresa
        tk.Label(self.root, text="Conozca más de nuestros servicios", fg="blue", cursor="hand2").pack(pady=5)
        self.build_ui_elements()

    def open_services_page(self, event=None):
        webbrowser.open("https://agsoft.co.cr/servicios/")

    def build_ui_elements(self):
        # Entrada para el archivo XSD
        tk.Label(self.root, text="Archivo XSD:").pack(pady=5)
        entry = tk.Entry(self.root, textvariable=self.xsd_path, width=40)
        entry.pack()
        tk.Button(self.root, text="Buscar...", command=self.browse_file).pack(pady=5)

        # Selector de lenguaje
        tk.Label(self.root, text="Lenguaje de salida:").pack(pady=5)
        lang_combo = ttk.Combobox(self.root, textvariable=self.language, values=["java", "python", "csharp", "JSONSchema"])
        lang_combo.pack()

        # Selector de carpeta de salida
        tk.Label(self.root, text="Carpeta de salida:").pack(pady=5)
        output_entry = tk.Entry(self.root, textvariable=self.output_dir, width=40)
        output_entry.pack()
        tk.Button(self.root, text="Seleccionar carpeta...", command=self.browse_output_folder).pack(pady=5)

        # Botón para generar el código
        tk.Button(self.root, text="Generar Código", command=self.generate_code).pack(pady=15)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("XSD files", "*.xsd")])
        if file_path:
            self.xsd_path.set(file_path)

    def browse_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_dir.set(folder_path)

    def generate_code(self):
        xsd = self.xsd_path.get()
        lang = self.language.get()
        output_folder = self.output_dir.get()

        if not xsd:
            messagebox.showerror("Error", "Debes seleccionar un archivo XSD.")
            return

        if not output_folder:
            messagebox.showerror("Error", "Debes seleccionar una carpeta de salida.")
            return

        # Crear la ventana de carga
        loading_win = tk.Toplevel(self.root)
        loading_win.title("Generando...")
        loading_win.geometry("300x100")
        loading_win.resizable(False, False)

        # Deshabilitar botón de cerrar
        loading_win.protocol("WM_DELETE_WINDOW", lambda: None)

        # Eliminar los botones de minimizar/maximizar en Windows
        loading_win.attributes("-toolwindow", True)

        # Hacerla modal: evitar interacción con la ventana principal
        loading_win.transient(self.root)
        loading_win.grab_set()

        # Centrar la ventana de carga
        loading_win.update_idletasks()
        x = (loading_win.winfo_screenwidth() - 300) // 2
        y = (loading_win.winfo_screenheight() - 100) // 2
        loading_win.geometry(f"+{x}+{y}")

        tk.Label(loading_win, text="Generando, por favor espere...").pack(pady=10)
        progress_bar = ttk.Progressbar(loading_win, mode='indeterminate')
        progress_bar.pack(fill='x', padx=20, pady=10)
        progress_bar.start()

        # Ejecutar en segundo plano
        def task():
            try:
                run_generator(xsd, lang, output_folder)
                self.root.after(0, lambda: messagebox.showinfo("Éxito", "Código generado correctamente."))
            except Exception as e:
                error_message = f"Ocurrió un error: {str(e)}\n\n{traceback.format_exc()}"
                print(error_message)  # Imprimir el error en consola
                self.root.after(0, lambda: messagebox.showerror("Error", error_message))
            finally:
                self.root.after(0, loading_win.destroy)

        import threading
        threading.Thread(target=task).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = XSDToolGUI(root)
    root.mainloop()
