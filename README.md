# 📄 Generador de Recibos Boxqui

![Splash](screenshots_recibosBoxquiDemo/Pantalla%20Splash.png)

Aplicación de escritorio desarrollada en **Python + Tkinter** para la automatización de recibos de cobro.
Permite la generación masiva o individual de recibos, con exportación automática de listas de cobro en Excel.

---

## 🚀 Características principales

* **Generación masiva de recibos** a partir de un archivo Excel.
* **Generación individual** de recibos por cliente.
* **Exportación automática** de listas de cobro.
* **Interfaz intuitiva** con selector de localidad, mes y año.
* **Salida organizada** en carpeta `output/` por fecha y localidad.

---

## 🖼️ Capturas de pantalla

### 🔹 Pantalla de carga (Splash)

![Splash](screenshots_recibosBoxquiDemo/Pantalla%20Splash.png)

### 🔹 Menú principal

![Menú Principal](screenshots_recibosBoxquiDemo/Menu%20Principal.png)

### 🔹 Generar todos los recibos

![Generar Todos](screenshots_recibosBoxquiDemo/Menu%20Generar%20Todos.png)

### 🔹 Generar recibo individual

![Generar Individual](screenshots_recibosBoxquiDemo/Menu%20Generar%20Individual.png)

### 🔹 Mensaje de éxito

![Mensaje Éxito](screenshots_recibosBoxquiDemo/Mensaje%20de%20Exito.png)

### 🔹 Carpeta de salida

![Output](screenshots_recibosBoxquiDemo/Output%20recibos%20y%20lista%20de%20cobro.png)

---

## 📂 Estructura del proyecto

```
RecibosBoxqui_Demo/
│
├── acciones.py
├── config.py
├── datos.py
├── generador.py   (versión censurada para demo)
├── gui.py
├── helpers.py
├── main.py
│
├── assets/        (no incluye archivos reales en versión pública)
│   └── .gitkeep
├── data/          (no incluye Excel real en versión pública)
│   └── .gitkeep
├── output/        (carpeta de salida generada automáticamente)
│   └── .gitkeep
├── screenshots_recibosBoxquiDemo/   (capturas para README)
│   ├── Pantalla Splash.png
│   ├── Menu Principal.png
│   ├── Menu Generar Todos.png
│   ├── Menu Generar Individual.png
│   ├── Mensaje de Exito.png
│   └── Output recibos y lista de cobro.png
└── README.md
```

---

## ⚠️ Nota sobre versión pública

> Esta es una **versión pública para portafolio**.
>
> * No incluye `assets` ni `data` reales.
> * `generador.py` está censurado y reemplazado por una implementación de demostración.
> * La estructura y arquitectura se mantienen para evaluación técnica.

---

## 📌 Tecnologías utilizadas

* **Python 3.12**
* **Tkinter** (GUI)
* **Pandas** (manejo de Excel)
* **Pillow (PIL)** (manipulación de imágenes)
* **OpenPyXL** (lectura/escritura Excel)

---

## 🛠️ Instalación y uso

1. Clonar repositorio

```bash
git clone https://github.com/TU_USUARIO/RecibosBoxqui_Demo.git
```

2. Instalar dependencias

```bash
pip install -r requirements.txt
```

3. Ejecutar aplicación

```bash
python gui.py
```
## 🔮 Próximas mejoras

Optimización del tiempo de carga inicial en formato ejecutable.

Mejora visual de la interfaz con un diseño más moderno.

Integración opcional de base de datos para gestión de clientes.

Creación de versión web usando un framework como Streamlit o Flask.

---

## 👨‍💻 Autor

Desarrollado por **\AaronDevIMT** como herramienta interna y proyecto de portafolio.
