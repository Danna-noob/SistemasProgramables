# Estado de verificación de seguridad — Firebase y Supabase

Este archivo distingue los hechos comprobables en el código de los elementos que requieren acceso a las consolas.

## 1. Servicio Firebase

**Confirmado por código:** Cloud Firestore, mediante `firebase_admin.firestore` y `firestore.client()`. No se encontró uso de Realtime Database en los archivos Python revisados.

## 2. Reglas publicadas de Cloud Firestore

**No están incluidas en el paquete.** No se encontró `firestore.rules`, `rules.json`, exportación de reglas ni evidencia de Firebase Console → Firestore Database → Rules.

Por tanto, no puedo compartir el contenido actualmente publicado. No se genera un `reglas.json` inventado.

Para obtener el contenido real:
1. Abrir Firebase Console y seleccionar el proyecto correcto (el código configura `vision-dia-foot`; confirmar que sea el proyecto activo).
2. Ir a Firestore Database → Rules.
3. Copiar íntegramente el contenido publicado, incluyendo `rules_version`, `service cloud.firestore` y todos los bloques `match`.
4. Guardarlo literalmente como `firebase/firestore.rules` (formato nativo). Si la entrega exige `reglas.json`, confirmar con quien la solicita si acepta el contenido nativo con extensión `.rules`; las reglas de Firestore no son JSON.

## 3. SDK y clientes que acceden a Firestore

**Confirmado por código:**
- `laptop/vision_mqtt.py` usa `firebase_admin.credentials.Certificate(...)` y `firestore.client()`.
- `laptop/dashboard.py` también inicializa Firebase Admin SDK en Python y usa `firestore.client()`.
- El Dashboard Streamlit consulta Firestore desde Python en el proceso servidor local.
- `laptop/prueba_firebase.py` también usa Firebase Admin SDK.
- No se encontró SDK web Firebase ni acceso directo a Firestore desde JavaScript en los archivos revisados.

Firebase Admin SDK opera con identidad de cuenta de servicio y sus operaciones de servidor no están sujetas a las reglas cliente de Firestore; el acceso se controla mediante IAM/permisos de la identidad de servicio. Esto no revela qué reglas están publicadas para clientes.

## 4. Operaciones y permisos funcionales observados

| Ruta | Operaciones en el código | Permiso funcional del servidor |
|---|---|---|
| `pacientes/{patient_id}` | Dashboard lista/lee y crea; backend lee por ID. | Lectura/listado y creación. |
| `sesiones/{session_id}` | Vision crea/actualiza inicio y cierre; Dashboard lista/lee. | Lectura/listado, creación y actualización. |
| `sesiones/{session_id}/capturas/{capture_id}` | Vision crea; Dashboard lista/lee. | Lectura/listado y creación. |

No se encontró una pantalla de autenticación de usuarios finales ni un flujo Firebase Authentication. El acceso de la aplicación parece depender del equipo/servidor local y de sus credenciales de servicio. Esto no permite concluir que Firestore tenga acceso público: las reglas publicadas deben revisarse directamente. No se recomienda habilitar lectura/escritura pública para estas rutas.

## 5. Supabase Storage y políticas

**Confirmado por código:** `vision_mqtt.py` y `dashboard.py` crean un cliente Supabase con `SUPABASE_URL` y `SUPABASE_SECRET_KEY`. El bucket predeterminado es `capturas-dia-foot`. Vision sube imágenes y el Dashboard descarga objetos.

**No disponible en el paquete:** políticas RLS de `storage.objects`, estado público/privado del bucket o políticas adicionales. No se encontró exportación SQL de políticas ni captura de Supabase.

Para verificar:
1. Abrir el proyecto Supabase correcto.
2. Revisar Storage → Buckets y confirmar si `capturas-dia-foot` es público o privado.
3. Revisar Database → Policies para `storage.objects`.
4. Copiar/exportar el SQL completo de las políticas aplicables y anotar fecha de revisión.
5. No incluir claves secretas en la documentación.

El uso de una clave secreta desde Python no demuestra por sí mismo que el bucket sea público. La clave debe permanecer fuera del ZIP y del control de versiones.

## 6. Evidencias pendientes

- [ ] Captura de Firestore → Data con colecciones/documentos de prueba y datos personales ocultos.
- [ ] Copia o captura de Firestore → Rules con reglas publicadas.
- [ ] Confirmación del proyecto seleccionado y fecha de revisión.
- [ ] Captura/exportación de políticas de Supabase Storage y estado público/privado del bucket.
- [ ] Prueba autorizada de lectura/escritura con datos ficticios.

No sustituir estas evidencias por reglas, capturas o documentos inventados.
