import streamlit as st
import requests
import json
import os
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Historia Clínica", page_icon="📋", layout="wide")

API_URL = os.getenv("API_URL", "http://localhost:5000")
HCE_URL = os.getenv("HCE_URL", "http://localhost:8001")

def get_paciente_hce(numero_documento):
    try:
        response = requests.get(f"{HCE_URL}/api/pacientes/{numero_documento}", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def get_antecedentes_hce(numero_documento):
    try:
        response = requests.get(f"{HCE_URL}/api/pacientes/{numero_documento}/antecedentes", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def get_logs_sincronizacion():
    try:
        response = requests.get(f"{API_URL}/api/logs?accion=SINCRONIZADO_HCE&limite=20", timeout=5)
        if response.status_code == 200:
            return response.json().get('logs', [])
    except:
        pass
    return []

def main():
    st.title("Historia Clínica Electrónica")
    st.markdown("Consulta y gestiona la información clínica de los pacientes sincronizados con el HCE")
    st.markdown("---")

    numero_documento = st.text_input("Número de documento del paciente", placeholder="Ej: 12345678")

    if st.button("Buscar") and numero_documento:
        paciente = get_paciente_hce(numero_documento)

        if paciente:
            antecedentes_data = get_antecedentes_hce(numero_documento)

            genero = 'Masculino' if paciente.get('genero') == 'M' else 'Femenino' if paciente.get('genero') == 'F' else 'N/A'

            st.subheader("Datos del Paciente")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Nombre", paciente.get('nombre_completo', 'N/A'))
            with col2:
                st.metric("Documento", f"{paciente.get('tipo_documento', 'N/A')} {paciente.get('numero_documento', 'N/A')}")
            with col3:
                st.metric("Género", genero)
            with col4:
                st.metric("Teléfono", paciente.get('telefono', 'N/A'))

            tabs = st.tabs(["Triajes", "Antecedentes", "Signos Vitales", "Historial"])

            with tabs[0]:
                st.subheader("Historia de Triajes")

                logs = get_logs_sincronizacion()
                triajes_paciente = [log for log in logs if numero_documento in str(log.get('detalles', ''))]

                if triajes_paciente:
                    for triaje in triajes_paciente:
                        datos = triaje.get('detalles', {})
                        if isinstance(datos, str):
                            try:
                                datos = json.loads(datos)
                            except:
                                datos = {}

                        nivel = datos.get('nivel_urgencia', 'desconocido')
                        nivel_color = {"critico": "red", "alto": "orange", "moderado": "yellow", "bajo": "green"}.get(nivel.lower(), "gray")

                        st.info(f"**ID:** {str(triaje.get('id_registro_afectado', 'N/A'))[:8]}... | **Nivel:** {nivel.upper()} | **Fecha:** {triaje.get('fecha', 'N/A')}")
                        st.write(f"**Síntomas:** {datos.get('sintomas', 'N/A')}")
                        st.markdown("---")
                else:
                    st.warning("No hay triajes sincronizados con el HCE para este paciente")

            with tabs[1]:
                st.subheader("Antecedentes Clínicos")

                if antecedentes_data and antecedentes_data.get('antecedentes'):
                    for ant in antecedentes_data['antecedentes']:
                        tipo_icon = {"enfermedad": "🏥", "alergia": "⚠️", "procedimiento": "🔧", "habito": "🚬", "condicion": "❤️"}.get(ant.get('tipo', 'general'), "📋")
                        st.write(f"{tipo_icon} **{ant.get('nombre', 'N/A').upper()}:** {ant.get('descripcion', 'N/A')}")
                else:
                    st.info("No hay antecedentes registrados para este paciente")

            with tabs[2]:
                st.subheader("Signos Vitales Base")

                if antecedentes_data and antecedentes_data.get('signos_vitales_base'):
                    sv = antecedentes_data['signos_vitales_base']
                    col1, col2, col3, col4, col5, col6 = st.columns(6)

                    with col1:
                        st.metric("PA", f"{sv.get('presion_arterial', 'N/A')}", "mmHg")
                    with col2:
                        st.metric("FC", f"{sv.get('frecuencia_cardiaca', 'N/A')}", "lpm")
                    with col3:
                        st.metric("Temp", f"{sv.get('temperatura', 'N/A')}°", "°C")
                    with col4:
                        st.metric("Sat O2", f"{sv.get('saturacion_oxigeno', 'N/A')}%", "%")
                    with col5:
                        st.metric("FR", f"{sv.get('frecuencia_respiratoria', 'N/A')}", "rpm")
                    with col6:
                        st.metric("Peso", f"{sv.get('peso', 'N/A')}", "kg")
                else:
                    st.info("No hay signos vitales registrados para este paciente")

            with tabs[3]:
                st.subheader("Historial de Atención")

                if antecedentes_data and antecedentes_data.get('historial_sintomas'):
                    for item in antecedentes_data['historial_sintomas']:
                        with st.expander(f"{item.get('fecha', 'N/A')} - {item.get('sintoma', 'N/A')}"):
                            st.write(f"**Diagnóstico:** {item.get('diagnostico', 'N/A')}")
                            st.write(f"**Tratamiento:** {item.get('tratamiento', 'N/A')}")
                else:
                    st.info("No hay historial de atención para este paciente")
        else:
            st.error(f"No se encontró la historia clínica para el documento: {numero_documento}")

    elif not numero_documento:
        st.info("Ingrese el número de documento del paciente para consultar su historia clínica")

        st.subheader("Pacientes Recientes con Triajes")
        logs = get_logs_sincronizacion()
        if logs:
            data = []
            for log in logs[:10]:
                datos = log.get('detalles', {})
                if isinstance(datos, str):
                    try:
                        datos = json.loads(datos)
                    except:
                        datos = {}
                data.append({
                    'ID Triaje': str(log.get('id_registro_afectado', ''))[:8],
                    'Fecha': log.get('fecha', 'N/A'),
                    'Nivel': datos.get('nivel_urgencia', 'N/A'),
                    'Síntomas': datos.get('sintomas', 'N/A')[:50]
                })

            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("No hay registros de sincronización con el HCE")

    st.markdown("---")
    st.caption("Sistema de Triaje Clínico Asistido por IA - v1.0 | Integración con n8n y HCE")

if __name__ == "__main__":
    main()