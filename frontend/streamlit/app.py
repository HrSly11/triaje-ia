import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import utils

st.set_page_config(
    page_title="Sistema de Triaje Clínico - IA",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.usuario = None

def pagina_login():
    st.title("Sistema de Triaje Clínico Asistido por IA")
    st.markdown("Plataforma de gestión de triage con inteligencia artificial")
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.subheader("Iniciar Sesión")
            nombre_usuario = st.text_input("Usuario", placeholder="Ingrese su usuario")
            contrasena = st.text_input("Contraseña", type="password", placeholder="Ingrese su contraseña")
            submit = st.form_submit_button("Ingresar", use_container_width=True)

            if submit:
                if not nombre_usuario or not contrasena:
                    st.error("Todos los campos son requeridos")
                else:
                    usuario = utils.login_usuario(nombre_usuario, contrasena)
                    if usuario:
                        st.session_state.autenticado = True
                        st.session_state.usuario = usuario
                        st.success("¡Bienvenido!")
                        st.rerun()
                    else:
                        st.error("Credenciales inválidas")

    st.markdown("---")
    st.markdown("**Credenciales de prueba:** admin / admin123")

def pagina_principal():
    st.title("Sistema de Triaje Clínico Asistido por IA")

    usuario = st.session_state.usuario

    col_info, col_rol = st.columns([3, 1])
    with col_info:
        st.success(f"Bienvenido, {usuario.get('nombre_completo', 'N/A')}")
    with col_rol:
        st.info(f"Rol: {usuario.get('rol', 'N/A').upper()}")

    st.markdown("---")
    st.subheader("Resumen del Día")

    col1, col2, col3, col4 = st.columns(4)

    metricas = utils.obtener_dashboard_operacional()

    with col1:
        total = metricas.get('metricas', {}).get('total_triajes', 0) if metricas else 0
        st.metric("Total Triajes", total)

    with col2:
        criticos = metricas.get('metricas', {}).get('criticos', 0) if metricas else 0
        st.metric("Críticos", criticos)

    with col3:
        altos = metricas.get('metricas', {}).get('altos', 0) if metricas else 0
        st.metric("Altos", altos)

    with col4:
        avg_time = metricas.get('metricas', {}).get('tiempo_promedio_minutos', 0) if metricas else 0
        avg_time_display = f"{float(avg_time):.1f} min" if avg_time and isinstance(avg_time, (int, float, str)) and str(avg_time) != 'None' else "N/A"
        st.metric("Tiempo Promedio", avg_time_display)

    st.markdown("---")
    st.info("Usa el menú lateral izquierdo para navegar entre las diferentes secciones del sistema.")

    st.markdown("---")
    st.caption("Sistema de Triaje Clínico Asistido por IA - v1.0 | Desarrollado para integración con n8n y HCE")

def logout():
    st.session_state.autenticado = False
    st.session_state.usuario = None
    st.rerun()

if __name__ == "__main__":
    if not st.session_state.autenticado:
        pagina_login()
    else:
        pagina_principal()