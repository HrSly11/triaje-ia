import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import utils
from datetime import datetime

st.set_page_config(page_title="Nuevo Triaje - Sistema de Triaje IA", page_icon="🏥", layout="wide")

if "autenticado" not in st.session_state or not st.session_state.autenticado:
    st.error("Debe iniciar sesión para acceder a esta página")
    st.stop()

st.title("➕ Nuevo Triaje Clínico")
st.markdown("---")

tab_buscar, tab_lista = st.tabs(["🔍 Buscar Paciente", "📋 Lista de Pacientes"])

with tab_buscar:
    col_busqueda, col_btn_buscar = st.columns([3, 1])
    with col_busqueda:
        termino_busqueda = st.text_input("Buscar por nombre o número de documento", placeholder="Ej: 12345678 o nombre")
    with col_btn_buscar:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        btn_buscar = st.button("🔍 Buscar", use_container_width=True)

    if btn_buscar and termino_busqueda:
        resultado = utils.obtener_pacientes(busqueda=termino_busqueda)
        if resultado.get("pacientes"):
            paciente = resultado["pacientes"][0]
            st.session_state.paciente_seleccionado = paciente
            st.success(f"Paciente encontrado: {paciente['nombre_completo']}")
        else:
            st.warning("No se encontraron pacientes.")

with tab_lista:
    st.markdown("**Selecciona un paciente de la lista:**")
    resultado_todos = utils.obtener_pacientes(busqueda="", page=1, per_page=100)
    
    if resultado_todos.get("pacientes"):
        pacientes = resultado_todos["pacientes"]
        
        for paciente in pacientes:
            col_pac, col_btn = st.columns([4, 1])
            with col_pac:
                genero_emoji = "👨" if paciente.get("genero") == "Masculino" else "👩"
                st.markdown(f"{genero_emoji} **{paciente.get('nombre_completo', 'N/A')}** | {paciente.get('tipo_documento', 'CC')} {paciente.get('numero_documento', 'N/A')}")
            with col_btn:
                if st.button("Seleccionar", key=f"sel_{paciente.get('id_paciente')}"):
                    st.session_state.paciente_seleccionado = paciente
                    st.success(f"Paciente '{paciente['nombre_completo']}' seleccionado")
                    st.rerun()
    else:
        st.info("No hay pacientes registrados")

paciente_seleccionado = st.session_state.get("paciente_seleccionado", None)

if "paciente_seleccionado" in st.session_state and st.session_state.paciente_seleccionado:
    paciente_seleccionado = st.session_state.paciente_seleccionado
    st.success(f"Paciente seleccionado: {paciente_seleccionado['nombre_completo']}")

    col_info = st.columns(2)
    with col_info[0]:
        st.text_input("Nombre", value=paciente_seleccionado.get("nombre_completo", ""), disabled=True, key="nombre_paciente")
    with col_info[1]:
        st.text_input("Documento", value=f"{paciente_seleccionado.get('tipo_documento', 'CC')} {paciente_seleccionado.get('numero_documento', '')}", disabled=True, key="doc_paciente")

    with st.expander("📋 Consultar Antecedentes en HCE"):
        antecedentes = utils.obtener_antecedentes_hce(paciente_seleccionado.get("numero_documento", ""))
        if antecedentes.get("antecedentes"):
            st.markdown("**Antecedentes:**")
            for ant in antecedentes["antecedentes"]:
                st.write(f"- **{ant.get('nombre', 'N/A')}**: {ant.get('descripcion', '')}")
        else:
            st.info("No se encontraron antecedentes en HCE")

        if antecedentes.get("historial_sintomas"):
            st.markdown("**Historial de Síntomas:**")
            for hist in antecedentes["historial_sintomas"][:5]:
                st.write(f"- {hist.get('fecha', '')}: {hist.get('sintoma', '')} → {hist.get('diagnostico', '')}")

else:
    st.warning("Busque y seleccione un paciente antes de continuar con el triaje.")
    st.stop()

st.markdown("---")
st.subheader("📝 Datos del Triaje")

SINTOMAS_PRESION = ["Dolor de cabeza", "Mareo", "Visión borrosa", "Sangrado nasal", "Ninguno"]
SINTOMAS_CARDIACOS = ["Dolor torácico", "Palpitaciones", "Fatiga", "Disnea", "Ninguno"]
SINTOMAS_RESPIRATORIOS = ["Tos", "Dificultad respiratoria", "Sibilancias", "Dolor de garganta", "Congestión nasal", "Ninguno"]
SINTOMAS_DIGESTIVOS = ["Náuseas", "Vómito", "Diarrea", "Dolor abdominal", "Distensión", "Ninguno"]
SINTOMAS_GENERALES = ["Fiebre", "Calentura", "Escalofríos", "Sudoración", "Pérdida de apetito", "Ninguno"]

with st.form("form_triaje"):
    st.markdown("**Signos Vitales**")
    col_sv = st.columns(4)

    with col_sv[0]:
        presion_sistolica = st.number_input("Presión Sistólica (mmHg)", min_value=60, max_value=250, value=120)
    with col_sv[1]:
        presion_diastolica = st.number_input("Presión Diastólica (mmHg)", min_value=40, max_value=150, value=80)
    with col_sv[2]:
        frecuencia_cardiaca = st.number_input("Frecuencia Cardíaca (lpm)", min_value=30, max_value=250, value=72)
    with col_sv[3]:
        temperatura = st.number_input("Temperatura (°C)", min_value=35.0, max_value=42.0, value=36.5, step=0.1)

    col_sv2 = st.columns(2)
    with col_sv2[0]:
        saturacion_oxigeno = st.number_input("Saturación O₂ (%)", min_value=70, max_value=100, value=98)
    with col_sv2[1]:
        frecuencia_respiratoria = st.number_input("Frecuencia Respiratoria (rpm)", min_value=8, max_value=40, value=16)

    st.markdown("**Síntomas Principales**")

    col_symp = st.columns(2)
    with col_symp[0]:
        st.markdown("Presión arterial:")
        presion_symptoms = st.multiselect("Seleccione...", SINTOMAS_PRESION, default=["Ninguno"], label_visibility="collapsed")

        st.markdown("Cardíacos:")
        cardiac_symptoms = st.multiselect("Seleccione...", SINTOMAS_CARDIACOS, default=["Ninguno"], label_visibility="collapsed")

        st.markdown("Respiratorios:")
        respiratory_symptoms = st.multiselect("Seleccione...", SINTOMAS_RESPIRATORIOS, default=["Ninguno"], label_visibility="collapsed")

    with col_symp[1]:
        st.markdown("Digestivos:")
        digestive_symptoms = st.multiselect("Seleccione...", SINTOMAS_DIGESTIVOS, default=["Ninguno"], label_visibility="collapsed")

        st.markdown("Generales:")
        general_symptoms = st.multiselect("Seleccione...", SINTOMAS_GENERALES, default=["Ninguno"], label_visibility="collapsed")

    sintomas_texto_libre = st.text_area("Síntomas en texto libre (describa otros síntomas)", height=80)
    antecedentes_relevantes = st.text_area("Antecedentes relevantes", height=60)

    col_ia, col_resultado = st.columns([1, 1])

    with col_ia:
        st.markdown("**🤖 Análisis con IA**")
        analizar_ia = st.checkbox("Solicitar análisis de IA", value=True)

        if analizar_ia:
            st.info("El sistema utilizará IA para analizar los datos y proporcionar nivel de urgencia, diagnósticos y recomendaciones.")

    with col_resultado:
        st.markdown("**Resultado del Triaje**")
        nivel_urgencia = st.selectbox("Nivel de Urgencia", ["", "bajo", "moderado", "alto", "critico"], index=0)
        estado = st.selectbox("Estado", ["completado", "en_proceso", "derivado"], index=0)

    observaciones = st.text_area("Observaciones adicionales", height=60)

    submitted = st.form_submit_button("💾 Guardar Triaje", use_container_width=True)

if submitted:
    if not paciente_seleccionado:
        st.error("Debe seleccionar un paciente primero")
    elif not nivel_urgencia:
        st.error("Debe especificar el nivel de urgencia")
    else:
        sintomas_seleccionados = []
        for symptom_list in [presion_symptoms, cardiac_symptoms, respiratory_symptoms, digestive_symptoms, general_symptoms]:
            for s in symptom_list:
                if s != "Ninguno" and s not in sintomas_seleccionados:
                    sintomas_seleccionados.append(s)

        signos_vitales = {
            "presion_sistolica": presion_sistolica,
            "presion_diastolica": presion_diastolica,
            "frecuencia_cardiaca": frecuencia_cardiaca,
            "temperatura": temperatura,
            "saturacion_oxigeno": saturacion_oxigeno
        }

        sintomas_str = ", ".join(sintomas_seleccionados) if sintomas_seleccionados else sintomas_texto_libre

        resultado_ia = None
        if analizar_ia:
            with st.spinner("🤖 Analizando con IA..."):
                resultado_ia = utils.generar_sugerencia_ia(
                    signos_vitales=signos_vitales,
                    sintomas=sintomas_str,
                    antecedentes=antecedentes_relevantes
                )
                st.success("✓ Análisis de IA completado")

        triaje_data = {
            "id_paciente": str(paciente_seleccionado.get("id_paciente")),
            "id_usuario": str(st.session_state.usuario.get("id_usuario")),
            "presion_arterial_sistolica": presion_sistolica,
            "presion_arterial_diastolica": presion_diastolica,
            "frecuencia_cardiaca": frecuencia_cardiaca,
            "temperatura": temperatura,
            "saturacion_oxigeno": saturacion_oxigeno,
            "sintomas_principales": sintomas_str,
            "sintomas_texto_libre": sintomas_texto_libre,
            "antecedentes_relevantes": antecedentes_relevantes,
            "nivel_urgencia": nivel_urgencia,
            "estado": estado,
            "resultado_ia": resultado_ia
        }

        resultado_triaje = utils.crear_triaje(triaje_data)

        if "error" not in resultado_triaje:
            id_triaje = resultado_triaje.get("id_triaje")
            completar_data = {
                "id_usuario": str(st.session_state.usuario.get("id_usuario")),
                "nivel_urgencia": nivel_urgencia,
                "observaciones": observaciones
            }

            if resultado_ia:
                completar_data["resultado_ia"] = {
                    "nivel_urgencia_sugerido": resultado_ia.get("nivel_urgencia"),
                    "confiabilidad": resultado_ia.get("confiabilidad"),
                    "posibles_diagnosticos": resultado_ia.get("posibles_diagnosticos"),
                    "recomendaciones": resultado_ia.get("recomendaciones"),
                    "parametros_entrada": str(signos_vitales)
                }

            utils.completar_triaje(id_triaje, completar_data)

            st.success("✓ Triaje guardado exitosamente")

            if resultado_ia:
                st.balloons()
                st.markdown("---")
                st.markdown("**📋 Resultado del Análisis de IA:**")
                col_res = st.columns(2)
                with col_res[0]:
                    st.metric("Nivel de Urgencia Sugerido", resultado_ia.get("nivel_urgencia", "N/A").upper())
                    st.metric("Confiabilidad", f"{resultado_ia.get('confiabilidad', 0)*100:.0f}%" if resultado_ia.get("confiabilidad") else "N/A")
                with col_res[1]:
                    st.markdown(f"**Posibles Diagnósticos:**\n{resultado_ia.get('posibles_diagnosticos', 'N/A')}")
                    st.markdown(f"**Recomendaciones:**\n{resultado_ia.get('recomendaciones', 'N/A')}")

            st.markdown("---")
            col_nuevo = st.columns([1, 1])
            with col_nuevo[0]:
                if st.button("➕ Nuevo Triaje", use_container_width=True):
                    if "paciente_seleccionado" in st.session_state:
                        del st.session_state.paciente_seleccionado
                    st.rerun()
        else:
            st.error(f"Error: {resultado_triaje.get('error', 'Error desconocido')}")