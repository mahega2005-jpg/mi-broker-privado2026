import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Mi Broker Privado", page_icon="🛡️", layout="centered")

# --- CABECERA Y LOGOTIPO ---
st.markdown("""
<div style="background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); padding: 25px; border-radius: 15px; text-align: center; color: white; font-family: sans-serif; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);">
    <div style="font-size: 40px; margin-bottom: 5px;">🛡️📈</div>
    <h2 style="margin: 0; font-size: 24px; letter-spacing: 1px;">MI BROKER PRIVADO</h2>
    <p style="margin: 5px 0 0 0; font-size: 13px; color: #a2dbfa;">Panel de Control, Cartera Eficiente & Control de Costes (España)</p>
    <div style="margin-top: 15px; display: inline-block; background: #00b09b; color: white; padding: 6px 15px; border-radius: 15px; font-size: 11px; font-weight: bold;">
        ESTADO: GESTIÓN DE CARTERA ACTIVA 🇪🇸
    </div>
</div>
<br>
""", unsafe_allow_html=True)

# --- BASE DE DATOS DE TU CARTERA Y FONDOS DE REFERENCIA ---
data_fondos = {
    'Nombre del Fondo': [
        'Vanguard Global Stock Index Institutional Plus EUR', 
        'Vanguard Global Bond Index Institutional Plus EUR', 
        'Polar Capital Biotechnology EUR R Acc',
        'Pictet - Security P EUR',
        'Banco Tradicional Cartera Activa (Ejemplo)'
    ],
    'ISIN': [
        'IE00BFPM9N11', 'IE00BGCZOB53', 'IE00B43VBZ18', 'LU0503631872', 'ES0111222333'
    ],
    'Tipo': [
        'Renta Variable Global', 'Renta Fija Global (Hedged)', 'Biotecnología (Satélite)', 'Ciberseguridad (Satélite)', 'Gestión Activa (Banco)'
    ],
    'TER_%': [0.10, 0.10, 1.25, 1.00, 1.85],       
    'YTD_2026_%': [18.55, -3.35, 11.5, 14.2, 2.1],
    '2025_%': [6.73, 2.89, 14.0, 22.5, 4.2],
    '2024_%': [26.59, 0.88, 8.5, 25.1, 5.0],
    '2023_%': [19.63, 4.74, 6.2, 18.0, 3.5],
    '2022_%': [-12.79, -15.03, -12.4, -20.1, -8.5],
    'Operador / Contratación en España': [
        'MyInvestor / Renta 4 (Transferencia bancaria)', 
        'MyInvestor / Renta 4 (Transferencia bancaria)', 
        'MyInvestor / Openbank / Bróker europeo', 
        'MyInvestor / Allfunds / Renta 4', 
        'Tu Banco Tradicional (Evitar)'
    ]
}

df_master = pd.DataFrame(data_fondos)

# --- BARRA LATERAL IZQUIERDA: PARÁMETROS Y FILTROS ---
st.sidebar.header("🔍 Parámetros de Búsqueda")
busqueda_texto = st.sidebar.text_input("Buscar por Nombre o ISIN", "").strip()
ter_limite = st.sidebar.slider("Filtrar por TER Máximo (%)", min_value=0.0, max_value=3.0, value=3.0, step=0.05)

st.sidebar.markdown("---")
st.sidebar.header("🏆 Filtros de Cartera")
solo_top_10 = st.sidebar.checkbox("Mostrar solo Top Mejores Fondos", value=False)
criterio_top = st.sidebar.selectbox("Ordenar TOP por:", ["YTD 2026", "Rentabilidad 2025", "Menores Comisiones (TER)"])

# --- APLICAR FILTROS ---
df_filtrado = df_master.copy()
df_filtrado = df_filtrado[df_filtrado['TER_%'] <= ter_limite]

if busqueda_texto:
    mask = df_filtrado['Nombre del Fondo'].str.contains(busqueda_texto, case=False, na=False) | \
           df_filtrado['ISIN'].str.contains(busqueda_texto, case=False, na=False)
    df_filtrado = df_filtrado[mask]

if solo_top_10:
    if criterio_top == "YTD 2026":
        df_filtrado = df_filtrado.sort_values(by='YTD_2026_%', ascending=False).head(10)
    elif criterio_top == "Rentabilidad 2025":
        df_filtrado = df_filtrado.sort_values(by='2025_%', ascending=False).head(10)
    elif criterio_top == "Menores Comisiones (TER)":
        df_filtrado = df_filtrado.sort_values(by='TER_%', ascending=True).head(10)

# --- VISUALIZACIÓN DE RESULTADOS ---
st.subheader("📊 Resultados de la Búsqueda y Desglose Histórico")
if not df_filtrado.empty:
    st.dataframe(df_filtrado[['Nombre del Fondo', 'ISIN', 'Tipo', 'TER_%', 'YTD_2026_%', '2025_%', '2024_%', 'Operador / Contratación en España']].reset_index(drop=True), use_container_width=True)
else:
    st.warning("No se ha encontrado ningún fondo con esos criterios de búsqueda en la barra lateral.")

# --- SECCIONES DE CONTROL FIJAS ---
st.markdown("---")
st.subheader("✅ Cartera Core & Renta Fija (Bajos Costes / TER ≤ 0.50%)")
st.dataframe(df_master[df_master['TER_%'] <= 0.50][['Nombre del Fondo', 'ISIN', 'Tipo', 'TER_%', 'Operador / Contratación en España']].reset_index(drop=True), use_container_width=True)

st.subheader("🚀 Satélites Temáticos de Alto Crecimiento")
st.dataframe(df_master[(df_master['TER_%'] > 0.50) & (df_master['TER_%'] <= 1.50)][['Nombre del Fondo', 'ISIN', 'Tipo', 'TER_%', 'Operador / Contratación en España']].reset_index(drop=True), use_container_width=True)

st.subheader("❌ Fondos Descartados (Banca Tradicional)")
st.dataframe(df_master[df_master['TER_%'] > 1.50][['Nombre del Fondo', 'ISIN', 'Tipo', 'TER_%', 'Operador / Contratación en España']].reset_index(drop=True), use_container_width=True)
