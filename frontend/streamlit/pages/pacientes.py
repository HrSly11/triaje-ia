import streamlit as st
import sys
import os
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import utils
from datetime import datetime

st.set_page_config(page_title="Pacientes - Sistema de Triaje IA", page_icon="👥", layout="wide")

if "autenticado" not in st.session_state or not st.session_state.autenticado:
    st.error("Debe iniciar sesión para acceder a esta página")
    st.stop()

st.title("👥 Gestión de Pacientes")
st.markdown("---")

tab1, tab2 = st.tabs(["🔍 Buscar Pacientes", "➕ Registrar Paciente"])

with tab1:
    col_busq, col_filtros = st.columns([2, 1])
    with col_busq:
        termino = st.text_input("Buscar por nombre o número de documento", placeholder="Ej: 12345678 o nombre del paciente")
    with col_filtros:
        ver_inactivos = st.checkbox("Ver inactivos")

    if st.button("🔍 Buscar", use_container_width=True):
        resultado = utils.obtener_pacientes(busqueda=termino)
        st.session_state.resultado_busqueda = resultado

    if "resultado_busqueda" in st.session_state and st.session_state.resultado_busqueda.get("pacientes"):
        pacientes = st.session_state.resultado_busqueda["pacientes"]
        total = st.session_state.resultado_busqueda.get("total", 0)

        st.success(f"Se encontraron {total} paciente(s)")
        
        df_pacientes = pd.DataFrame(pacientes)
        df_display = df_pacientes[['numero_documento', 'nombre_completo', 'genero', 'telefono', 'fecha_registro']].copy()
        df_display.columns = ['Documento', 'Nombre', 'Género', 'Teléfono', 'Fecha Registro']
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("**Detalles de Pacientes:**")
        
        for i, paciente in enumerate(pacientes):
            with st.expander(f"📋 {paciente.get('nombre_completo', 'N/A')} | {paciente.get('numero_documento', 'N/A')}"):
                col_det = st.columns(2)
                with col_det[0]:
                    st.text_input("Tipo Documento", value=paciente.get("tipo_documento", "CC"), disabled=True, key=f"tipo_doc_{i}")
                    st.text_input("Nombre", value=paciente.get("nombre_completo", ""), disabled=True, key=f"nombre_{i}")
                    st.text_input("Fecha Nacimiento", value=str(paciente.get("fecha_nacimiento", "")), disabled=True, key=f"fecha_nac_{i}")
                with col_det[1]:
                    st.text_input("Género", value=paciente.get("genero", ""), disabled=True, key=f"genero_{i}")
                    st.text_input("Teléfono", value=paciente.get("telefono", "N/A") or "N/A", disabled=True, key=f"telefono_{i}")
                    st.text_input("Correo", value=paciente.get("correo", "N/A") or "N/A", disabled=True, key=f"correo_{i}")

                if st.button("📋 Usar para Triaje", key=f"triaje_btn_{paciente.get('id_paciente')}"):
                    st.session_state.paciente_seleccionado = paciente
                    st.success(f"Paciente '{paciente.get('nombre_completo')}' seleccionado para triaje")
                    st.rerun()
    elif "resultado_busqueda" in st.session_state:
        st.info("No se encontraron pacientes con ese criterio")
    else:
        st.info("Ingrese un término de búsqueda y haga clic en 'Buscar'")

with tab2:
    st.subheader("Registro de Nuevo Paciente")
    with st.form("form_registro_paciente"):
        col_doc = st.columns(2)
        with col_doc[0]:
            tipo_documento = st.selectbox("Tipo de Documento", ["CC", "CE", "TI", "PA", "RC", "NIT"])
        with col_doc[1]:
            numero_documento = st.text_input("Número de Documento *", placeholder="Sin puntos ni espacios")

        nombre_completo = st.text_input("Nombre Completo *", placeholder="Nombres y Apellidos")

        col_fecha = st.columns(2)
        with col_fecha[0]:
            fecha_nacimiento = st.date_input("Fecha de Nacimiento *", format="YYYY-MM-DD")
        with col_fecha[1]:
            genero = st.selectbox("Género *", ["Masculino", "Femenino", "Otro"])

        col_contacto = st.columns(2)
        with col_contacto[0]:
            telefono = st.text_input("Teléfono", placeholder="+57 3XX XXX XXXX")
        with col_contacto[1]:
            correo = st.text_input("Correo electrónico", placeholder="email@ejemplo.com")

        direccion = st.text_input("Dirección", placeholder="Carrera/Calle # XX - XX")

        submitted = st.form_submit_button("💾 Registrar Paciente", use_container_width=True)

        if submitted:
            if not numero_documento or not nombre_completo or not fecha_nacimiento:
                st.error("Los campos marcados con * son requeridos")
            else:
                data = {
                    "numero_documento": numero_documento,
                    "tipo_documento": tipo_documento,
                    "nombre_completo": nombre_completo,
                    "fecha_nacimiento": fecha_nacimiento.strftime("%Y-%m-%d"),
                    "genero": genero,
                    "telefono": telefono if telefono else None,
                    "correo": correo if correo else None,
                    "direccion": direccion if direccion else None,
                    "id_usuario": str(st.session_state.usuario.get("id_usuario"))
                }

                resultado = utils.crear_paciente(data)

                if "error" not in resultado:
                    st.success("✓ Paciente registrado exitosamente")
                    st.balloons()
                else:
                    st.error(f"Error: {resultado.get('error', 'Error desconocido')}")
