# DiaFoot — Manual de configuración de Firebase y Supabase

Este manual explica la configuración que debe realizar el responsable del proyecto en sus propias cuentas. **No es necesario completar estos pasos para entregar el código y la documentación**; sí son necesarios para habilitar la persistencia en la nube en otra instalación.

## 1. Qué servicio usa cada cosa

- **Firebase Cloud Firestore:** registros estructurados de pacientes, sesiones y metadatos que el código guarda/consulta.
- **Supabase Storage:** almacenamiento de fotografías originales y fotografías procesadas/anotadas.

El código de `dashboard.py` y `vision_mqtt.py` lee los datos privados desde `laptop/.env`. La inicialización cloud está protegida con manejo de errores, por lo que una falta de credenciales se informa en la interfaz/consola; las funciones que dependen de la nube no estarán disponibles.

## 2. Preparar el archivo `.env`

Desde la carpeta `laptop`:

```powershell
Copy-Item .env.example .env
```

La plantilla contiene:

```dotenv
SUPABASE_URL=
SUPABASE_SECRET_KEY=
SUPABASE_BUCKET=
FIREBASE_CREDENTIALS=RUTA_LOCAL_AL_JSON_DE_CUENTA_DE_SERVICIO
```

Completar los valores localmente. No usar comillas salvo que la herramienta/valor lo requiera. No compartir el archivo.

## 3. Firebase / Cloud Firestore

### 3.1 Requisitos

- Acceso al proyecto Firebase usado por DiaFoot.
- Permisos suficientes para consultar la configuración del proyecto y obtener una credencial de servidor autorizada.
- Cloud Firestore habilitado en el proyecto.

El código incluido inicializa Firebase Admin SDK con el identificador de proyecto `vision-dia-foot`. Si el proyecto real tiene otro identificador, no cambiarlo a ciegas: el responsable debe confirmar el ID y adaptar el código/configuración de manera consistente.

### 3.2 Obtener credencial de servidor

1. Entrar a Firebase Console con una cuenta autorizada.
2. Seleccionar el proyecto correcto.
3. Abrir la configuración del proyecto y la sección **Cuentas de servicio**.
4. Seguir el procedimiento institucional para generar/obtener una clave privada JSON de una cuenta de servicio. Si la organización prohíbe crear claves privadas, pedir al administrador una alternativa segura.
5. Guardar el archivo JSON en una ubicación local protegida, fuera de carpetas públicas o sincronizadas.
6. En `FIREBASE_CREDENTIALS`, escribir la ruta absoluta al JSON. Ejemplo ilustrativo de Windows:

```dotenv
FIREBASE_CREDENTIALS=C:\DiaFoot\credenciales\firebase-service-account.json
```

7. Verificar que la cuenta de servicio tenga únicamente los permisos mínimos necesarios para acceder a Firestore.

**Importante:** la contraseña personal de Google no es esta credencial. No enviar el JSON por correo/chat, no subirlo a GitHub y no incluirlo en el ZIP.

## 4. Supabase Storage

### 4.1 Requisitos

- Acceso al proyecto Supabase que contiene el almacenamiento de DiaFoot.
- URL del proyecto.
- Clave de servidor autorizada para el entorno local.
- Bucket existente y permisos/políticas compatibles con las operaciones de carga y lectura que utiliza la aplicación.

### 4.2 Configurar variables

1. Entrar al panel de Supabase y seleccionar el proyecto correcto.
2. Obtener la URL del proyecto y la clave de servidor de acuerdo con las políticas vigentes de Supabase y de la institución.
3. Confirmar el nombre exacto del bucket. El código usa `capturas-dia-foot` como valor predeterminado si `SUPABASE_BUCKET` no está definido.
4. Completar en `laptop/.env`:

```dotenv
SUPABASE_URL=URL_DEL_PROYECTO
SUPABASE_SECRET_KEY=CLAVE_PRIVADA_DE_SERVIDOR
SUPABASE_BUCKET=capturas-dia-foot
```

5. Comprobar que el bucket exista y que la clave utilizada pueda realizar las operaciones requeridas.

No colocar una clave `service_role` o equivalente en una aplicación pública, navegador o repositorio. En este proyecto se usa desde Python en la laptop, que debe considerarse un entorno de confianza.

## 5. Prueba de conexión

1. Guardar `.env`.
2. Cerrar y volver a ejecutar `vision_mqtt.py` y `dashboard.py` para que lean las variables.
3. Revisar la consola de Vision y los avisos del Dashboard.
4. Realizar una prueba con un paciente/dato ficticio y una imagen de prueba autorizada.
5. Confirmar en Firestore que se registró el documento esperado y en Storage que se subieron los archivos esperados.
6. Eliminar los datos de prueba cuando corresponda.

## 6. Errores frecuentes

- **FIREBASE_CREDENTIALS no existe:** la ruta en `.env` está vacía o apunta a un archivo inexistente.
- **Permiso denegado en Firestore:** revisar proyecto, identidad de servicio y roles mínimos.
- **Proyecto equivocado:** confirmar que el ID sea `vision-dia-foot` o adaptar el código tras validarlo.
- **Supabase no inicializa:** revisar URL y clave.
- **Bucket no encontrado:** revisar el nombre exacto y que el bucket esté creado.
- **Carga rechazada:** revisar políticas/permisos de Storage y límites aplicables.

## 7. Qué se entrega y qué no

Se entrega `.env.example`, el código que consume las variables y este procedimiento. No se entrega el `.env` real, la clave privada JSON de Firebase, claves de Supabase ni contraseñas de cuentas. Cada instalación debe obtener sus credenciales de forma autorizada.
