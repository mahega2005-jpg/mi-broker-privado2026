import streamlit as st
import pandas as pd

# Configuración de la página y layout
st.set_page_config(page_title="Mi Broker Privado", page_icon="🛡️", layout="centered")

# --- ESTILOS CSS: FONDO ANTERIOR + PANEL CLARO + PESTAÑAS SUAVES SUTILMENTE SOMBREADAS ---
st.markdown("""
<style>
    /* Fondo general de la aplicación */
    .stApp {
        background-color: #0b0f19;
        color: #f0f6fc;
    }
    
    /* Contenedores y tarjetas transparentes */
    div.stMarkdownContainer, div.stDataFrame {
        background-color: transparent;
    }
    
    /* Pestañas superiores estilizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #161b22;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #30363d;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #21262d;
        border-radius: 8px;
        color: #8b949e !important;
        padding: 10px 16px;
        font-weight: 600;
        font-size: 14px;
        border: 1px solid #30363d;
    }
    /* Pestaña seleccionada: Sutilmente sombreada y sin azul fuerte */
    .stTabs [aria-selected="true"] {
        background-color: #30363d !important;
        color: #ffffff !important;
        border-color: #8b949e !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }

    /* Botones principales y de la barra lateral */
    .stButton button {
        background-color: #21262d;
        color: #ffffff;
        border: 1px solid #30363d;
        border-radius: 8px;
        font-weight: 500;
    }
    .stButton button:hover {
        background-color: #30363d;
        border-color: #8b949e;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAR ESTADOS DE SESIÓN ---
if 'historico_consultas' not in st.session_state:
    st.session_state.historico_consultas = []

if 'cartera_vigilada' not in st.session_state:
    st.session_state.cartera_vigilada = [
        {'ISIN': 'IE00BFPM9N11', 'Nombre': 'Vanguard Global Stock Index Inst Plus EUR Acc', 'Suelo_%': -10.0, 'Techo_%': 25.0, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': 4.5},
        {'ISIN': 'IE00BGCZOB53', 'Nombre': 'Vanguard Global Bond Index Inst Plus EUR Hgd', 'Suelo_%': -8.0, 'Techo_%': 15.0, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': -2.1}
    ]

if 'prueba_correo_enviada' not in st.session_state:
    st.session_state.prueba_correo_enviada = False

# Comprobación automática de bandas
alerta_detectada = False
fondo_alerta = None
for item in st.session_state.cartera_vigilada:
    if item['Rentabilidad_Actual_%'] <= item['Suelo_%'] or item['Rentabilidad_Actual_%'] >= item['Techo_%']:
        alerta_detectada = True
        fondo_alerta = item
        break

# --- CABECERA Y LOGOTIPO CON PANEL CENTRAL EN AZUL MÁS CLARO ---
st.markdown("""
<div style="background: linear-gradient(135deg, #1f3a60, #162a45); padding: 25px; border-radius: 12px; text-align: center; color: white; border: 1px solid #3b82f6; box-shadow: 0px 4px 20px rgba(0,0,0,0.4);">
    <div style="font-size: 38px; margin-bottom: 5px;">🛡️📈</div>
    <h2 style="margin: 0; font-size: 24px; letter-spacing: 1.5px; color: #93c5fd;">MI BROKER PRIVADO</h2>
    <p style="margin: 6px 0 0 0; font-size: 13px; color: #cbd5e1;">Panel Táctico • Core en Indexa Capital • Vigilancia de Bandas 24h</p>
</div>
<br>
""", unsafe_allow_html=True)

# --- BASE DE DATOS MAESTRA ---
data_fondos = {
    'Nombre del Fondo': [
        'Vanguard Global Stock Index Inst Plus EUR Acc', 
        'Vanguard Global Bond Index Inst Plus EUR Hgd', 
        'Polar Capital Biotechnology EUR R Acc',
        'Pictet - Security P EUR',
        'Amundi Index MSCI World AE-C',
        'Banco Tradicional Cartera Activa (Ejemplo)'
    ],
    'ISIN': [
        'IE00BFPM9N11', 'IE00BGCZOB53', 'IE00B43VBZ18', 'LU0503631872', 'LU1681048899', 'ES0111222333'
    ],
    'Tipo': [
        'Renta Variable Global (Core)', 'Renta Fija Global (Core)', 'Biotecnología (Satélite)', 'Ciberseguridad (Satélite)', 'Indexado Global', 'Gestión Activa'
    ],
    'Operador / Comercializador España': [
        'Indexa Capital (Tu Núcleo Core)', 'Indexa Capital (Tu Núcleo Core)', 'MyInvestor / Renta 4', 'MyInvestor / IronIA / Renta 4', 'MyInvestor / Openbank', 'Banco Comercial Tradicional'
    ],
    'Permite Transferencia/Traspaso': [
        'Sí (Traspasable sin peaje fiscal)', 'Sí (Traspasable sin peaje fiscal)', 'Sí (Traspasable)', 'Sí (Traspasable)', 'Sí (Traspasable)', 'Sí (Sujeto a comisiones)'
    ],
    'TER_%': [0.06, 0.10, 1.25, 1.00, 0.30, 1.85],       
    'YTD_2026_%': [18.55, -3.35, 11.5, 14.2, 7.9, 2.1],
    '2025_%': [6.73, 2.89, 14.0, 22.5, 19.2, 4.2],
    '2024_%': [26.59, 0.88, 8.5, 25.1, 21.9, 5.0],
    '2023_%': [19.63, 4.74, 6.2, 18.0, 14.8, 3.5],
    '2022_%': [-12.79, -15.03, -12.4, -20.1, -18.5, -8.5],
    '2021_%': [27.5, 5.1, 10.1, 31.0, 27.1, 6.1]
}

df_master = pd.DataFrame(data_fondos)

# --- VENTANA FLOTANTE DE ALERTA URGENTE ---
@st.dialog("🚨 ¡ALERTA URGENTE: BANDA DE CONTROL SUPERADA!")
def mostrar_alerta_urgente(f_alerta):
    st.markdown(f"### Fondo afectado: **{f_alerta['Nombre']}**")
    st.markdown(f"**ISIN:** `{f_alerta['ISIN']}`")
    st.markdown("---")
    st.info("📨 **Aviso interno registrado para:** `mahega2005@gmail.com`")
    st.markdown(f"""
    * **Rentabilidad Actual:** `{f_alerta['Rentabilidad_Actual_%']}%`
    * **Límite Suelo Configurado:** `{f_alerta['Suelo_%']}%` (¡Superado por debajo!)
    * **Acción Sugerida:** Revisar la posición y valorar reequilibrio o traspaso exento.
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✖️ Cerrar y Entendido", type="primary", use_container_width=True):
        st.rerun()

