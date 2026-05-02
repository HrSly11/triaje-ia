import requests

API_URL = "http://localhost:5000/api"

print("=" * 50)
print("PRUEBA 1: Login")
print("=" * 50)
response = requests.post(f"{API_URL}/auth/login", json={
    "nombre_usuario": "admin",
    "contrasena": "admin123"
}, timeout=10)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
print()

print("=" * 50)
print("PRUEBA 2: Dashboard Operacional HOY")
print("=" * 50)
response = requests.get(f"{API_URL}/dashboard/operacional?fecha=2026-05-02", timeout=10)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
print()

print("=" * 50)
print("PRUEBA 3: Dashboard Operacional MAÑANA")
print("=" * 50)
response = requests.get(f"{API_URL}/dashboard/operacional?fecha=2026-05-03", timeout=10)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
print()

print("=" * 50)
print("PRUEBA 4: Lista de Triajes")
print("=" * 50)
response = requests.get(f"{API_URL}/triajes/lista?fecha_desde=2026-05-02&fecha_hasta=2026-05-04", timeout=10)
print(f"Status: {response.status_code}")
data = response.json()
print(f"Total triajes: {data.get('total', 0)}")
for t in data.get('triajes', [])[:5]:
    print(f"  - {t.get('fecha_hora')} | {t.get('paciente_nombre')} | {t.get('nivel_urgencia')}")