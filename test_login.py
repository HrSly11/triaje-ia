
import requests

API_URL = "http://localhost:5000/api/auth/login"

print("Probando login en API...")
response = requests.post(API_URL, json={
    "nombre_usuario": "admin",
    "contrasena": "admin123"
}, timeout=10)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
