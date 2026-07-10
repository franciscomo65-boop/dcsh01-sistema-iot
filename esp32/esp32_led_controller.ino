/*
  ============================================================
  DCSH01 - Evaluacion Sumativa 3
  Sistema IoT con Actuacion Real - Codigo ESP32
  ============================================================
  Rol de esta tarjeta: Recibe comandos HTTP desde el backend
  Flask y enciende/apaga 3 LEDs (rojo, amarillo, verde) que
  representan distintos estados del sistema.

  Protocolo usado: HTTP (servidor web embebido en el ESP32)
  ============================================================
*/

#include <WiFi.h>
#include <WebServer.h>

// ---------------- CONFIGURACION WIFI ----------------
// Cambia esto por los datos de tu red
const char* ssid     = "NOMBRE_DE_TU_WIFI";
const char* password = "CONTRASENA_DE_TU_WIFI";

// ---------------- PINES DE LOS LEDS ----------------
// Ajusta estos numeros segun como conectaste tus LEDs
// en la protoboard (revisa tu propio cableado)
const int LED_ROJO    = 4;
const int LED_AMARILLO = 5;
const int LED_VERDE   = 18;

WebServer server(80);

// Guarda el ultimo estado de cada LED para poder consultarlo
String estadoRojo    = "off";
String estadoAmarillo = "off";
String estadoVerde   = "off";

// ---------------- FUNCIONES AUXILIARES ----------------
void aplicarEstado(String color, String estado) {
  int pin;
  if (color == "rojo") {
    pin = LED_ROJO;
    estadoRojo = estado;
  } else if (color == "amarillo") {
    pin = LED_AMARILLO;
    estadoAmarillo = estado;
  } else if (color == "verde") {
    pin = LED_VERDE;
    estadoVerde = estado;
  } else {
    return;
  }

  digitalWrite(pin, estado == "on" ? HIGH : LOW);
}

// ---------------- ENDPOINT: /led ----------------
// Ejemplo de uso: http://IP_ESP32/led?color=rojo&estado=on
void manejarLed() {
  if (!server.hasArg("color") || !server.hasArg("estado")) {
    server.send(400, "application/json", "{\"error\":\"faltan parametros color o estado\"}");
    return;
  }

  String color  = server.arg("color");
  String estado = server.arg("estado");

  aplicarEstado(color, estado);

  String respuesta = "{\"color\":\"" + color + "\",\"estado\":\"" + estado + "\"}";
  server.send(200, "application/json", respuesta);
}

// ---------------- ENDPOINT: /estado ----------------
// Devuelve el estado actual de los 3 LEDs en formato JSON
void manejarEstado() {
  String json = "{";
  json += "\"rojo\":\"" + estadoRojo + "\",";
  json += "\"amarillo\":\"" + estadoAmarillo + "\",";
  json += "\"verde\":\"" + estadoVerde + "\"";
  json += "}";
  server.send(200, "application/json", json);
}

// ---------------- SETUP ----------------
void setup() {
  Serial.begin(115200);

  pinMode(LED_ROJO, OUTPUT);
  pinMode(LED_AMARILLO, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);

  digitalWrite(LED_ROJO, LOW);
  digitalWrite(LED_AMARILLO, LOW);
  digitalWrite(LED_VERDE, LOW);

  // Conexion WiFi
  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Conectado. IP del ESP32: ");
  Serial.println(WiFi.localIP());

  // Rutas del servidor
  server.on("/led", manejarLed);
  server.on("/estado", manejarEstado);

  server.begin();
  Serial.println("Servidor HTTP iniciado.");
}

// ---------------- LOOP ----------------
void loop() {
  server.handleClient();
}
