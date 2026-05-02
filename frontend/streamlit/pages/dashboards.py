import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import utils
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF

st.set_page_config(page_title="Dashboards - Sistema de Triaje IA", page_icon="📊", layout="wide")

if "autenticado" not in st.session_state or not st.session_state.autenticado:
    st.error("Debe iniciar sesión para acceder a esta página")
    st.stop()

st.title("📊 Dashboards de Triaje")
st.markdown("---")

tab_operacional, tab_gestion = st.tabs(["📈 Dashboard Operacional", "📋 Dashboard de Gestión"])

with tab_operacional:
    st.subheader("Panel Operacional - Día en Curso")

    col_fecha = st.columns([1, 4])
    with col_fecha[0]:
        fecha_seleccionada = st.date_input("📅 Fecha", value=datetime.now().date())
    with col_fecha[1]:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        actualizar = st.button("🔄 Actualizar", use_container_width=False)

    datos = utils.obtener_dashboard_operacional(fecha=fecha_seleccionada.strftime("%Y-%m-%d"))

    if datos and datos.get("metricas"):
        metricas = datos.get("metricas", {})

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("📊 Total Triajes", metricas.get("total_triajes", 0))
        with col_m2:
            criticos = metricas.get("criticos", 0)
            st.metric("🔴 Críticos", criticos, delta_color="inverse")
        with col_m3:
            altos = metricas.get("altos", 0)
            st.metric("🟠 Altos", altos, delta_color="off")
        with col_m4:
            avg_time = metricas.get("tiempo_promedio_minutos", 0)
            avg_time_display = f"{float(avg_time):.1f} min" if avg_time and isinstance(avg_time, (int, float, str)) and str(avg_time) != 'None' else "N/A"
            st.metric("⏱️ Tiempo Promedio", avg_time_display)

        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.markdown("**📊 Distribución por Nivel de Urgencia**")
            dist = datos.get("distribucion_urgencia", [])
            if dist:
                df_dist = pd.DataFrame(dist)
                fig_pie = px.pie(df_dist, values="cantidad", names="nivel_urgencia",
                                 color="nivel_urgencia",
                                 color_discrete_map={"critico": "#e74c3c", "alto": "#e67e22",
                                           "moderado": "#f39c12", "bajo": "#27ae60"})
                fig_pie.update_layout(margin=dict(l=20, r=20, t=30, b=20))
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No hay datos para esta fecha")

        with col_g2:
            st.markdown("**📈 Triajes por Hora**")
            por_hora = datos.get("triajes_por_hora", [])
            if por_hora:
                df_hora = pd.DataFrame(por_hora)
                df_hora["hora"] = pd.to_datetime(df_hora["hora"])
                fig_bar = px.bar(df_hora, x="hora", y="cantidad", text="cantidad")
                fig_bar.update_layout(xaxis_title="Hora", yaxis_title="Cantidad de Triajes")
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("No hay datos para esta fecha")

        st.markdown("---")

        st.markdown("### 📋 Triajes Recientes del Día")
        triajes = utils.listar_triajes(
            fecha_desde=fecha_seleccionada.strftime("%Y-%m-%d"),
            fecha_hasta=fecha_seleccionada.strftime("%Y-%m-%d")
        )
        if triajes.get("triajes"):
            df_triajes = pd.DataFrame(triajes["triajes"])
            df_triajes["fecha_hora"] = pd.to_datetime(df_triajes["fecha_hora"]).dt.strftime("%Y-%m-%d %H:%M")
            st.dataframe(df_triajes[["fecha_hora", "paciente_nombre", "nivel_urgencia", "usuario_nombre"]], use_container_width=True)
        else:
            st.info("No hay triajes para esta fecha")

        st.markdown("---")

        st.markdown("### 📥 Exportar Reportes")
        
        def generar_pdf_operacional_profesional(datos, metricas, fecha_seleccionada):
            pdf = FPDF()
            pdf.add_page()
            
            pdf.set_fill_color(41, 128, 185)
            pdf.rect(0, 0, 210, 40, 'F')
            pdf.set_font("Helvetica", "B", 20)
            pdf.set_text_color(255, 255, 255)
            pdf.set_y(10)
            pdf.cell(0, 15, "SISTEMA DE TRIAGE CLINICO", ln=True, align="C")
            pdf.set_font("Helvetica", "", 12)
            pdf.cell(0, 8, "Reporte Operacional Diario", ln=True, align="C")
            
            pdf.set_text_color(0, 0, 0)
            pdf.set_y(50)
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 10, f"Fecha del Reporte: {fecha_seleccionada}", ln=True)
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 6, f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
            pdf.ln(10)

            pdf.set_font("Helvetica", "B", 14)
            pdf.set_fill_color(230, 230, 230)
            pdf.cell(0, 10, "RESUMEN DE METRICAS", ln=True, fill=True)
            pdf.set_font("Helvetica", "", 11)
            pdf.ln(5)
            
            metrics_data = [
                ["Total de Triajes", str(metricas.get('total_triajes', 0))],
                ["Casos Criticos", str(metricas.get('criticos', 0))],
                ["Casos Altos", str(metricas.get('altos', 0))],
                ["Casos Moderados", str(metricas.get('moderados', 0))],
                ["Casos Bajos", str(metricas.get('bajos', 0))],
            ]
            avg_time = metricas.get("tiempo_promedio_minutos", 0)
            avg_time_display = f"{float(avg_time):.1f} minutos" if avg_time and str(avg_time) != 'None' else "N/A"
            metrics_data.append(["Tiempo Promedio Atencion", avg_time_display])
            
            for label, value in metrics_data:
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(80, 8, label, border=1)
                pdf.set_font("Helvetica", "", 10)
                pdf.cell(0, 8, value, border=1, ln=True)
            
            pdf.ln(10)
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 10, "DISTRIBUCION POR NIVEL DE URGENCIA", ln=True, fill=True)
            pdf.set_font("Helvetica", "", 11)
            pdf.ln(5)
            
            dist = datos.get("distribucion_urgencia", [])
            if dist:
                for d in dist:
                    nivel = d.get("nivel_urgencia", "N/A").upper()
                    cantidad = d.get("cantidad", 0)
                    color_map = {"CRITICO": "[CRITICO]", "ALTO": "[ALTO]", "MODERADO": "[MODERADO]", "BAJO": "[BAJO]"}
                    icon = color_map.get(nivel, "")
                    pdf.cell(0, 8, f"{icon} {nivel}: {cantidad} casos", ln=True)
            else:
                pdf.cell(0, 8, "No hay datos disponibles", ln=True)
            
            pdf.ln(10)
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 10, "TRIAJES POR HORA", ln=True, fill=True)
            pdf.set_font("Helvetica", "", 11)
            pdf.ln(5)
            
            por_hora = datos.get("triajes_por_hora", [])
            if por_hora:
                for h in por_hora:
                    hora = h.get("hora", "")[:19]
                    cantidad = h.get("cantidad", 0)
                    pdf.cell(0, 7, f"   {hora}: {cantidad} triaje(s)", ln=True)
            else:
                pdf.cell(0, 8, "No hay datos disponibles", ln=True)
            
            pdf.ln(15)
            pdf.set_draw_color(41, 128, 185)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(128, 128, 128)
            pdf.cell(0, 6, "Este reporte fue generado automaticamente por el Sistema de Triaje Clinico Asistido por IA", ln=True, align="C")
            pdf.cell(0, 6, "Hospital Central - Departamento de Emergencias", ln=True, align="C")
            
            return pdf.output()
        
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            csv_data = f"REPORTE OPERACIONAL - {fecha_seleccionada}\n"
            csv_data += "=" * 50 + "\n"
            csv_data += f"Fecha: {fecha_seleccionada}\n"
            csv_data += f"Total Triajes,{metricas.get('total_triajes', 0)}\n"
            csv_data += f"Criticos,{metricas.get('criticos', 0)}\n"
            csv_data += f"Altos,{metricas.get('altos', 0)}\n"
            csv_data += f"Moderados,{metricas.get('moderados', 0)}\n"
            csv_data += f"Bajos,{metricas.get('bajos', 0)}\n"
            csv_data += "\nDistribucion por Urgencia\n"
            csv_data += "Nivel,Cantidad\n"
            for d in datos.get("distribucion_urgencia", []):
                csv_data += f"{d.get('nivel_urgencia', '')},{d.get('cantidad', 0)}\n"
            
            st.download_button(
                label="📥 Descargar CSV",
                data=csv_data,
                file_name=f"reporte_operacional_{fecha_seleccionada}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_exp2:
            pdf_data = generar_pdf_operacional_profesional(datos, metricas, fecha_seleccionada)
            if isinstance(pdf_data, bytearray):
                pdf_data = bytes(pdf_data)
            st.download_button(
                label="📄 Descargar PDF",
                data=pdf_data,
                file_name=f"reporte_operacional_{fecha_seleccionada}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.warning("No hay datos disponibles para la fecha seleccionada. Seleccione otra fecha o verifique que existan triajes.")

with tab_gestion:
    st.subheader("Panel de Gestión - Estadísticas Mensuales")

    col_mes = st.columns([1, 4])
    with col_mes[0]:
        hoy = datetime.now()
        year = hoy.year
        meses = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }
        mes_nombre = st.selectbox("📅 Mes", options=list(meses.keys()), index=hoy.month-1,
                                   format_func=lambda x: f"{meses[x]} {year}")
        mes_seleccionado = f"{year}-{mes_nombre:02d}"
    with col_mes[1]:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        actualizar_mes = st.button("🔄 Actualizar Mes", use_container_width=False)

    datos_gestion = utils.obtener_dashboard_gestion(mes=mes_seleccionado)

    if datos_gestion and datos_gestion.get("metricas"):
        metricas = datos_gestion.get("metricas", {})

        col_gm1, col_gm2, col_gm3, col_gm4, col_gm5 = st.columns(5)
        with col_gm1:
            st.metric("📊 Total Mes", metricas.get("total_triajes", 0))
        with col_gm2:
            criticos = metricas.get("criticos", 0)
            st.metric("🔴 Críticos", criticos, delta_color="inverse")
        with col_gm3:
            altos = metricas.get("altos", 0)
            st.metric("🟠 Altos", altos, delta_color="off")
        with col_gm4:
            moderados = metricas.get("moderados", 0)
            st.metric("🟡 Moderados", moderados)
        with col_gm5:
            bajos = metricas.get("bajos", 0)
            st.metric("🟢 Bajos", bajos)

        col_gg1, col_gg2 = st.columns(2)

        with col_gg1:
            st.markdown("**📈 Triajes por Día**")
            por_dia = datos_gestion.get("triajes_por_dia", [])
            if por_dia:
                df_dia = pd.DataFrame(por_dia)
                df_dia["fecha"] = pd.to_datetime(df_dia["fecha"])
                fig_line = px.line(df_dia, x="fecha", y="cantidad", markers=True, text="cantidad")
                fig_line.update_layout(xaxis_title="Fecha", yaxis_title="Cantidad de Triajes")
                st.plotly_chart(fig_line, use_container_width=True)
            else:
                st.info("No hay datos para este mes")

        with col_gg2:
            st.markdown("**👨‍⚕️ Triajes por Profesional**")
            por_prof = datos_gestion.get("triajes_por_profesional", [])
            if por_prof:
                df_prof = pd.DataFrame(por_prof)
                fig_barh = px.bar(df_prof, y="nombre_completo", x="cantidad", orientation="h", text="cantidad")
                fig_barh.update_layout(yaxis_title="Profesional", xaxis_title="Cantidad de Triajes")
                st.plotly_chart(fig_barh, use_container_width=True)
            else:
                st.info("No hay datos para este mes")

        col_gg3, col_gg4 = st.columns(2)

        with col_gg3:
            st.markdown("**📊 Distribución por Urgencia**")
            dist = datos_gestion.get("distribucion_urgencia", [])
            if dist:
                df_dist = pd.DataFrame(dist)
                fig_barra = px.bar(df_dist, x="nivel_urgencia", y="cantidad", color="nivel_urgencia",
                                  color_discrete_map={"critico": "#e74c3c", "alto": "#e67e22",
                                           "moderado": "#f39c12", "bajo": "#27ae60"},
                                  text="cantidad")
                fig_barra.update_layout(xaxis_title="Nivel de Urgencia", yaxis_title="Cantidad")
                st.plotly_chart(fig_barra, use_container_width=True)
            else:
                st.info("No hay datos para este mes")

        with col_gg4:
            st.markdown("**📋 Resumen de Tendencias**")
            criticos = metricas.get("criticos", 0)
            altos = metricas.get("altos", 0)
            total = metricas.get("total_triajes", 0)
            if total > 0:
                pct_criticos = (criticos / total) * 100
                pct_altos = (altos / total) * 100

                st.markdown(f"- **Casos Críticos:** {criticos} ({pct_criticos:.1f}% del total)")
                st.markdown(f"- **Casos Altos:** {altos} ({pct_altos:.1f}% del total)")
                st.markdown(f"- **Total atenciones:** {total}")

                if pct_criticos > 10:
                    st.warning("⚠️ El porcentaje de casos críticos es alto este mes")
                else:
                    st.success("✓ Los niveles de urgencia crítica están dentro de rangos normales")
            else:
                st.info("No hay datos suficientes para analizar tendencias")

        st.markdown("---")
        
        st.markdown("### 📥 Exportar Reportes")
        
        def generar_pdf_gestion_profesional(datos, metricas, mes_seleccionado):
            pdf = FPDF()
            pdf.add_page()
            
            pdf.set_fill_color(39, 174, 96)
            pdf.rect(0, 0, 210, 40, 'F')
            pdf.set_font("Helvetica", "B", 20)
            pdf.set_text_color(255, 255, 255)
            pdf.set_y(10)
            pdf.cell(0, 15, "SISTEMA DE TRIAGE CLINICO", ln=True, align="C")
            pdf.set_font("Helvetica", "", 12)
            pdf.cell(0, 8, "Reporte Mensual de Gestion", ln=True, align="C")
            
            pdf.set_text_color(0, 0, 0)
            pdf.set_y(50)
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 10, f"Periodo: {mes_seleccionado}", ln=True)
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 6, f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
            pdf.ln(10)
            
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_fill_color(230, 230, 230)
            pdf.cell(0, 10, "RESUMEN DE METRICAS", ln=True, fill=True)
            pdf.set_font("Helvetica", "", 11)
            pdf.ln(5)
            
            metrics_data = [
                ["Total de Triajes del Mes", str(metricas.get('total_triajes', 0))],
                ["Casos Criticos", str(metricas.get('criticos', 0))],
                ["Casos Altos", str(metricas.get('altos', 0))],
                ["Casos Moderados", str(metricas.get('moderados', 0))],
                ["Casos Bajos", str(metricas.get('bajos', 0))],
            ]
            
            for label, value in metrics_data:
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(80, 8, label, border=1)
                pdf.set_font("Helvetica", "", 10)
                pdf.cell(0, 8, value, border=1, ln=True)
            
            pdf.ln(10)
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 10, "DISTRIBUCION POR NIVEL DE URGENCIA", ln=True, fill=True)
            pdf.set_font("Helvetica", "", 11)
            pdf.ln(5)
            
            dist = datos.get("distribucion_urgencia", [])
            if dist:
                for d in dist:
                    nivel = d.get("nivel_urgencia", "N/A").upper()
                    cantidad = d.get("cantidad", 0)
                    color_map = {"CRITICO": "[CRITICO]", "ALTO": "[ALTO]", "MODERADO": "[MODERADO]", "BAJO": "[BAJO]"}
                    icon = color_map.get(nivel, "")
                    pdf.cell(0, 8, f"{icon} {nivel}: {cantidad} casos", ln=True)
            else:
                pdf.cell(0, 8, "No hay datos disponibles", ln=True)
            
            pdf.ln(10)
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 10, "TENDENCIAS Y ANALISIS", ln=True, fill=True)
            pdf.set_font("Helvetica", "", 11)
            pdf.ln(5)
            
            criticos = metricas.get("criticos", 0)
            altos = metricas.get("altos", 0)
            total = metricas.get("total_triajes", 0)
            if total > 0:
                pct_criticos = (criticos / total) * 100
                pct_altos = (altos / total) * 100
                pdf.cell(0, 7, f"Porcentaje Casos Criticos: {pct_criticos:.1f}%", ln=True)
                pdf.cell(0, 7, f"Porcentaje Casos Altos: {pct_altos:.1f}%", ln=True)
                pdf.ln(3)
                if pct_criticos > 10:
                    pdf.set_text_color(200, 0, 0)
                    pdf.cell(0, 8, "ALERTA: Nivel critico elevado", ln=True)
                    pdf.set_text_color(0, 0, 0)
                else:
                    pdf.set_text_color(0, 128, 0)
                    pdf.cell(0, 8, "Estado: Normal", ln=True)
                    pdf.set_text_color(0, 0, 0)
            
            pdf.ln(15)
            pdf.set_draw_color(39, 174, 96)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(128, 128, 128)
            pdf.cell(0, 6, "Este reporte fue generado automaticamente por el Sistema de Triaje Clinico Asistido por IA", ln=True, align="C")
            pdf.cell(0, 6, "Hospital Central - Departamento de Gestion", ln=True, align="C")
            
            return pdf.output()
        
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            csv_data = f"REPORTE MENSUAL - {mes_seleccionado}\n"
            csv_data += "=" * 50 + "\n"
            csv_data += f"Periodo: {mes_seleccionado}\n"
            csv_data += f"Total Triajes,{metricas.get('total_triajes', 0)}\n"
            csv_data += f"Criticos,{metricas.get('criticos', 0)}\n"
            csv_data += f"Altos,{metricas.get('altos', 0)}\n"
            csv_data += f"Moderados,{metricas.get('moderados', 0)}\n"
            csv_data += f"Bajos,{metricas.get('bajos', 0)}\n"
            csv_data += "\nDistribucion por Urgencia\n"
            csv_data += "Nivel,Cantidad\n"
            for d in datos_gestion.get("distribucion_urgencia", []):
                csv_data += f"{d.get('nivel_urgencia', '')},{d.get('cantidad', 0)}\n"
            
            st.download_button(
                label="📥 Descargar CSV",
                data=csv_data,
                file_name=f"reporte_mensual_{mes_seleccionado}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_exp2:
            pdf_data = generar_pdf_gestion_profesional(datos_gestion, metricas, mes_seleccionado)
            if isinstance(pdf_data, bytearray):
                pdf_data = bytes(pdf_data)
            st.download_button(
                label="📄 Descargar PDF",
                data=pdf_data,
                file_name=f"reporte_mensual_{mes_seleccionado}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.warning("No hay datos disponibles para el mes seleccionado.")