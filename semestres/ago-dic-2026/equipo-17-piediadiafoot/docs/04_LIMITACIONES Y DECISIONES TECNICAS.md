# DiaFoot — Registro de limitaciones y decisiones técnicas

**Propósito:** dejar constancia transparente de las condiciones conocidas del prototipo y de las decisiones tomadas durante la integración. Este registro no sustituye pruebas, calibraciones ni validaciones clínicas.

## 1. Limitaciones conocidas

| Área | Limitación / condición | Cómo debe comunicarse |
|---|---|---|
| Sensor de temperatura | La lectura no quedó validada/calibrada de forma suficiente. Durante la integración se retiró la condición que impedía continuar cuando la lectura térmica no estaba disponible o validada. | No presentar la temperatura como medición clínica calibrada. Indicar que requiere calibración y validación antes de usarla como referencia cuantitativa. |
| Cámara | La WROVER entrega fotogramas al software de visión mediante HTTP `/frame`. No debe afirmarse que el movimiento motorizado de la cámara mediante pulsos de teclado quedó operativo si no existe una prueba verificable de esa función en la versión entregada. | Describir la cámara como módulo de adquisición de imagen en la posición de operación comprobada. Aclarar el control de posición únicamente si se ha verificado. |
| YOLO | El modelo realiza detecciones experimentales sensibles a iluminación, enfoque, encuadre, datos de entrenamiento y umbral de confianza. | Las detecciones son apoyo experimental, no diagnóstico ni clasificación médica validada. |
| Nube | Firestore y Supabase requieren credenciales propias de cada instalación. Esas credenciales no forman parte del paquete. | Explicar que la persistencia/consulta cloud requiere configuración local de Firebase y Supabase. |
| Red | MQTT, HTTP de cámara y API local dependen de IP, puertos, firewall y conectividad de la red donde se instale. | Las direcciones IP del equipo de desarrollo deben reemplazarse por las de la red destino. |
| Reproducción | El paquete no incluye credenciales ni evidencia de una instalación limpia en una segunda computadora. | No afirmar que la instalación en cualquier equipo está certificada; ejecutar y registrar la lista de verificación del manual. |

## 2. Decisiones técnicas documentadas

1. **Separación de responsabilidades:** la DevKit se encarga de sensores/actuadores; la WROVER se dedica a cámara; la laptop integra visión artificial, MQTT, API y Dashboard.
2. **Transporte de imagen:** se conserva HTTP `/frame` con RGB565 para la cámara, y se convierte el fotograma en la laptop antes de procesarlo con OpenCV/YOLO.
3. **Mensajería:** se conserva MQTT mediante Mosquitto y los tópicos `proyecto/...` declarados en la configuración.
4. **Interfaz:** se conserva Streamlit para el Dashboard y FastAPI/Uvicorn para la API local consumida por el Dashboard.
5. **Persistencia dividida:** Firestore se utiliza para datos estructurados/metadatos y Supabase Storage para archivos de imagen.
6. **Credenciales fuera del repositorio:** se incluye `.env.example`, no el `.env` con secretos. Las contraseñas de configuración se sustituyen por marcadores.
7. **Modelo incluido:** se incorpora `best.pt` en `laptop/` y la configuración referencia ese nombre de archivo.
8. **Privacidad:** no se incluyen capturas clínicas ni datos identificables de pacientes en el paquete.

## 3. Alcance de las afirmaciones de entrega

El equipo informó que el prototipo físico fue entregado funcionando y que el Dashboard estaba operativo al momento de la entrega. Esta documentación registra ese antecedente como información proporcionada por el equipo; no representa una nueva prueba independiente del hardware ni de los servicios externos.

## 4. Mejoras futuras recomendadas

- Calibrar el sensor térmico con un procedimiento repetible y registrar error/incertidumbre.
- Validar el modelo YOLO con un conjunto de imágenes representativo y documentar métricas.
- Verificar y documentar el control de posición de cámara si se desea incluir como función.
- Añadir pruebas automatizadas para conversión RGB565, comunicación MQTT, API y persistencia.
- Registrar versiones exactas de Python y dependencias en una instalación reproducible.
- Incorporar diagramas eléctricos finales y evidencia fotográfica no identificable.
- Definir políticas de acceso, retención y eliminación para datos e imágenes de pacientes.

## 5. Nota de seguridad

Antes de operar actuadores, comprobar conexiones, fuente de alimentación, relevadores y mecanismo de paro físico. La parada por software no sustituye un corte físico de energía. El prototipo no debe utilizarse para decisiones clínicas ni para sustituir la supervisión de personal competente.
