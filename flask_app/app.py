from flask import Flask, render_template, redirect, url_for
import requests
from datetime import datetime

from supabase_client import registrar_evento

app = Flask(__name__)

ESP32_IP = "192.168.100.191"

NOMBRE_DISPOSITIVO = "ESP32-1"

log_terminal = []


def agregar_log(mensaje):
    hora = datetime.now().strftime("%H:%M:%S")
    log_terminal.append(f"[{hora}] {mensaje}")
    if len(log_terminal) > 50:
        log_terminal.pop(0)


@app.route("/")
def index():
    estado = None
    try:
        r = requests.get(f"http://{ESP32_IP}/status", timeout=3)
        estado = r.json()
    except Exception as e:
        agregar_log(f"ERROR consultando ESP32: {e}")
    return render_template("index.html", estado=estado)


@app.route("/monitor")
def monitor():
    return render_template("monitor.html", logs=log_terminal)


@app.route("/led/<nombre>/<valor>")
def led(nombre, valor):
    valor_http = "1" if valor == "on" else "0"

    try:
        requests.get(
            f"http://{ESP32_IP}/led",
            params={"nombre": nombre, "valor": valor_http},
            timeout=3,
        )
        ok = True
    except Exception as e:
        agregar_log(f"ERROR enviando comando al ESP32: {e}")
        ok = False

    mensaje = f"LED {nombre.upper()} -> {'ENCENDIDO' if valor == 'on' else 'APAGADO'}"
    if not ok:
        mensaje += " (SIN RESPUESTA DEL ESP32)"

    agregar_log(mensaje)
    registrar_evento(NOMBRE_DISPOSITIVO, mensaje)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
