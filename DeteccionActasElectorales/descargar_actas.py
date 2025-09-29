import requests
import json
import os
import base64
import time
import csv
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# ================================
# DESCARGA JSONS BASE
# ================================
BASE_URL = "https://computo.oep.org.bo/"

nacional_response = requests.get(BASE_URL + "geografiaNacional.json")
internacional_response = requests.get(BASE_URL + "geografiaExtranjero.json")

# Guardar geografiaNacional.json
if nacional_response.status_code == 200:
    with open("geografiaNacional.json", "w", encoding="utf-8") as f:
        json.dump(nacional_response.json(), f, ensure_ascii=False, indent=2)
    print("✅ geografiaNacional.json descargado")
else:
    print(f"❌ Error {nacional_response.status_code} en geografiaNacional.json")

# Guardar geografiaExtranjera.json
if internacional_response.status_code == 200:
    with open("geografiaExtranjera.json", "w", encoding="utf-8") as f:
        json.dump(internacional_response.json(), f, ensure_ascii=False, indent=2)
    print("✅ geografiaExtranjera.json descargado")
else:
    print(f"❌ Error {internacional_response.status_code} en geografiaExtranjera.json")

# ================================
# CONFIGURACIÓN GENERAL
# ================================
URL = "https://computo.oep.org.bo/api/v1/resultados/mesa"
BASE_DIR = "ACTAS"
MAX_THREADS = 8
MIN_DELAY = 0.3
MAX_DELAY = 0.7


# ================================
# FUNCIONES COMUNES
# ================================
def descargar_mesa(mesa_id, mesa_num, rec_path):
    mesa_file = os.path.join(rec_path, f"mesa_{mesa_num}_{mesa_id}.jpg")

    if os.path.exists(mesa_file):
        return mesa_num, mesa_id, mesa_file, "Ya descargado"

    try:
        resp = requests.post(URL, json={"codigoMesa": mesa_id}, timeout=15)
        if resp.status_code == 200:
            data_resp = resp.json()
            estado = "Sin ACTA"
            for adj in data_resp.get("adjunto", []):
                if adj["tipo"] == "ACTA" and adj["valor"] != "false":
                    img_data = base64.b64decode(adj["valor"])
                    with open(mesa_file, "wb") as f:
                        f.write(img_data)
                    estado = "OK"
                    break
            return mesa_num, mesa_id, mesa_file, estado
        else:
            return mesa_num, mesa_id, "", f"Error HTTP {resp.status_code}"
    except Exception as e:
        return mesa_num, mesa_id, "", f"Error {e}"


def procesar_json(json_file, log_file, extranjero=False):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(BASE_DIR, exist_ok=True)

    # Contar mesas
    def contar_mesas():
        total = 0
        if extranjero:
            for pais in data:
                for ciudad in pais.get("c", []):
                    for recinto in ciudad.get("r", []):
                        total += len(recinto.get("t", []))
        else:
            for pais in data:
                for dep in pais.get("d", []):
                    for prov in dep.get("p", []):
                        for mun in prov.get("m", []):
                            for loc in mun.get("l", []):
                                for rec in loc.get("r", []):
                                    total += len(rec.get("t", []))
        return total

    TOTAL_MESAS = contar_mesas()
    tareas = []

    # Preparar rutas y tareas
    if extranjero:
        for pais in data:
            pais_path = os.path.join(BASE_DIR, pais["n"])
            os.makedirs(pais_path, exist_ok=True)
            for ciudad in pais.get("c", []):
                ciudad_path = os.path.join(pais_path, ciudad["n"])
                os.makedirs(ciudad_path, exist_ok=True)
                for recinto in ciudad.get("r", []):
                    recinto_path = os.path.join(ciudad_path, recinto["n"])
                    os.makedirs(recinto_path, exist_ok=True)
                    for mesa in recinto.get("t", []):
                        tareas.append((mesa["i"], mesa["n"], recinto_path))
    else:
        for pais in data:
            pais_path = os.path.join(BASE_DIR, pais["n"])
            os.makedirs(pais_path, exist_ok=True)
            for dep in pais.get("d", []):
                dep_path = os.path.join(pais_path, dep["n"])
                os.makedirs(dep_path, exist_ok=True)
                for prov in dep.get("p", []):
                    prov_path = os.path.join(dep_path, prov["n"])
                    os.makedirs(prov_path, exist_ok=True)
                    for mun in prov.get("m", []):
                        mun_path = os.path.join(prov_path, mun["n"])
                        os.makedirs(mun_path, exist_ok=True)
                        for loc in mun.get("l", []):
                            loc_path = os.path.join(mun_path, loc["n"])
                            os.makedirs(loc_path, exist_ok=True)
                            for rec in loc.get("r", []):
                                rec_path = os.path.join(loc_path, rec["n"])
                                os.makedirs(rec_path, exist_ok=True)
                                for mesa in rec.get("t", []):
                                    tareas.append((mesa["i"], mesa["n"], rec_path))

    # Ejecutar descargas
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor, \
            open(log_file, "a", newline="", encoding="utf-8") as log:

        writer = csv.writer(log)
        if os.stat(log_file).st_size == 0:
            writer.writerow(["Mesa_Num", "Mesa_ID", "Ruta", "Estado"])

        futures = {executor.submit(descargar_mesa, tid, tnum, tpath): (tnum, tid)
                   for tid, tnum, tpath in tareas}

        with tqdm(total=TOTAL_MESAS, desc=f"Descargando {json_file}") as pbar:
            for fut in as_completed(futures):
                mesa_num, mesa_id, mesa_file, estado = fut.result()
                writer.writerow([mesa_num, mesa_id, mesa_file, estado])
                time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
                pbar.update(1)

    print(f"✅ Descarga finalizada ({json_file})")


# ================================
# EJECUCIÓN
# ================================
if __name__ == "__main__":
    procesar_json("geografiaNacional.json", "descargas.csv", extranjero=False)
    procesar_json("geografiaExtranjera.json", "descargas_extranjera.csv", extranjero=True)
