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

# --- BASE DE DATOS AMPLIADA CON FONDOS REALES DE BAJO COSTE ---
data_fondos = {
    'Nombre del Fondo': [
        'Vanguard Global Stock Index EUR Acc', 
        'iShares Developed World Index (IE) D Acc', 
        'Fidelity MSCI World Index Fund EUR P',
        'Vanguard U.S. 500 Stock Index Fund',
        'Banco Tradicional Cartera Activa (Ejemplo)',  
        'Mixto Comercial Banco X (Ejemplo)'             
    ],
    'ISIN': [
        'IE00B03HD191', 'IE00BD0NCM55', 'IE00BYX5NX33', 'IE0032620787', 'ES0111222333', 'ES0444555666'
    ],
    'Tipo': [
        'Indexado Global (Vanguard)', 'Indexado Global (iShares)', 'Indexado Global (Fidelity)', 'Indexado S&P 500 (Vanguard)', 'Gestión Activa (Banco)', 'Gestión Activa (Banco)'
    ],
    'TER_Anual_%': [0.18, 0.12, 0.10, 0.10, 1.85, 2.10],       
    'Rentabilidad_3A_%': [16.86, 16.93, 16.88, 17.58, 4.5, 3.2]    
}

df_master = pd.DataFrame(data_fondos)

# --- BARRA LATERAL: PARÁMETROS DE BÚSQUEDA ---
st.sidebar.header("🔍 Parámetros de Búsqueda")
busqueda_texto = st.sidebar.text_input("Buscar por Nombre o ISIN", "").strip()
ter_limite = st.sidebar.slider("Filtrar por TER Máximo (%)", min_value=0.0, max_value=3.0, value=3.0, step=0.05)

# --- APLICAR FILTROS ---
df_filtrado = df_master.copy()

# Filtro por deslizador de TER
df_filtrado = df_filtrado[df_filtrado['TER_Anual_%'] <= ter_limite]

# Filtro por caja de texto (Nombre o ISIN)
if busqueda_texto:
    mask = df_filtrado['Nombre del Fondo'].str.contains(busqueda_texto, case=False, na=False) | \
           df_filtrado['ISIN'].str.contains(busqueda_texto, case=False, na=False)
    df_filtrado = df_filtrado[mask]

# --- VISUALIZACIÓN DE RESULTADOS ---
st.subheader("📊 Resultados de la Búsqueda")
if not df_filtrado.empty:
    st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
else:
    st.warning("No se ha encontrado ningún fondo con esos criterios de búsqueda.")

# --- SECCIONES FIJAS DE CONTROL ---
st.markdown("---")
st.subheader("✅ Cartera Optimizada (Bajos Costes / TER ≤ 0.50%)")
cartera_optimizada = df_master[df_master['TER_Anual_%'] <= 0.50]
st.dataframe(cartera_optimizada.reset_index(drop=True), use_container_width=True)

st.subheader("❌ Fondos Descartados (Banca Tradicional / TER > 0.50%)")
fondos_descartados = df_master[df_master['TER_Anual_%'] > 0.50]
st.dataframe(fondos_descartados[['Nombre del Fondo', 'Tipo', 'TER_Anual_%']].reset_index(drop=True), use_container_width=True)

