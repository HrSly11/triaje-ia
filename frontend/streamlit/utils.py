import streamlit as st
import requests
import json
from datetime import datetime
import hashlib
import bcrypt
import os

API_BASE_URL = os.getenv("API_URL", "http://localhost:5000") + "/api"

def get_base_url():
    return API_BASE_URL

def verificar_contrasena(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def login_usuario(nombre_usuario, contrasena):
    try:
        response = requests.post(f"{get_base_url()}/auth/login", json={
            "nombre_usuario": nombre_usuario,
            "contrasena": contrasena
        }, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

def obtener_pacientes(busqueda="", page=1, per_page=20):
    try:
        params = {"page": page, "per_page": per_page}
        if busqueda:
            params["busqueda"] = busqueda
        response = requests.get(f"{get_base_url()}/pacientes", params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"pacientes": [], "total": 0}
    except Exception as e:
        st.error(f"Error: {e}")
        return {"pacientes": [], "total": 0}

def obtener_paciente(id_paciente):
    try:
        response = requests.get(f"{get_base_url()}/pacientes/{id_paciente}", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def crear_paciente(data):
    try:
        response = requests.post(f"{get_base_url()}/pacientes", json=data, timeout=10)
        if response.status_code == 201:
            return response.json()
        return {"error": response.json().get("error", "Error desconocido")}
    except Exception as e:
        return {"error": str(e)}

def crear_triaje(data):
    try:
        response = requests.post(f"{get_base_url()}/triajes", json=data, timeout=10)
        if response.status_code == 201:
            return response.json()
        return {"error": response.json().get("error", "Error desconocido")}
    except Exception as e:
        return {"error": str(e)}

def completar_triaje(id_triaje, data):
    try:
        response = requests.put(f"{get_base_url()}/triajes/{id_triaje}/completar", json=data, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"error": response.json().get("error", "Error desconocido")}
    except Exception as e:
        return {"error": str(e)}

def obtener_triaje(id_triaje):
    try:
        response = requests.get(f"{get_base_url()}/triajes/{id_triaje}", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def listar_triajes(page=1, per_page=20, fecha_desde=None, fecha_hasta=None, nivel_urgencia=None):
    try:
        params = {"page": page, "per_page": per_page}
        if fecha_desde:
            params["fecha_desde"] = fecha_desde
        if fecha_hasta:
            params["fecha_hasta"] = fecha_hasta
        if nivel_urgencia:
            params["nivel_urgencia"] = nivel_urgencia
        response = requests.get(f"{get_base_url()}/triajes/lista", params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"triajes": [], "total": 0}
    except Exception as e:
        st.error(f"Error: {e}")
        return {"triajes": [], "total": 0}

def obtener_dashboard_operacional(fecha=None):
    try:
        params = {}
        if fecha:
            params["fecha"] = fecha
        response = requests.get(f"{get_base_url()}/dashboard/operacional", params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def obtener_dashboard_gestion(mes=None):
    try:
        params = {}
        if mes:
            params["mes"] = mes
        response = requests.get(f"{get_base_url()}/dashboard/gestion", params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def obtener_antecedentes_hce(numero_documento):
    try:
        response = requests.get(f"{get_base_url()}/hce/{numero_documento}/antecedentes", timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"antecedentes": [], "historial": []}
    except Exception:
        return {"antecedentes": [], "historial": []}

def generar_sugerencia_ia(signos_vitales, sintomas, antecedentes=None):
    prompt = f"""
Eres un asistente de triaje clínico. Analiza los siguientes datos del paciente y proporciona:
1. Nivel de urgencia (bajo, moderado, alto, crítico)
2. Posibles diagnósticos diferenciales (hasta 3)
3. Recomendaciones iniciales de conducta

DATOS DEL PACIENTE:
- Signos Vitales:
  * Presión arterial: {signos_vitales.get('presion_sistolica', 'N/A')}/{signos_vitales.get('presion_diastolica', 'N/A')} mmHg
  * Frecuencia cardíaca: {signos_vitales.get('frecuencia_cardiaca', 'N/A')} lpm
  * Temperatura: {signos_vitales.get('temperatura', 'N/A')} °C
  * Saturación O₂: {signos_vitales.get('saturacion_oxigeno', 'N/A')} %

- Síntomas reportados: {sintomas}

{f'- Antecedentes relevantes: {antecedentes}' if antecedentes else ''}

Responde en formato JSON con esta estructura exacta:
{{
    "nivel_urgencia": "bajo|moderado|alto|critico",
    "confiabilidad": 0.XX,
    "posibles_diagnosticos": "diagnostico1, diagnostico2, diagnostico3",
    "recomendaciones": "Recomendación 1. Recomendación 2."
}}

Sé preciso y clínico en tu análisis.
"""

    try:
        import os
        api_key = os.getenv("OPENAI_API_KEY", "")
        if not api_key or api_key == "sk-tu-api-key-aqui":
            return {
                "nivel_urgencia": "moderado",
                "confiabilidad": 0.70,
                "posibles_diagnosticos": "Necesaria evaluación clínica presencial",
                "recomendaciones": "Derivar a consulta médica general para evaluación completa."
            }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": os.getenv("OPENAI_MODEL", "gpt-4"),
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            },
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            return json.loads(content)
        else:
            return {
                "nivel_urgencia": "moderado",
                "confiabilidad": 0.50,
                "posibles_diagnosticos": "Evaluación pendientes",
                "recomendaciones": "Consulte a su médico tratante."
            }
    except Exception as e:
        return {
            "nivel_urgencia": "moderado",
            "confiabilidad": 0.50,
            "posibles_diagnosticos": "Análisis no disponible",
            "recomendaciones": "Consulte a su médico tratante."
        }

def generar_pdf_reporte(data, titulo, periodo):
    pass
