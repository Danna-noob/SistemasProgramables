# DiaFoot — Manual de instalación y ejecución

## 1. Requisitos

- Computadora con Windows (los comandos de ejemplo usan PowerShell) y conexión a la red Wi-Fi local.
- Python instalado. Se recomienda usar una versión compatible con las versiones vigentes de `ultralytics`, `opencv-python`, `paho-mqtt`, `streamlit` y Firebase/Supabase; validar en el equipo de destino.
- Thonny u otra herramienta compatible con MicroPython para cargar firmware en las ESP32.
- ESP32 DevKit, ESP32-WROVER con cámara y hardware periférico.
- Broker Mosquitto instalado y configurado.
- Acceso al Wi-Fi de 2.4 GHz para las placas.
- Credenciales locales de MQTT y, para las funciones cloud, Firebase y Supabase.

> El paquete no contiene credenciales reales ni un archivo `.env`. Tampoco se garantiza que las versiones de software instaladas en otra computadora sean idénticas a las usadas durante el desarrollo.

## 2. Preparar el proyecto en la computadora

1. Extraer `DIAFOOT_ENTREGA_CONSOLIDADA.zip` en una carpeta de trabajo, por ejemplo `C:\\DiaFoot`.
2. Abrir PowerShell y entrar a la carpeta `DIAFOOT_PROYECTO\\laptop`.
3. Crear y activar un entorno virtual:

```powershell
py -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

Si PowerShell bloquea la activación, consultar la política local de ejecución o activar el entorno desde CMD con `.venv\\Scripts\\activate.bat`.

4. Actualizar pip e instalar dependencias:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

La primera instalación de Ultralytics/OpenCV puede tardar y requiere conexión a internet.

## 3. Configurar los archivos

### 3.1 `laptop/.env`

Desde la carpeta `laptop`, copiar la plantilla:

```powershell
Copy-Item .env.example .env
```

Completar las variables de Firebase y Supabase siguiendo `03_MANUAL_FIREBASE_SUPABASE.md`. No enviar ni incluir el `.env` en el ZIP de entrega.

### 3.2 `laptop/config_ia.json`

Editar al menos:

- `mqtt_host`: dirección IP de la computadora donde corre Mosquitto.
- `mqtt_port`: normalmente `1883`, si se conserva la configuración del broker.
- `mqtt_user`: `vision_user` si se mantiene la ACL incluida.
- `mqtt_password`: contraseña local de ese usuario.
- `camera_stream_url`: `http://IP_DE_LA_WROVER/frame`.
- `model_path`: `best.pt` si el modelo permanece junto a `vision_mqtt.py`.
- `camera_width` y `camera_height`: `320` y `240` para QVGA.

La aplicación carga `config_ia.json` desde la misma carpeta del script. Mantener la ruta relativa `best.pt` evita depender de una ruta de otra computadora.

### 3.3 `esp32_devkit/config.json`

Antes de cargarlo a la placa, completar:

- `wifi_ssid` y `wifi_password`.
- `mqtt_host` con la IP de la computadora que ejecuta Mosquitto.
- `mqtt_port`.
- `mqtt_user` y `mqtt_password` para `esp32_user`.

Las claves de MQTT deben coincidir con las creadas en el broker. No basta con editar el archivo en la computadora: hay que volver a cargarlo a la DevKit.

### 3.4 `wrover/main.py`

Editar `ssid` y `password` dentro del firmware con la red Wi-Fi de 2.4 GHz. Cargarlo a la raíz de la WROVER como `/main.py`.

## 4. Configurar y arrancar Mosquitto

1. Instalar Mosquitto en la computadora que actuará como broker.
2. Configurar usuarios y contraseñas localmente. La ACL de referencia utiliza `esp32_user` y `vision_user`; las contraseñas deben crearse mediante las herramientas de Mosquitto y no escribirse en la ACL.
3. Revisar `mosquitto/mosquitto.conf` y `mosquitto/aclfile`. Copiarlos a las rutas de configuración reales solo después de adaptar las rutas de archivos de contraseña/ACL a la instalación.
4. Iniciar el servicio Mosquitto.
5. Confirmar que el broker escucha en el puerto TCP 1883 y que el firewall permite conexiones desde las placas en la red local.

No reemplazar la configuración de un broker existente sin respaldarla. La instalación del servicio y la creación de usuarios dependen del sistema operativo.

## 5. Cargar y probar las placas

### WROVER (primero)

1. Conectar la WROVER por USB y seleccionar el puerto correcto en Thonny.
2. Cargar `wrover/main.py` como `/main.py`.
3. Reiniciar la placa.
4. Revisar la consola: debe mostrar la IP asignada y el mensaje de servidor HTTP listo.
5. Desde un navegador de la misma red abrir `http://IP_DE_LA_WROVER/`.
6. Comprobar el fotograma en `http://IP_DE_LA_WROVER/frame`.

### DevKit

1. Cargar a la raíz de la DevKit `esp32_devkit/main.py`, `mqtt_client.py`, `lcd1602.py`, `ssd1306.py` y `config.json`.
2. Reiniciar.
3. Revisar que conecte al Wi-Fi y que la consola indique conexión MQTT.
4. Confirmar que LCD/OLED y sensores respondan según el montaje.

No cargar el `main.py` de la WROVER en la DevKit ni viceversa.

## 6. Orden de ejecución en la laptop

Abrir dos terminales en `laptop` y activar el mismo entorno virtual en ambas.

**Terminal 1 — Visión, YOLO, MQTT y API local:**

```powershell
python vision_mqtt.py
```

Esperar mensajes de carga del modelo, conexión MQTT y disponibilidad de la API en `http://127.0.0.1:8000`. Los mensajes de Firebase/Supabase informan si esos servicios pudieron inicializarse.

**Terminal 2 — Dashboard:**

```powershell
streamlit run dashboard.py
```

Abrir la dirección local que indique Streamlit, normalmente `http://localhost:8501`.

Mantener abierta la terminal de `vision_mqtt.py` mientras se use el Dashboard: el Dashboard consulta la API local de ese proceso.

## 7. Lista de verificación

- [ ] WROVER conectada al Wi-Fi.
- [ ] `http://IP_WROVER/` muestra la cámara.
- [ ] `http://IP_WROVER/frame` responde con fotograma.
- [ ] Mosquitto activo en la IP/puerto configurados.
- [ ] DevKit conectada a MQTT.
- [ ] `vision_mqtt.py` carga `best.pt`.
- [ ] Se reciben fotogramas y se ejecuta YOLO.
- [ ] Dashboard abre en Streamlit.
- [ ] API local responde en `127.0.0.1:8000`.
- [ ] Firebase y Supabase conectan si se habilitaron las credenciales.
- [ ] Se realiza una prueba controlada de captura/sesión con datos autorizados.

## 8. Solución de problemas

| Síntoma | Revisar |
|---|---|
| No se encuentra `best.pt` | Ejecutar desde la carpeta `laptop`; confirmar que `model_path` apunta al archivo correcto. |
| Error MQTT / no conecta | IP del broker, puerto, firewall, servicio activo, usuario y contraseña en ambos clientes. |
| Cámara no responde | IP mostrada por WROVER, Wi-Fi de 2.4 GHz, alimentación y ruta `/frame`. |
| Dashboard no conecta con Vision | Mantener `vision_mqtt.py` abierto; verificar que API local use puerto 8000 y que no esté ocupado. |
| Firestore no inicializa | Revisar ruta del JSON de cuenta de servicio, permisos y proyecto. |
| Supabase no inicializa o no sube fotos | Revisar URL, clave, nombre del bucket y políticas/permisos de Storage. |
| Imagen incorrecta o detección inestable | Iluminación, enfoque/posición, formato RGB565, dimensiones y umbral de confianza. |

## 9. Seguridad durante pruebas

Antes de accionar motores, relés o mecanismos, verificar el cableado, la fuente, el sentido de movimiento y el paro físico. No depender únicamente de un comando de parada por software. Mantener manos y objetos fuera de partes móviles durante las pruebas.
