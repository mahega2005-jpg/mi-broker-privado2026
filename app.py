import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Mi Broker Privado", page_icon="🛡️", layout="centered")

# --- CABECERA Y LOGOTIPO ---
st.markdown("""
<div style="background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); padding: 25px; border-radius: 15px; text-align: center; color: white; font-family: sans-serif; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);">
    <div style="font-size: 40px; margin-bottom: 5px;">🛡️📈</div>
    <h2 style="margin: 0; font-size: 24px; letter-spacing: 1px;">MI BROKER PRIVADO</h2>
    <p style="margin: 5px 0 0 0; font-size: 13px; color: #a2dbfa;">Panel de Cartera Satélite & Control de Costes</p>
    <div style="margin-top: 15px; display: inline-block; background: #00b09b; color: white; padding: 6px 15px; border-radius: 15px; font-size: 11px; font-weight: bold;">
        ESTADO: PROTEGIDO (FILTRO ANTI-BANCA TRADICIONAL ACTIVO)
    </div>
</div>
<br>
""", unsafe_allow_html=True)

# --- BASE DE DATOS DE TUS FONDOS ---
data_fondos = {
    'Nombre del Fondo': [
        'Vanguard Global Stock Index', 
        'Amundi Index MSCI World', 
        'iShares Developed World Index',
        'Banco Tradicional Cartera Activa',  
        'Mixto Comercial Banco X'             
    ],
    'ISIN': [
        'IE00B03HD191', 'LU1681048899', 'IE00B4L5Y983', 'ES0111222333', 'ES0444555666'
    ],
    'Tipo': [
        'Indexado (Global)', 'Indexado (Global)', 'Indexado (Global)', 'Gestión Activa (Banco)', 'Gestión Activa (Banco)'
    ],
    'TER_Anual_%': [0.18, 0.30, 0.24, 1.85, 2.10],       
    'Rentabilidad_1A_%': [12.4, 11.9, 12.1, 4.5, 3.2]    
}

df_master = pd.DataFrame(data_fondos)

# --- VISUALIZACIÓN DE FILTROS ---
st.subheader("📊 Tus Fondos Seleccionados (Bajos Costes / Estilo Indexa)")
cartera_optimizada = df_master[df_master['TER_Anual_%'] <= 0.50]
st.dataframe(cartera_optimizada.reset_index(drop=True), use_container_width=True)

st.subheader("❌ Fondos Descartados (Banca Tradicional)")
fondos_descartados = df_master[df_master['TER_Anual_%'] > 0.50]
st.dataframe(fondos_descartados[['Nombre del Fondo', 'Tipo', 'TER_Anual_%']].reset_index(drop=True), use_container_width=True)
