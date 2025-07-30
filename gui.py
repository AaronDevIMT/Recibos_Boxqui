import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk
from helpers import obtener_fecha_corte
from acciones import generar_todos, generar_individual
from config import MESES_ES, RUTA_LOGO, RUTA_LOGO_SMALL
import ctypes  # Para icono en barra de tareas en Windows

# ----------------------------
# 🔹 Splash Screen
# ----------------------------
class SplashScreen(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.overrideredirect(True)  # Sin bordes
        self.configure(bg="#f8f9fa")

        # Centrar pantalla
        w, h = 400, 300
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.lift()  # Mantener encima
        self.attributes("-topmost", True)  # Forzar encima

        # Logo
        try:
            img = Image.open(RUTA_LOGO)
            img = img.resize((150, 150))
            self.logo_img = ImageTk.PhotoImage(img)
            tk.Label(self, image=self.logo_img, bg="#f8f9fa").pack(pady=20)
        except:
            tk.Label(self, text="(Logo)", bg="#f8f9fa").pack(pady=20)

        # Texto
        tk.Label(self, text="Generador de Recibos Boxqui", font=("Segoe UI", 14, "bold"), bg="#f8f9fa").pack()
        tk.Label(self, text="Cargando...", font=("Segoe UI", 10), bg="#f8f9fa", fg="gray").pack(pady=10)

        # Cerrar después de unos segundos
        self.after(2000, self.destroy)

# ----------------------------
# 🔹 Ventana Principal
# ----------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()  # Oculta la ventana principal inmediatamente
        self.title("Generador de Recibos Boxqui")
        self.geometry("500x550")
        self.configure(bg="#f8f9fa")

        # Icono ventana y barra tareas
        try:
            ico_path = RUTA_LOGO_SMALL
            # Barra de tareas (solo Windows)
            try:
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("boxqui.generador.recibos")
            except:
                pass
            # Icono de ventana
            self.iconbitmap(ico_path)
            print(f"✅ Icono cargado correctamente desde: {ico_path}")
        except Exception as e:
            print(f"⚠ No se pudo cargar el icono: {e}")

    # 🔹 Cargar logo PNG para cabecera aquí
        try:
            img = Image.open(RUTA_LOGO)
            img = img.resize((120, 120))
            self.logo_img_header = ImageTk.PhotoImage(img)  # Guardar como atributo de App
            print("✅ Logo cargado correctamente en App")
        except Exception as e:
            self.logo_img_header = None
            print(f"⚠ No se pudo cargar logo cabecera: {e}")

        self.frames = {}
        

        # Estilos
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TLabel", background="#f8f9fa", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("TCombobox", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))

        self.frames = {}
        self.mostrar_frame(FrameInicio)

    def mostrar_frame(self, frame_class):
        # Destruir frame actual
        for frame in self.frames.values():
            frame.destroy()
        self.frames.clear()

        # Crear frame nuevo
        frame = frame_class(self)
        self.frames[frame_class] = frame
        frame.pack(fill="both", expand=True, padx=20, pady=20)

# ----------------------------
# 🔹 Frame Inicio
# ----------------------------
class FrameInicio(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f8f9fa")

        header_frame = tk.Frame(self, bg="#e9ecef", height=200)
        header_frame.pack(fill="x")

         # Usar la imagen cargada desde App
        if master.logo_img_header:
            tk.Label(header_frame, image=master.logo_img_header, bg="#e9ecef").pack(pady=10)
        else:
            tk.Label(header_frame, text="(Logo no disponible)", bg="#e9ecef").pack(pady=10)


        tk.Label(header_frame, text="Generador de Recibos Boxqui", font=("Segoe UI", 16, "bold"), bg="#e9ecef").pack()

        content_frame = tk.Frame(self, bg="#f8f9fa")
        content_frame.pack(fill="both", expand=True, pady=30)

        ttk.Button(content_frame, text="📄 Generar todos los recibos",
                   command=lambda: master.mostrar_frame(FrameGenerarTodos)).pack(pady=10, fill="x")
        ttk.Button(content_frame, text="👤 Generar un recibo",
                   command=lambda: master.mostrar_frame(FrameGenerarIndividual)).pack(pady=10, fill="x")

# ----------------------------
# 🔹 Frame Generar Todos
# ----------------------------
class FrameGenerarTodos(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f8f9fa")
        tk.Label(self, text="Generar todos los recibos", font=("Segoe UI", 14, "bold"), bg="#f8f9fa").pack(pady=10)

        self.localidad_var = tk.StringVar()
        localidades = ["Hecelchakan", "Pomuch", "Santa Cruz", "Dzinup", "Poc boc"]

        ttk.Label(self, text="Municipio:").pack(anchor="w")
        ttk.Combobox(self, textvariable=self.localidad_var, values=localidades).pack(fill="x", pady=5)

        mes_actual, anio_actual = obtener_fecha_corte()
        self.mes_var = tk.StringVar(value=MESES_ES[mes_actual])
        self.anio_var = tk.StringVar(value=anio_actual)

        ttk.Label(self, text="Mes:").pack(anchor="w")
        ttk.Combobox(self, textvariable=self.mes_var, values=list(MESES_ES.values())).pack(fill="x", pady=5)

        ttk.Label(self, text="Año:").pack(anchor="w")
        tk.Spinbox(self, from_=2024, to=2030, textvariable=self.anio_var).pack(fill="x", pady=5)

        self.excel_path = None
        ttk.Button(self, text="📂 Seleccionar Excel", command=self.sel_excel).pack(pady=5, fill="x")
        self.excel_label = ttk.Label(self, text="Archivo no seleccionado", foreground="red")
        self.excel_label.pack(pady=5)

        self.status_label = ttk.Label(self, text="")
        self.status_label.pack(pady=5)

        ttk.Button(self, text="✅ Generar", command=self.run_generar).pack(pady=10, fill="x")
        ttk.Button(self, text="⬅ Volver", command=lambda: master.mostrar_frame(FrameInicio)).pack(pady=5, fill="x")

    def sel_excel(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if path:
            self.excel_path = path
            self.excel_label.config(text=f"Archivo: {os.path.basename(path)}", foreground="green")

    def run_generar(self):
        self.status_label.config(text="⏳ Generando recibos...")
        self.update_idletasks()
        try:
            mes_str = list(MESES_ES.keys())[list(MESES_ES.values()).index(self.mes_var.get())]
            
            print("localidad:", self.localidad_var.get())
            print("excel_path:", self.excel_path)
            print("mes_str:", mes_str)
            print("anio:", self.anio_var.get())
            print("fecha_corte:", f"01-{self.mes_var.get()}-{self.anio_var.get()}")

            output = generar_todos(self.localidad_var.get(), self.excel_path, mes_str, self.anio_var.get(),
                                   f"01-{self.mes_var.get()}-{self.anio_var.get()}")
            self.status_label.config(text="✅ Proceso completado")
            messagebox.showinfo("Éxito", f"Recibos en:\n{output}")
        except Exception as e:
            self.status_label.config(text="❌ Error")
            messagebox.showerror("Error", str(e))

# ----------------------------
# 🔹 Frame Generar Individual
# ----------------------------
class FrameGenerarIndividual(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f8f9fa")
        tk.Label(self, text="Generar un recibo individual", font=("Segoe UI", 14, "bold"), bg="#f8f9fa").pack(pady=10)

        self.localidad_var = tk.StringVar()
        localidades = ["Hecelchakan", "Pomuch", "Santa Cruz", "Dzinup", "Poc boc"]

        ttk.Label(self, text="Municipio:").pack(anchor="w")
        ttk.Combobox(self, textvariable=self.localidad_var, values=localidades).pack(fill="x", pady=5)

        mes_actual, anio_actual = obtener_fecha_corte()
        self.mes_var = tk.StringVar(value=MESES_ES[mes_actual])
        self.anio_var = tk.StringVar(value=anio_actual)

        ttk.Label(self, text="Mes:").pack(anchor="w")
        ttk.Combobox(self, textvariable=self.mes_var, values=list(MESES_ES.values())).pack(fill="x", pady=5)

        ttk.Label(self, text="Año:").pack(anchor="w")
        tk.Spinbox(self, from_=2024, to=2030, textvariable=self.anio_var).pack(fill="x", pady=5)

        ttk.Label(self, text="NO de Cliente:").pack(anchor="w")
        self.cliente_no_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.cliente_no_var).pack(fill="x", pady=5)

        self.excel_path = None
        ttk.Button(self, text="📂 Seleccionar Excel", command=self.sel_excel).pack(pady=5, fill="x")
        self.excel_label = ttk.Label(self, text="Archivo no seleccionado", foreground="red")
        self.excel_label.pack(pady=5)

        self.status_label = ttk.Label(self, text="")
        self.status_label.pack(pady=5)

        ttk.Button(self, text="✅ Generar", command=self.run_generar).pack(pady=10, fill="x")
        ttk.Button(self, text="⬅ Volver", command=lambda: master.mostrar_frame(FrameInicio)).pack(pady=5, fill="x")

    def sel_excel(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if path:
            self.excel_path = path
            self.excel_label.config(text=f"Archivo: {os.path.basename(path)}", foreground="green")

    def run_generar(self):
        self.status_label.config(text="⏳ Generando recibo...")
        self.update_idletasks()
        try:
            mes_str = list(MESES_ES.keys())[list(MESES_ES.values()).index(self.mes_var.get())]
            output = generar_individual(self.localidad_var.get(), self.excel_path, mes_str, self.anio_var.get(),
                                        f"01-{self.mes_var.get()}-{self.anio_var.get()}", self.cliente_no_var.get())
            self.status_label.config(text="✅ Proceso completado")
            messagebox.showinfo("Éxito", f"Recibo en:\n{output}")
        except Exception as e:
            self.status_label.config(text="❌ Error")
            messagebox.showerror("Error", str(e))

# ----------------------------
# 🔹 Lanzar splash y app
# ----------------------------
if __name__ == "__main__":
    app = App()
    #app.withdraw()  # Ocultar ventana principal mientras aparece splash

    splash = SplashScreen(app)

    def mostrar_app():
        splash.destroy()   # Cerrar splash
        app.deiconify()    # Mostrar ventana principal ya cargada

    app.after(2000, mostrar_app)
    app.mainloop()

