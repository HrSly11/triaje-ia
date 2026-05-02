import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import utils
from datetime import datetime, timedelta

st.set_page_config(page_title="Ver Triajes - Sistema de Triaje IA", page_icon="📋", layout="wide")

if "autenticado" not in st.session_state or not st.session_state.autenticado:
    st.error("Debe iniciar sesión para acceder a esta página")
    st.stop()

st.title("📋 Lista de Triajes")
st.markdown("---")

col_filtros1, col_filtros2, col_filtros3 = st.columns([1, 1, 1])

with col_filtros1:
    fecha_desde = st.date_input("Desde", value=datetime.now().date() - timedelta(days=7))
with col_filtros2:
    fecha_hasta = st.date_input("Hasta", value=datetime.now().date())
with col_filtros3:
    nivel_opciones = ["Todos", "critico", "alto", "moderado", "bajo"]
    nivel_seleccionado = st.selectbox("Nivel de Urgencia", nivel_opciones)

col_pagina = st.columns([1, 4, 1])
with col_pagina[0]:
    page = 1
with col_pagina[1]:
    page = st.number_input("Página", min_value=1, value=1, step=1)

nivel_filtro = nivel_seleccionado if nivel_seleccionado != "Todos" else None

resultado = utils.listar_triajes(
    page=page,
    per_page=20,
    fecha_desde=fecha_desde.strftime("%Y-%m-%d"),
    fecha_hasta=fecha_hasta.strftime("%Y-%m-%d"),
    nivel_urgencia=nivel_filtro
)

if resultado.get("triajes"):
    triajes = resultado["triajes"]
    total = resultado.get("total", 0)
    total_pages = resultado.get("total_pages", 1)
    
    st.success(f"Se encontraron {total} triaje(s) - Página {page} de {total_pages}")
    
    for triaje in triajes:
        nivel = triaje.get("nivel_urgencia", "N/A")
        
        color_map = {
            "critico": "🔴",
            "alto": "🟠", 
            "moderado": "🟡",
            "bajo": "🟢"
        }
        emoji = color_map.get(nivel, "⚪")
        
        with st.expander(f"{emoji} {triaje.get('fecha_hora', 'N/A')} - {triaje.get('paciente_nombre', 'Paciente N/A')} - Urgencia: {nivel.upper()}"):
            col_det = st.columns(2)
            with col_det[0]:
                st.markdown("**Datos del Paciente**")
                st.write(f"- Nombre: {triaje.get('paciente_nombre', 'N/A')}")
                st.write(f"- Documento: {triaje.get('paciente_documento', 'N/A')}")
                st.write(f"- Fecha: {triaje.get('fecha_hora', 'N/A')}")
            
            with col_det[1]:
                st.markdown("**Signos Vitales**")
                st.write(f"- Presión: {triaje.get('presion_arterial_sistolica', 'N/A')}/{triaje.get('presion_arterial_diastolica', 'N/A')} mmHg")
                st.write(f"- FC: {triaje.get('frecuencia_cardiaca', 'N/A')} lpm")
                st.write(f"- Temperatura: {triaje.get('temperatura', 'N/A')} °C")
                st.write(f"- O₂: {triaje.get('saturacion_oxigeno', 'N/A')}%")
            
            st.markdown("**Síntomas**")
            st.write(triaje.get('sintomas_principales', 'N/A'))
            
            if triaje.get('observaciones'):
                st.markdown("**Observaciones**")
                st.write(triaje.get('observaciones'))
    
    if total_pages > 1:
        col_nav = st.columns(3)
        with col_nav[1]:
            st.info(f"Página {page} de {total_pages}. Use los controles arriba para cambiar de página.")
else:
    st.info("No se encontraron triajes con los criterios seleccionados")
