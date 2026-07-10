# Sistema IoT con Actuación Real y Registro en Nube

Proyecto para DCSH01 - Evaluación Sumativa 3.

## Explicación del sistema

El sistema permite encender y apagar 3 LEDs (rojo, amarillo, verde) conectados
a un ESP32, controlados desde un panel web hecho en Flask. Cada vez que se
activa o desactiva un LED, el evento queda registrado en Supabase con la
fecha y hora exacta, y también se puede ver en tiempo real en un monitor
estilo terminal dentro de la misma aplicación Flask.

Flujo del sistema:

1. El usuario entra al panel web (Flask) y presiona "Encender" o "Apagar"
   sobre alguno de los 3 LEDs.
2. Flask envía una petición HTTP al ESP32 (`/led?color=...&estado=...`).
3. El ESP32 recibe la petición y cambia el estado físico del LED
   correspondiente.
4. Flask registra el evento en Supabase (tabla `eventos`) con fecha y hora.
5. El monitor tipo terminal (`/monitor`) muestra el historial de eventos,
   actualizándose automáticamente.

## Diagrama simple

```
[ Usuario ] --clic--> [ Flask (Python) ] --HTTP GET /led--> [ ESP32 ] --> LEDs fisicos
                              |
                              v
                         [ Supabase ]
                     (registro de eventos)
                              |
                              v
                    [ Monitor tipo terminal ]
                         (dentro de Flask)
```

## Justificación del rol de cada tarjeta

- **ESP32-1**: única tarjeta del proyecto. Su rol es recibir comandos HTTP
  y actuar sobre los 3 LEDs físicos (rojo, amarillo, verde), cada uno
  representando un estado distinto del sistema.

> Si el grupo cuenta con más de una tarjeta ESP32, se recomienda asignar un
> segundo rol (por ejemplo, una tarjeta adicional que simule un sensor y
> envíe datos hacia Flask), y documentar aquí el rol de cada una,
> justificado según la cantidad de integrantes del grupo.

## Protocolo utilizado

Se utiliza **HTTP** como protocolo de conectividad entre el ESP32 y el
backend Flask, cumpliendo el requisito de usar al menos uno de los
protocolos vistos en clase (ESP-NOW, HTTP o MQTT).

## Estructura del repositorio

```
proyecto_iot/
├── esp32/
│   └── esp32_led_controller.ino   # Código del ESP32
├── flask_app/
│   ├── app.py                     # Backend Flask
│   ├── requirements.txt
│   ├── templates/
│   │   ├── index.html             # Panel de control
│   │   └── monitor.html           # Monitor estilo terminal
│   └── static/
│       └── estilos.css            # Estilos (solo selectores por id)
├── supabase_tabla.sql             # Script para crear la tabla en Supabase
└── README.md
```

## Instrucciones para ejecutar el proyecto

### 1. Cargar el código al ESP32

1. Abre `esp32/esp32_led_controller.ino` en el IDE de Arduino.
2. Cambia `ssid` y `password` por los datos de tu red WiFi.
3. Ajusta los pines `LED_ROJO`, `LED_AMARILLO`, `LED_VERDE` según tu
   cableado real en la protoboard.
4. Sube el código al ESP32 y abre el Monitor Serial (115200 baudios).
5. Anota la IP que muestra el ESP32 al conectarse (la necesitarás en el
   paso siguiente).

### 2. Configurar Supabase

1. Crea un proyecto en [supabase.com](https://supabase.com).
2. Ve al **SQL Editor** y ejecuta el contenido de `supabase_tabla.sql`.
3. Copia la **URL del proyecto** y la **API key (anon/public)** desde
   Project Settings → API.

### 3. Configurar y correr el backend Flask

```bash
cd flask_app
pip install -r requirements.txt

# En Linux/Mac
export ESP32_IP="192.168.1.50"          # IP real que anotaste del ESP32
export SUPABASE_URL="https://TU_PROYECTO.supabase.co"
export SUPABASE_KEY="TU_API_KEY_ANON"

# En Windows (PowerShell)
$env:ESP32_IP="192.168.1.50"
$env:SUPABASE_URL="https://TU_PROYECTO.supabase.co"
$env:SUPABASE_KEY="TU_API_KEY_ANON"

python app.py
```

4. Abre el navegador en `http://localhost:5000` para ver el panel de
   control, y en `http://localhost:5000/monitor` para ver el monitor
   estilo terminal.

## Cumplimiento de restricciones de la pauta

- Sin uso de JavaScript (actualización del monitor vía `meta refresh`).
- CSS usando exclusivamente selectores por `id`.
- Backend 100% en Python (Flask).
- Base de datos relacional (Supabase / PostgreSQL).
- Registro de eventos con fecha y hora exacta.
