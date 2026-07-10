"""
============================================================
DCSH01 - Evaluacion Sumativa 3
Sistema IoT con Actuacion Real - Backend Flask
============================================================
Rol de este backend:
  - Enviar comandos HTTP al ESP32 para encender/apagar LEDs.
  - Registrar cada evento (con fecha y hora) en Supabase.
  - Mostrar un monitor estilo terminal con el estado del sistema.

Backend: solo Python (Flask). No se usa JavaScript.
CSS: solo selectores por id (sin clases).
============================================================
"""

import os
import requests
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ---------------- CONFIGURACION ----------------
# IP local del ESP32 en tu red (revisa el monitor serial al conectarlo)
ESP32_IP = os.environ.get("ESP32_IP", "192.168.1.50")

# Datos de conexion a Supabase (usa variables de entorno, no las dejes
# escritas directamente aqui para no subir credenciales al repositorio)
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://TU_PROYECTO.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "TU_API_KEY_DE_SUPABASE")
SUPABASE_TABLE = "eventos"

LEDS_VALIDOS = ["rojo", "amarillo", "verde"]

# Historial en memoria para mostrar en el monitor sin depender de JS
historial = []


def registrar_evento(led, estado, origen="flask"):
    """Guarda el evento en Supabase y en el historial local."""
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    evento = {
        "dispositivo": "ESP32-1",
        "led": led,
        "estado": estado,
        "timestamp": ahora,
    }
    historial.insert(0, evento)
    if len(historial) > 30:
        historial.pop()

    # Insercion en Supabase via API REST
    try:
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "dispositivo": "ESP32-1",
            "led": led,
            "estado": estado,
        }
        requests.post(
            f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
            json=payload,
            headers=headers,
            timeout=3,
        )
    except requests.exceptions.RequestException as error:
        print(f"[AVISO] No se pudo registrar en Supabase: {error}")


def enviar_comando_esp32(led, estado):
    """Envia el comando HTTP al ESP32 para cambiar el estado del LED."""
    try:
        url = f"http://{ESP32_IP}/led"
        respuesta = requests.get(
            url, params={"color": led, "estado": estado}, timeout=3
        )
        return respuesta.ok
    except requests.exceptions.RequestException as error:
        print(f"[ERROR] No se pudo contactar al ESP32: {error}")
        return False


# ---------------- RUTAS ----------------

@app.route("/")
def index():
    """Panel principal con botones para activar cada LED."""
    return render_template("index.html", leds=LEDS_VALIDOS)


@app.route("/activar", methods=["POST"])
def activar():
    """Recibe la activacion desde el formulario Flask (sin JS)."""
    led = request.form.get("led")
    estado = request.form.get("estado")

    if led in LEDS_VALIDOS and estado in ["on", "off"]:
        exito = enviar_comando_esp32(led, estado)
        registrar_evento(led, estado, origen="flask")
        if not exito:
            print(f"[AVISO] Comando enviado pero el ESP32 no respondio bien.")

    return redirect(url_for("monitor"))


@app.route("/monitor")
def monitor():
    """Monitor estilo terminal: muestra el estado del sistema."""
    return render_template("monitor.html", eventos=historial)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
