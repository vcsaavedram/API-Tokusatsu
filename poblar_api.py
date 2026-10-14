import requests

# 1. Configuración y Credenciales
USERNAME = "Admin"
PASSWORD = "L0l0pal0l0"  # <-- Tu contraseña ya está puesta aquí
BASE_URL = "http://127.0.0.1:8000"

print("--- Iniciando Automatización de Poblado (Tokusatsu API) ---")

# 2. Obtener Token JWT
respuesta_token = requests.post(f"{BASE_URL}/api/token/", data={
    "username": USERNAME,
    "password": PASSWORD
})

if respuesta_token.status_code != 200:
    print("[ERROR] Credenciales inválidas.")
    exit()

access_token = respuesta_token.json().get("access")
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
print("[OK] Token JWT generado correctamente.\n")

# 3. Funciones Inteligentes
def obtener_o_crear_franquicia(datos):
    url = f"{BASE_URL}/api/v1/franchises/"
    res_post = requests.post(url, json=datos, headers=headers)
    
    if res_post.status_code == 201:
        print(f" [+] Franquicia creada: {datos['name']}")
        return res_post.json()['id']
    
    res_get = requests.get(url, headers=headers)
    data = res_get.json()
    lista_franquicias = data.get('results', data) 
    
    for f in lista_franquicias:
        if f['name'] == datos['name']:
            print(f" [*] Franquicia ya existía: {datos['name']}")
            return f['id']
    return None

def obtener_o_crear_serie(datos):
    url = f"{BASE_URL}/api/v1/series/"
    res_post = requests.post(url, json=datos, headers=headers)
    
    if res_post.status_code == 201:
        tipo = "Spin-off" if datos.get('base_series') else "Principal"
        print(f" [+] Serie {tipo} creada: {datos['title']}")
        return res_post.json()['id']
    
    res_get = requests.get(url, headers=headers)
    data = res_get.json()
    lista_series = data.get('results', data)
    
    for s in lista_series:
        if s['title'] == datos['title']:
            print(f" [*] Serie ya existía: {datos['title']}")
            return s['id']
            
    # ---> AQUÍ ESTÁ EL DETECTIVE QUE NOS FALTABA <---
    print(f" [!] Error al intentar crear '{datos['title']}': {res_post.text}")
    return None

# 4. Inyección de Datos
print(">>> Procesando Franquicias...")
id_kr = obtener_o_crear_franquicia({
    "name": "Kamen Rider",
    "production_company": "Toei Company",
    "creation_year": 1971
})

id_sentai = obtener_o_crear_franquicia({
    "name": "Super Sentai",
    "production_company": "Toei Company",
    "creation_year": 1975
})

print("\n>>> Procesando Series Principales...")
id_zero_one = obtener_o_crear_serie({
    "franchise": id_kr,
    "title": "Kamen Rider Zero-One",
    "platform": "TV",
    "release_year": 2019,
    "episode_count": 45,
    "theme": "Inteligencia Artificial",
    "is_airing": False
})

obtener_o_crear_serie({
    "franchise": id_sentai,
    "title": "Tensou Sentai Goseiger",
    "platform": "TV",
    "release_year": 2010,
    "episode_count": 50,
    "theme": "Ángeles / Magia",
    "is_airing": False
})

print("\n>>> Procesando Spin-offs (Demostración de relación recursiva)...")
if id_zero_one:
    obtener_o_crear_serie({
        "franchise": id_kr,
        "base_series": id_zero_one,
        "title": "Project Thouser",
        "platform": "OTHER",           
        "release_year": 2020,
        "episode_count": 2,            
        "theme": "Creación de Thouser", 
        "is_airing": False
    })

print("\n--- ¡Proceso finalizado! ---")