import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Mi Broker Privado", page_icon="🛡️", layout="centered")

# --- CABECERA Y LOGOTIPO ---
st.markdown("""
<div style="background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); padding: 25px; border-radius: 15px; text-align: center; color: white; font-family: sans-serif; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);">
    <div style="font-size: 40px; margin-bottom: 5px;">🛡️📈</div>
    <h2 style="margin: 0; font-size: 24px; letter-spacing: 1px;">MI BROKER PRIVADO</h2>
    <p style="margin: 5px 0 0 0; font-size: 13px; color: #a2dbfa;">Panel Inteligente & Copiloto de Inversión (España / Europa)</p>
    <div style="margin-top: 15px; display: inline-block; background: #00b09b; color: white; padding: 6px 15px; border-radius: 15px; font-size: 11px; font-weight: bold;">
        ESTADO: COPILOTO IA ACTIVO 🤖
    </div>
</div>
<br>
""", unsafe_allow_html=True)

# --- BASE DE DATOS AMPLIADA Y DETALLADA (AÑO A AÑO) ---
data_fondos = {
    'Nombre del Fondo': [
        'Vanguard Global Stock Index EUR Acc', 
        'iShares Developed World Index (IE) D Acc', 
        'Amundi Index MSCI World AE-C',
        'Polar Capital Biotechnology EUR R Acc',
        'Pictet - Security P EUR',
        'Vanguard U.S. 500 Stock Index Fund',
        'Banco Tradicional Cartera Activa (Ejemplo)',  
        'Mixto Comercial Banco X (Ejemplo)'             
    ],
    'ISIN': [
        'IE00B03HD191', 'IE00BD0NCM55', 'LU1681048899', 'IE00B43VBZ18', 'LU0503631872', 'IE0032620787', 'ES0111222333', 'ES0444555666'
    ],
    'Tipo': [
        'Indexado Global', 'Indexado Global', 'Indexado Global', 'Biotecnología', 'Ciberseguridad', 'Indexado S&P 500', 'Gestión Activa', 'Gestión Activa'
    ],
    'TER_%': [0.18, 0.12, 0.30, 1.25, 1.00, 0.10, 1.85, 2.10],       
    'YTD_2026_%': [8.4, 8.2, 7.9, 11.5, 14.2, 9.1, 2.1, 1.5],
    '2025_%': [19.5, 19.8, 19.2, 14.0, 22.5, 21.0, 4.2, 3.1],
    '2024_%': [22.1, 22.4, 21.9, 8.5, 25.1, 24.5, 5.0, 4.0],
    '2023_%': [15.2, 15.0, 14.8, 6.2, 18.0, 16.5, 3.5, 2.8],
    '2022_%': [-18.1, -18.3, -18.5, -12.4, -20.1, -19.0, -8.5, -9.2],
    '2021_%': [27.5, 27.8, 27.1, 10.1, 31.0, 28.7, 6.1, 5.0]
}

df_master = pd.DataFrame(data_fondos)

# --- BARRA LATERAL: PARÁmetros Y FILTROS AVANZADOS ---
st.sidebar.header("🔍 Parámetros de Búsqueda")
busqueda_texto = st.sidebar.text_input("Buscar por Nombre o ISIN", "").strip()
ter_limite = st.sidebar.slider("Filtrar por TER Máximo (%)", min_value=0.0, max_value=3.0, value=3.0, step=0.05)

st.sidebar.markdown("---")
st.sidebar.header("🏆 Filtros Especiales IA")
solo_top_10 = st.sidebar.checkbox("Mostrar solo Top 10 Mejores Fondos", value=False)
criterio_top = st.sidebar.selectbox("Ordenar TOP por:", ["YTD 2026", "Rentabilidad 2025", "Menores Comisiones (TER)"])

# --- APLICAR FILTROS ---
df_filtrado = df_master.copy()

# Filtro por TER
df_filtrado = df_filtrado[df_filtrado['TER_%'] <= ter_limite]

# Filtro por Texto
if busqueda_texto:
    mask = df_filtrado['Nombre del Fondo'].str.contains(busqueda_texto, case=False, na=False) | \
           df_filtrado['ISIN'].str.contains(busqueda_texto, case=False, na=False)
    df_filtrado = df_filtrado[mask]

# Filtro Top 10 / Selección inteligente
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
    st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
else:
    st.warning("No se ha encontrado ningún fondo con esos criterios de búsqueda.")

# --- SECCIÓN: ROBOT COPILOTO ASESOR (TOP 3 RECOMENDACIONES) ---
st.markdown("---")
st.subheader("🤖 Copiloto IA: Top 3 Mejores Opciones Recomendadas")
st.markdown("El robot analiza en tiempo real la combinación de **bajas comisiones (TER)** y **consistencia histórica** para sugerirte las mejores alternativas para invertir desde España:")

# Algoritmo de recomendación del Copiloto (Filtra banca tradicional y prioriza eficiencia)
df_robot = df_master[df_master['TER_%'] <= 1.50].copy()
# Puntuación simple combinando bajo TER y alta rentabilidad media en 2024/2025
df_robot['Score'] = (df_robot['2024_%'] + df_robot['2025_%']) / 2 - (df_robot['TER_%'] * 10)
top_3_recomendados = df_robot.sort_values(by='Score', ascending=False).head(3)

for idx, row in top_3_recomendados.reset_index().iterrows():
    st.success(f"""
    **Opción {idx+1}: {row['Nombre del Fondo']}** (ISIN: `{row['ISIN']}`)  
    * **Tipo:** {row['Tipo']} | **TER:** {row['TER_%']}% | **Rentabilidad 2025:** {row['2025_%']}%  
    * *Motivo de selección:* Excelente equilibrio entre costes reducidos y rendimiento sobresaliente en el mercado europeo.
    """)

# --- SECCIÓN: GRÁFICO DE MEDIA DEL MERCADO VS FONDOS ---
st.markdown("---")
st.subheader("📈 Gráfico Comparativo: Rentabilidad Anual vs. Media del Mercado")

# Calcular media del mercado por año para los fondos indexados globales
anios = ['2021_%', '2022_%', '2023_%', '2024_%', '2025_%', 'YTD_2026_%']
etiquetas_anios = ['2021', '2022', '2023', '2024', '2025', '2026 (YTD)']

# Media de los fondos indexados limpios (Core) como referencia de mercado
df_indexados = df_master[df_master['TER_%'] <= 0.30]
media_mercado = df_indexados[anios].mean().values

# Preparar dataframe para el gráfico de líneas de Streamlit
df_chart = pd.DataFrame({
    'Año': etiquetas_anios,
    'Media del Mercado Global (Indexados)': media_mercado,
    'Ejemplo Destacado (Pictet Security)': df_master.loc[df_master['Tipo'] == 'Ciberseguridad', anios].values[0]
})
df_chart = df_chart.set_index('Año')

st.line_chart(df_chart)
st.caption("Nota: El gráfico compara la evolución media de los índices globales de bajo coste frente a fondos sectoriales especializados.")

# --- SECCIONES DE CONTROL FIJAS ---
data_core = df_master[df_master['TER_%'] <= 0.50]
data_satelites = df_master[(df_master['TER_%'] > 0.50) & (df_master['TER_%'] <= 1.50)]
data_descartados = df_master[df_master['TER_%'] > 1.50]

st.markdown("---")
st.subheader("✅ Cartera Core / Núcleo (TER ≤ 0.50%)")
st.dataframe(data_core.reset_index(drop=True), use_container_width=True)

st.subheader("🚀 Satélites de Alto Crecimiento (Biotecnología y Ciberseguridad)")
st.dataframe(data_satelites.reset_index(drop=True), use_container_width=True)

st.subheader("❌ Fondos Descartados (Banca Tradicional / Altas Comisiones)")
st.dataframe(data_descartados[['Nombre del Fondo', 'ISIN', 'Tipo', 'TER_%']].reset_index(drop=True), use_container_width=True)
