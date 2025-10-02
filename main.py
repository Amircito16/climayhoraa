import requests
from customtkinter import *
from tkinter import messagebox

# Interfaz
app = CTk()
app.title("Obtener datos")
app.resizable(width=False, height=False)


def obtener_dato_gato():
    url = "https://catfact.ninja/fact"
    response = requests.get(url)
    data = response.json()
    return f"Dato curioso sobre gatos:\n{data.get('fact', 'No se encontró el dato')}"


def obtener_consejo():
    url = "https://api.adviceslip.com/advice"
    response = requests.get(url)
    data = response.json()
    return f"Consejo:\n{data['slip']['advice']}"


def obtener_clima_actual(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Python script)",
        "Accept": "application/json"
    }
    res = requests.get(url, headers=headers)
    datos = res.json()
    clima_actual = datos.get("current_weather", {})

    descripcion_clima = {
        0: "Soleado / Despejado", 1: "Mayormente despejado", 2: "Parcialmente nublado", 3: "Nublado",
        45: "Niebla", 48: "Niebla con escarcha", 51: "Llovizna ligera", 53: "Llovizna moderada",
        55: "Llovizna intensa", 56: "Llovizna helada ligera", 57: "Llovizna helada intensa",
        61: "Lluvia ligera", 63: "Lluvia moderada", 65: "Lluvia fuerte", 66: "Lluvia helada ligera",
        67: "Lluvia helada fuerte", 71: "Nevada ligera", 73: "Nevada moderada", 75: "Nevada intensa",
        77: "Granizo", 80: "Chubascos ligeros", 81: "Chubascos moderados", 82: "Chubascos fuertes",
        85: "Chubascos de nieve ligeros", 86: "Chubascos de nieve fuertes", 95: "Tormenta eléctrica",
        96: "Tormenta con granizo leve", 99: "Tormenta con granizo fuerte"
    }

    codigo_clima = clima_actual.get("weathercode")
    descripcion = descripcion_clima.get(codigo_clima, "Desconocido")

    return {
        "latitud": lat,
        "longitud": lon,
        "temperatura": clima_actual.get("temperature"),
        "velocidad_viento": clima_actual.get("windspeed"),
        "direccion_viento": clima_actual.get("winddirection"),
        "hora_reporte": clima_actual.get("time"),
        "es_de_dia": clima_actual.get("is_day") == 1,
        "descripcion_clima": descripcion
    }


# Funciones para mostrar mensajes
def mostrard():
    messagebox.showinfo("Dato curioso", obtener_dato_gato())


def mostrarc():
    messagebox.showinfo("Consejo", obtener_consejo())


# Etiquetas fijas
CTkLabel(app, text="Temperatura:", font=("ArialBlack", 20), text_color="white").grid(column=0, row=0, padx=5, pady=5)
CTkLabel(app, text="Clima:", font=("ArialBlack", 20), text_color="white").grid(column=0, row=1, padx=5, pady=5)
CTkLabel(app, text="Velocidad del viento:", font=("ArialBlack", 20), text_color="white").grid(column=0, row=2, padx=5, pady=5)
CTkLabel(app, text="Dirección del viento:", font=("ArialBlack", 20), text_color="white").grid(column=0, row=3, padx=5, pady=5)
CTkLabel(app, text="Hora del reporte:", font=("ArialBlack", 20), text_color="white").grid(column=0, row=4, padx=5, pady=5)
CTkLabel(app, text="Es de día:", font=("ArialBlack", 20), text_color="white").grid(column=0, row=5, padx=5, pady=5)

# Nueva etiqueta fija para la hora actual
CTkLabel(app, text="Hora actual:", font=("ArialBlack", 20), text_color="white").grid(column=0, row=6, padx=5, pady=5)

# Etiquetas dinámicas
label_temperatura = CTkLabel(app, text="", font=("ArialBlack", 20), text_color="#dc8165")
label_temperatura.grid(column=1, row=0, padx=5, pady=5,columnspan=5)

label_clima = CTkLabel(app, text="", font=("ArialBlack", 20), text_color="#d7d05f")
label_clima.grid(column=1, row=1, padx=5, pady=5,columnspan=5)

label_vel_viento = CTkLabel(app, text="", font=("ArialBlack", 20), text_color="#295ef5")
label_vel_viento.grid(column=1, row=2, padx=5, pady=5,columnspan=5)

label_dir_viento = CTkLabel(app, text="", font=("ArialBlack", 20), text_color="#38d6ed")
label_dir_viento.grid(column=1, row=3, padx=5, pady=5,columnspan=5)

label_hora_reporte = CTkLabel(app, text="", font=("ArialBlack", 20), text_color="gray")
label_hora_reporte.grid(column=1, row=4, padx=5, pady=5,columnspan=5)

label_es_de_dia = CTkLabel(app, text="", font=("ArialBlack", 20), text_color="#b073d0")
label_es_de_dia.grid(column=1, row=5, padx=5, pady=5,columnspan=5)

# Etiqueta dinámica para la hora
label_hora_actual = CTkLabel(app, text="", font=("ArialBlack", 20), text_color="sky blue")
label_hora_actual.grid(column=1, row=6, padx=5, pady=5,columnspan=5)

# Botones
boton1 = CTkButton(app, text="Dato sobre gatos :3", command=mostrard,fg_color="#84b990",text_color="black")
boton1.grid(column=0, row=7, padx=5, pady=15, sticky="WE")

boton2 = CTkButton(app, text="Consejo", command=mostrarc,fg_color="#84b990",text_color="black")
boton2.grid(column=1, row=7, padx=5, pady=15, sticky="WE")


# Actualización automática del clima
def actualizar_clima():
    clima = obtener_clima_actual(14.63, -90.55)
    label_temperatura.configure(text=f"{clima['temperatura']} °C")
    label_clima.configure(text=clima['descripcion_clima'])
    label_vel_viento.configure(text=f"{clima['velocidad_viento']} km/h")
    label_dir_viento.configure(text=f"{clima['direccion_viento']} °")
    label_hora_reporte.configure(text=clima['hora_reporte'])
    label_es_de_dia.configure(text="Sí" if clima['es_de_dia'] else "No")

    # Repetir cada 60,000 milisegundos (1 minuto)
    app.after(60000, actualizar_clima)


# Nueva función: actualización de la hora cada 5 segundos
def actualizar_hora():
    url = "https://timeapi.io/api/time/current/zone?timeZone=America%2FGuatemala"
    data = requests.get(url).json()

    hora = data["hour"]
    minutos = data["minute"]

    # Formato HH:MM sin segundos
    texto = f"{hora:02d}:{minutos:02d}"
    label_hora_actual.configure(text=texto)

    # Repetir cada 5 segundos
    app.after(60000, actualizar_hora)


# Primera llamada para iniciar
actualizar_clima()
actualizar_hora()

# Ejecutar la app
app.mainloop()
