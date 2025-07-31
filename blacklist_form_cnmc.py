# 31/7/2025 - Script para generar una blacklist de números bloqueados
# Basado en el fichero geograficos.txt de la CNMC y los numeros más frecuentes de spam

#Requirements:
# pip install requests

import csv
import time
import zipfile
import requests
from datetime import datetime
from io import BytesIO

# --- CONFIGURACIÓN ---
URL_ZIP = "https://numeracionyoperadores.cnmc.es/bd-num.zip"
OPERADORES_OBJETIVO = [
    "AIRE NETWORKS DEL MEDITERRÁNEO, S.L.",
    "ORANGE ESPAGNE, S.A. UNIPERSONAL"
]
PROVINCIAS_EXCLUIDAS_ORANGE = {"Madrid", "Barcelona"}  # Provincias de donde se pueden recibir llamadas legítimas

# --- DESCARGAR ZIP ---
print("Descargando fichero ZIP...")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36"
}

response = requests.get(URL_ZIP, headers=headers)

if response.status_code != 200:
    raise Exception(f"Error al descargar ZIP: código {response.status_code}")

zip_data = BytesIO(response.content)

# --- EXTRAER Y LEER geograficos.txt ---
with zipfile.ZipFile(zip_data) as z:
    if "geograficos.txt" not in z.namelist():
        raise FileNotFoundError("No se encontró 'geograficos.txt' en el ZIP")
    with z.open("geograficos.txt") as f:
        lineas = f.read().decode("latin-1").splitlines()

# --- PROCESAR Y FILTRAR ---
fecha = datetime.now().strftime("%d-%m-%Y")
output_file = f"blacklist-{fecha}.csv"
timestamp_base = int(time.time() * 1000)

registros = []
id_counter = 1

for linea in lineas:
    partes = linea.strip().split("#")
    if len(partes) != 6:
        continue

    prefijo, bloque, provincia, estado, operador, _ = partes

    if operador == OPERADORES_OBJETIVO[0] or (
        operador == OPERADORES_OBJETIVO[1] and provincia not in PROVINCIAS_EXCLUIDAS_ORANGE
    ):
        numero = f"{prefijo}{bloque}"

        # Añadir con +34
        registros.append([
            id_counter,
            f"Bloque{numero}",
            f"+34{numero}**",
            timestamp_base + id_counter * 1000,
            0,
            ""
        ])
        id_counter += 1

        # Añadir sin +34
        registros.append([
            id_counter,
            f"Bloque{numero}_noCC",
            f"{numero}**",
            timestamp_base + id_counter * 1000,
            0,
            ""
        ])
        id_counter += 1

# --- GUARDAR CSV ---
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "name", "pattern", "creationTimestamp", "numberOfCalls", "lastCallTimestamp"])
    writer.writerows(registros)

print(f"Archivo generado: {output_file}")
