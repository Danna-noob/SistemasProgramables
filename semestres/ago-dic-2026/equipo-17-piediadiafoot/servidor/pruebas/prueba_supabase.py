
import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SECRET_KEY")
bucket = os.getenv("SUPABASE_BUCKET")

try:
    supabase = create_client(url, key)

    archivos = supabase.storage.from_(bucket).list()

    print("SUPABASE CONECTADO CORRECTAMENTE")
    print("Bucket:", bucket)
    print("Acceso al almacenamiento: OK")
    print("Archivos encontrados:", len(archivos))

except Exception as e:
    print("ERROR DE CONEXION:")
    print(e)
