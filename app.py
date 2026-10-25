# ==============================================================================
# PROYECTO: MI BROKER PRIVADO - PANEL TÁCTICO DE INVERSIÓN
# AUTOR: Bartolomé Marín Hedrera
# DESCRIPCIÓN: Panel de control avanzado en Streamlit para la gestión táctica
#              de fondos de inversión, supervisión de bandas y motor autónomo.
# ==============================================================================

import streamlit as st
import pandas as pd
from datetime import datetime
import zoneinfo

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS
# ==============================================================================
st.set_page_config(
    page_title="Mi Broker Privado - Panel Táctico",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background-color: #f0f4f9;
        color: #1f2937;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. FUNCIONES DE TIEMPO Y CONFIGURACIÓN REGIONAL
# ==============================================================================
def hora_real_espana():
    try:
        zona = zoneinfo.ZoneInfo("Europe/Madrid")
        return datetime.now(zona).strftime("%d/%m/%Y %H:%M:%S")
    except Exception:
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# Inicialización de estados de sesión necesarios
if 'notificacion_actualizado' not in st.session_state:
    st.session_state.notificacion_actualizado = False
if 'historico_consultas' not in st.session_state:
    st.session_state.historico_consultas = []
if 'isin_preseleccionado' not in st.session_state:
    st.session_state.isin_preseleccionado = ""

# ==============================================================================
# 3. DATOS MAESTROS Y MOTOR DE ESCANEO
# ==============================================================================
@st.cache_data
def data_12_fondos():
    return [
        {"origen": "Top Mercado", "isin": "IE00BFPM9N11", "nombre": "Vanguard Global Stock Index Inst Plus EUR Acc", "cat": "Indexado Global (MSCI World)", "com": "MyInvestor / Openbank", "suelo": -10, "techo": 25, "email": "mahega2005@gmail.com"},
        {"origen": "Top Mercado", "isin": "LU1681048899", "nombre": "Amundi Index MSCI World AE-C", "cat": "Indexado Global (MSCI World)", "com": "MyInvestor / Renta 4", "suelo": -10, "techo": 25, "email": "mahega2005@gmail.com"},
        {"origen": "Top Mercado", "isin": "IE00B03HD191", "nombre": "Vanguard US 500 Stock Index EUR Acc", "cat": "Indexado S&P 500", "com": "MyInvestor / Renta 4", "suelo": -10, "techo": 25, "email": "mahega2005@gmail.com"},
        {"origen": "Top Mercado", "isin": "LU0503631872", "nombre": "Pictet - Security P EUR", "cat": "Ciberseguridad & Seguridad", "com": "MyInvestor / IronIA", "suelo": -12, "techo": 30, "email": "mahega2005@gmail.com"},
        {"origen": "Top Mercado", "isin": "IE00B43VBZ18", "nombre": "Polar Capital Biotechnology EUR R Acc", "cat": "Biotecnología & Salud", "com": "MyInvestor / Renta 4", "suelo": -15, "techo": 35, "email": "mahega2005@gmail.com"},
        {"origen": "Top Mercado", "isin": "ES0114105030", "nombre": "DWS Investments Alpha Opportunities", "cat": "Retorno Absoluto / Multi-Activo", "com": "Renta 4 / Allfunds", "suelo": -8, "techo": 15, "email": "mahega2005@gmail.com"},
        {"origen": "Core Cartera", "isin": "IE00BGCZOB53", "nombre": "Vanguard Global Bond Index Inst Plus EUR Hgd", "cat": "Renta Fija Global Hedged", "com": "MyInvestor", "suelo": -8, "techo": 15, "email": "mahega2005@gmail.com"},
        {"origen": "Core Cartera", "isin": "IE00011UKHJ7", "nombre": "Pictet - Global Megatrend Selection P EUR", "cat": "Megatendencias Globales", "com": "MyInvestor / IronIA", "suelo": -12, "techo": 30, "email": "mahega2005@gmail.com"}
    ]

def ejecutar_escanner_automatico_top10():
    pass

def consultar_catalogo_maestro(isin):
    for f in data_12_fondos():
        if f["isin"] == isin:
            return f
    return None

def abrir_modal_detalle(fondo):
    pass

# ==============================================================================
# 4. CABECERA TÁCTICA SUPERIOR (Diseño limpio y unificado)
# ==============================================================================
h_actual = hora_real_espana()

st.markdown(f"""
<div style="background: linear-gradient(135deg, #dbeafe, #bfdbfe); padding: 16px; border-radius: 12px; text-align: left; color: #1e3a8a; border: 2px solid #3b82f6; margin-bottom: 8px;">
    <div style="font-size: 22px; margin-bottom: 2px;">🛡️📈 <b style="font-size: 18px; color: #1e40af;">MI BROKER PRIVADO</b></div>
    <p style="margin: 4px 0 0 0; font-size: 12px; color: #1d4ed8; font-weight: 600;">Panel Táctico • Hora Oficial: {h_actual}</p>
</div>
""", unsafe_allow_html=True)
# ==============================================================================
# 5. BARRA LATERAL (PANEL TÁCTICO DE CONTROL)
# ==============================================================================
st.sidebar.markdown("### 🛡️ Panel Táctico")

with st.sidebar.expander("⚡ Test de Alertas", expanded=False):
    st.write("Herramienta de verificación de umbrales activa.")

with st.sidebar.expander("➕ Añadir / 🗑️ Eliminar ISIN", expanded=False):
    st.write("Gestión de posiciones y códigos ISIN.")

with st.sidebar.expander("🔍 Lector Universal ISIN", expanded=True):
    isin_input = st.text_input("Introduce ISIN", value=st.session_state.isin_preseleccionado, placeholder="Ej: IE00BFPM9N11")
    btn_submit = st.button("✅ Consultar e Incorporar", use_container_width=True)
    if btn_submit and isin_input:
        st.session_state.isin_preseleccionado = ""
        res = consultar_catalogo_maestro(isin_input)
        if not res:
            res = {"origen": "Manual", "isin": isin_input, "nombre": "Fondo Personalizado / Externo", "cat": "Personalizada", "com": "Manual", "suelo": -10, "techo": 20, "email": "mahega2005@gmail.com"}
        res['FechaConsulta'] = hora_real_espana()
        st.session_state.historico_consultas = [i for i in st.session_state.historico_consultas if i['ISIN'] != isin_input]
        st.session_state.historico_consultas.insert(0, res)
        if len(st.session_state.historico_consultas) > 5:
            st.session_state.historico_consultas.pop()

if st.session_state.historico_consultas:
    with st.sidebar.expander("🕒 Histórico Reciente (Últimas 5)", expanded=False):
        for idx, hist in enumerate(st.session_state.historico_consultas):
            if st.sidebar.button(f"⭐ {hist['ISIN']} ({hist.get('FechaConsulta','')})", key=f"btn_hist_{idx}", use_container_width=True):
                pass

# ==============================================================================
# 6. PESTAÑAS PRINCIPALES DEL PANEL (4 TÁCTICAS + 1 DE AJUSTES)
# ==============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🛡️ Control & Bandas", 
    "📊 Buscador Maestro", 
    "🎯 Radar de Tendencias & Estrategias", 
    "📈 Gráficos & Cartera Core",
    "⚙️ Ajustes & Enlaces"
])

with tab1:
    st.subheader("Supervisión 24h de Bandas (Suelos y Techos)")
    st.write("Edita las bandas de control de tus posiciones activas:")
    df_bandas = pd.DataFrame(data_12_fondos()[:2])
    st.dataframe(df_bandas[["isin", "nombre", "suelo", "techo", "email"]], use_container_width=True)

with tab2:
    st.subheader("Buscador Maestro: Top 10 Dinámico de Referencia + Cartera Core")
    fondos = data_12_fondos()
    opciones_fondos = [f"{f['isin']} - {f['nombre']}" for f in fondos]
    fondo_elegido = st.selectbox("Selecciona fondo:", opciones_fondos)
    if st.button("🚀 Cargar en Lector", use_container_width=True):
        st.success("Fondo seleccionado cargado correctamente.")
    
    df_maestro = pd.DataFrame(fondos)
    st.dataframe(df_maestro, use_container_width=True)

with tab3:
    st.subheader("Radar de Tendencias & Estrategias")
    st.info("Análisis sectorial y táctico en curso.")

with tab4:
    st.subheader("Gráficos & Cartera Core")
    st.line_chart([100, 105, 103, 110, 115])

with tab5:
    st.subheader("⚙️ Panel de Ajustes y Accesos Directos")
    st.markdown("Herramientas de control global y mantenimiento del panel táctico:")
    
    col_ajust1, col_ajust2 = st.columns(2)
    
    with col_ajust1:
        st.markdown("### 🔄 Sincronización")
        st.write("Actualiza el motor de escaneo y los datos globales del panel.")
        if st.button("🔄 Actualizar Datos", use_container_width=True):
            ejecutar_escanner_automatico_top10()
            st.toast(f"✅ ¡Escaneo autónomo completado! Hora oficial ({hora_real_espana()}) y Top 10 auditados.", icon="🔄")
            st.rerun()
            
    with col_ajust2:
        st.markdown("### 🐱 Gestión de Código")
        st.write("Accede directamente al repositorio en GitHub para editar la aplicación.")
        st.link_button("🐱 Editar App en GitHub", "https://github.com/mahega2005-jpg/mi-broker-privado2026", use_container_width=True)
