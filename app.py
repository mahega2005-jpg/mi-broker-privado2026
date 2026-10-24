# ==============================================================================
# PROYECTO: MI BROKER PRIVADO - PANEL TÁCTICO DE INVERSIÓN
# AUTOR: Bartolomé Marín Hedrera
# DESCRIPCIÓN: Panel de control avanzado en Streamlit para la gestión táctica
#              de fondos de inversión, supervisión de bandas (Suelo/Techo) y
#              análisis de megatendencias bajo un modelo Core-Satellite.
# ==============================================================================

import streamlit as st
import pandas as pd
from datetime import datetime
import zoneinfo

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS (ESTILO SUAVIZADO & ALINEACIÓN PERFECTA)
# ==============================================================================
st.set_page_config(
    page_title="Mi Broker Privado - Panel Táctico",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Estilo General del Fondo y Tipografía Principal */
    .stApp { 
        background-color: #f0f4f9; 
        color: #1f2328; 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Sidebar Personalizado con Gradiente Suave */
    section[data-testid="stSidebar"] { 
        background: linear-gradient(135deg, #dbeafe, #bfdbfe); 
        border-right: 2px solid #93c5fd; 
        padding-top: 10px;
    }
    
    /* Pestañas / Tabs Superiores (Estilo Suavizado y Moderno) */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 6px; 
        background-color: #e2e8f0; 
        padding: 6px; 
        border-radius: 12px; 
        border: 2px solid #cbd5e1; 
    }
    
    .stTabs [data-baseweb="tab"] { 
        background-color: #ffffff; 
        border-radius: 8px; 
        color: #475569 !important; 
        padding: 10px 16px; 
        font-weight: 600; 
        font-size: 14px; 
        border: 1px solid #cbd5e1; 
    }
    
    .stTabs [aria-selected="true"] { 
        background-color: #cbd5e1 !important; 
        color: #0f172a !important; 
        border-color: #94a3b8 !important; 
    }
    
    /* Botones Táctiles Interactivos */
    .stButton button { 
        background-color: #ffffff; 
        color: #1f2328; 
        border: 1px solid #cbd5e1; 
        border-radius: 8px; 
        font-weight: 500; 
        padding: 8px 16px;
    }

    .stButton button:hover {
        border-color: #3b82f6;
        color: #1d4ed8;
    }

    /* Tarjetas del Radar Megatendencial con Altura Fija para Alineación Horizontal Perfecta */
    .trend-card-header {
        background-color: #ffffff;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #cbd5e1;
        min-height: 165px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .fund-box-item {
        background-color: #ffffff;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        min-height: 95px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. FUNCIONES DE SOPORTE Y HORARIOS OFICIALES (ZONA HORARIA ESPAÑA)
# ==============================================================================
def hora_real_espana():
    """Retorna la hora actual exacta en la península ibérica para control de auditoría."""
    tz = zoneinfo.ZoneInfo("Europe/Madrid")
    return datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')


# ==============================================================================
# 3. BASE DE DATOS MAESTRA COMPLETA (2 CORE + 10 TOP MERCADO)
# ==============================================================================
data_12_fondos = {
    'Origen': [
        '📌 En Cartera (Core)', '📌 En Cartera (Core)',
        '⭐ Top Mercado', '⭐ Top Mercado', '⭐ Top Mercado', '⭐ Top Mercado',
        '⭐ Top Mercado', '⭐ Top Mercado', '⭐ Top Mercado', '⭐ Top Mercado',
        '⭐ Top Mercado', '⭐ Top Mercado'
    ],
    'ISIN': [
        'IE00BFPM9N11', 'IE00BGCZOB53',
        'LU1681048899', 'IE00B03HD191', 'LU0503631872', 'IE00B43VBZ18',
        'ES0114105030', 'IE00B03HCZ61', 'LU0996182563', 'LU1121307729',
        'IE00B3WVRB16', 'ES0111222333'
    ],
    'Nombre del Fondo': [
        'Vanguard Global Stock Index Inst Plus EUR Acc', 
        'Vanguard Global Bond Index Inst Plus EUR Hgd', 
        'Amundi Index MSCI World AE-C',
        'Vanguard US 500 Stock Index EUR Acc',
        'Pictet - Security P EUR',
        'Polar Capital Biotechnology EUR R Acc',
        'DWS Investments Alpha Opportunities',
        'Vanguard European Stock Index EUR Acc',
        'Fidelity Funds - Global Technology A-ACC-EUR',
        'Abante Global Funds Spanish Opportunities C EUR',
        'Polar Capital Biotechnology I EUR Dis',
        'Banco Tradicional Cartera Activa'
    ],
    'Categoría / Tipo': [
        'Renta Variable Global', 'Renta Fija Global',
        'Indexado Global (MSCI World)', 'Indexado S&P 500', 'Ciberseguridad & Seguridad', 'Biotecnología & Salud',
        'Retorno Absoluto / Multi-Activo', 'Renta Variable Europa', 'Tecnología Global', 'Renta Variable España',
        'Biotecnología (Clase I Dist)', 'Gestión Activa Tradicional'
    ],
    'Comercializador España': [
        'Indexa Capital', 'Indexa Capital',
        'MyInvestor / Openbank', 'MyInvestor / Renta 4', 'MyInvestor / IronIA', 'MyInvestor / Renta 4',
        'Renta 4 / Allfunds', 'MyInvestor / Renta 4', 'MyInvestor / Mapfre', 'Abante Asesores',
        'MyInvestor / Renta 4', 'Banco Tradicional'
    ],
    'Traspasable': ['Sí', 'Sí', 'Sí', 'Sí', 'Sí', 'Sí', 'Sí', 'Sí', 'Sí', 'Sí', 'Sí', 'Sí'],
    'Min_Inversion': ['Desde 10€', 'Desde 10€', 'Desde 10€', '100€', '1 Participación', '1 Participación', '100€', '100€', '1 Participación', '1 Participación', '1 Participación', 'Desde 500€'],
    'TER_%': [0.06, 0.10, 0.30, 0.10, 1.00, 1.25, 0.65, 0.12, 1.05, 1.35, 1.00, 1.85],
    'YTD_2026_%': [18.55, -3.35, 17.90, 21.40, 14.20, 11.50, 6.80, 12.10, 24.50, 8.20, 10.90, -2.10],
    '2025_%': [6.73, 2.89, 19.20, 23.50, 22.50, 14.00, 5.40, 11.20, 28.10, 9.10, 12.50, 4.20],
    '2024_%': [26.59, 0.88, 21.90, 26.80, 25.10, 8.50, 7.10, 15.80, 32.40, 11.40, 24.85, 5.00],
    '2023_%': [19.63, 4.74, 14.80, 21.20, 18.00, 6.20, 4.20, 12.50, 36.10, 14.20, 14.89, 3.50]
}
df_master = pd.DataFrame(data_12_fondos)


# ==============================================================================
# 4. GESTIÓN DE ESTADOS DE SESIÓN (SESSION STATE)
# ==============================================================================
if 'historico_consultas' not in st.session_state:
    st.session_state.historico_consultas = []

if 'cartera_vigilada' not in st.session_state:
    st.session_state.cartera_vigilada = pd.DataFrame([
        {'ISIN': 'IE00BFPM9N11', 'Nombre': 'Vanguard Global Stock Index Inst Plus EUR Acc', 'Suelo_%': -10.0, 'Techo_%': 25.0, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': 18.55},
        {'ISIN': 'IE00BGCZOB53', 'Nombre': 'Vanguard Global Bond Index Inst Plus EUR Hgd', 'Suelo_%': -8.0, 'Techo_%': 15.0, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': -3.35}
    ])

if 'notificacion_actualizado' not in st.session_state:
    st.session_state.notificacion_actualizado = False

if 'isin_preseleccionado' not in st.session_state:
    st.session_state.isin_preseleccionado = ""


# ==============================================================================
# 5. CABECERA TÁCTICA SUPERIOR
# ==============================================================================
col_head1, col_head2 = st.columns([4, 1])
h_actual = hora_real_espana()

with col_head1:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #dbeafe, #bfdbfe); padding: 20px; border-radius: 12px; text-align: center; color: #1e3a8a; border: 2px solid #3b82f6;">
        <div style="font-size: 32px; margin-bottom: 3px;">🛡️📈</div>
        <h2 style="margin: 0; font-size: 24px; color: #1e40af; font-weight: 700;">MI BROKER PRIVADO</h2>
        <p style="margin: 6px 0 0 0; font-size: 14px; color: #1d4ed8; font-weight: 600;">Panel Táctico • Hora Oficial España: {h_actual}</p>
    </div>
    """, unsafe_allow_html=True)

with col_head2:
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Actualizar Datos", use_container_width=True, help="Rec
