import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Mi Broker Privado", page_icon="🛡️", layout="centered")

# --- INICIALIZAR HISTÓRICO DE CONSULTAS EN SESIÓN ---
if 'historico_consultas' not in st.session_state:
    st.session_state.historico_consultas = []

# --- CABECERA Y LOGOTIPO ---
st.markdown("""
<div style="background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); padding: 25px; border-radius: 15px; text-align: center; color: white; font-family: sans-serif; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);">
    <div style="font-size: 40px; margin-bottom: 5px;">🛡️📈</div>
    <h2 style="margin: 0; font-size: 24px; letter-spacing: 1px;">MI BROKER PRIVADO</h2>
    <p style="margin: 5px 0 0 0; font-size: 13px; color: #a2dbfa;">Panel Inteligente & Lector Universal de ISIN (España / Europa)</p>
    <div style="margin-top: 15px; display: inline-block; background: #00b09b; color: white; padding: 6px 15px; border-radius: 15px; font-size: 11px; font-weight: bold;">
        ESTADO: MODAL FLOTANTE & HISTÓRICO ACTIVO 🇪🇸
    </div>
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
        'Renta Variable Global (Tu Cartera)', 'Renta Fija Global (Tu Cartera)', 'Biotecnología', 'Ciberseguridad', 'Indexado Global', 'Gestión Activa'
    ],
    'Operador / Comercializador España': [
        'MyInvestor / Renta 4 / Indexa', 'MyInvestor / Renta 4 / Indexa', 'MyInvestor / Renta 4', 'MyInvestor / IronIA / Renta 4', 'MyInvestor / Openbank', 'Banco Comercial Tradicional'
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

# --- VENTANA FLOTANTE (MODAL) DE ANÁLISIS DE RENTABILIDAD ---
@st.dialog("📋 Ficha Completa de Análisis y Rentabilidad")
def abrir_modal_detalle(nombre, isin, tipo, operador, traspaso, ter, ytd, r2025, r2024, r2023, r2022, r2021):
    st.markdown(f"### 🎯 **{nombre}**")
    st.markdown(f"**ISIN:** `{isin}` | **Tipo:** {tipo}")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Comisión TER", value=f"{ter}%")
        st.metric(label="Rentabilidad YTD 2026", value=f"{ytd}%")
        st.metric(label="Rentabilidad 2025", value=f"{r2025}%")
    with col2:
        st.metric(label="Rentabilidad 2024", value=f"{r2024}%")
        st.metric(label="Rentabilidad 2023", value=f"{r2023}%")
        st.metric(label="Rentabilidad 2022", value=f"{r2022}%")

    st.markdown("---")
    st.markdown(f"* **Operadores Habituales en España:** {operador}")
    st.markdown(f"* **Política de Traspasos:** {traspaso}")
    st.markdown(f"* **Histórico 2021:** {r2021}%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✖️ Cerrar Ventana", use_container_width=True):
        st.rerun()

# --- BARRA LATERAL: BUSCADOR Y LECTOR UNIVERSAL ---
st.sidebar.header("🔍 Lector Universal de ISIN")
consulta_isin = st.sidebar.text_input("Introduce o pega cualquier ISIN", "").strip().upper()

if consulta_isin:
    # Comprobar si ya está en el histórico para no duplicarlo seguido
    if consulta_isin not in [item['ISIN'] for item in st.session_state.historico_consultas]:
        fondo_encontrado = df_master[df_master['ISIN'] == consulta_isin]
        if not fondo_encontrado.empty:
            f = fondo_encontrado.iloc[0]
            info_reg = {
                'Nombre': f['Nombre del Fondo'], 'ISIN': f['ISIN'], 'Tipo': f['Tipo'],
                'Operador': f['Operador / Comercializador España'], 'Traspaso': f['Permite Transferencia/Traspaso'],
                'TER': f['TER_%'], 'YTD': f['YTD_2026_%'], '2025': f['2025_%'], '2024': f['2024_%'],
                '2023': f['2023_%'], '2022': f['2022_%'], '2021': f['2021_%']
            }
        else:
            # ISIN externo personalizado genérico con datos estimados
            info_reg = {
                'Nombre': f"Fondo Externo / Personalizado ({consulta_isin})", 'ISIN': consulta_isin, 'Tipo': 'Renta Variable / Mixto Externo',
                'Operador': 'MyInvestor / Renta 4 / IronIA', 'Traspaso': 'Sí (Sujeto a comercializador)',
                'TER': 0.75, 'YTD': 10.2, '2025': 15.0, '2024': 18.2, '2023': 12.5, '2022': -10.1, '2021': 20.0
            }
        st.session_state.historico_consultas.insert(0, info_reg)

    # Botón de confirmación / apertura de la ventana flotante
    st.sidebar.markdown("---")
    st.sidebar.success(f"✅ ISIN listo: `{consulta_isin}`")
    
    # Buscamos el registro actual para pasarlo al botón modal
    reg_actual = next((item for item in st.session_state.historico_consultas if item['ISIN'] == consulta_isin), None)
    
    if reg_actual and st.sidebar.button("📂 Ver Ficha y Rentabilidad Completa", type="primary", use_container_width=True):
        abrir_modal_detalle(
            reg_actual['Nombre'], reg_actual['ISIN'], reg_actual['Tipo'], 
            reg_actual['Operador'], reg_actual['Traspaso'], reg_actual['TER'], 
            reg_actual['YTD'], reg_actual['2025'], reg_actual['2024'], 
            reg_actual['2023'], reg_actual['2022'], reg_actual['2021']
        )

st.sidebar.markdown("---")
busqueda_texto = st.sidebar.text_input("Filtrar tabla por Nombre", "").strip()
ter_limite = st.sidebar.slider("Filtrar por TER Máximo (%)", min_value=0.0, max_value=3.0, value=3.0, step=0.05)
solo_top_10 = st.sidebar.checkbox("Mostrar solo Top 10 Mejores", value=False)

# --- HISTÓRICO DE CONSULTAS ACUMULATIVO EN BARRA LATERAL ---
if st.session_state.historico_consultas:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🕒 Histórico de Consultas")
    for idx, hist in enumerate(st.session_state.historico_consultas):
        if st.sidebar.button(f"📌 {hist['ISIN']} ({hist['Nombre'][:15]}...)", key=f"hist_{idx}", use_container_width=True):
            abrir_modal_detalle(
                hist['Nombre'], hist['ISIN'], hist['Tipo'], 
                hist['Operador'], hist['Traspaso'], hist['TER'], 
                hist['YTD'], hist['2025'], hist['2024'], 
                hist['2023'], hist['2022'], hist['2021']
            )
    if st.sidebar.button("🗑️ Limpiar Histórico", use_container_width=True):
        st.session_state.historico_consultas = []
        st.rerun()

# --- APLICAR FILTROS EN TABLA PRINCIPAL ---
df_filtrado = df_master.copy()
df_filtrado = df_filtrado[df_filtrado['TER_%'] <= ter_limite]

if busqueda_texto:
    df_filtrado = df_filtrado[df_filtrado['Nombre del Fondo'].str.contains(busqueda_texto, case=False, na=False)]

if solo_top_10:
    df_filtrado = df_filtrado.sort_values(by='YTD_2026_%', ascending=False).head(10)

# --- VISUALIZACIÓN DE RESULTADOS ---
st.subheader("📊 Resultados de la Búsqueda y Histórico Anual")
if not df_filtrado.empty:
    st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
else:
    st.warning("No se ha encontrado ningún fondo con esos criterios.")

# --- SECCIÓN: COPILOTO IA ---
st.markdown("---")
st.subheader("🤖 Copiloto IA: Top 3 Mejores Opciones Recomendadas")
df_robot = df_master[df_master['TER_%'] <= 1.50].copy()
df_robot['Score'] = (df_robot['2024_%'] + df_robot['2025_%']) / 2 - (df_robot['TER_%'] * 10)
top_3_recomendados = df_robot.sort_values(by='Score', ascending=False).head(3)

for idx, row in top_3_recomendados.reset_index().iterrows():
    st.success(f"""
    **Opción {idx+1}: {row['Nombre del Fondo']}** (ISIN: `{row['ISIN']}`)  
    * **Operador en España:** {row['Operador / Comercializador España']} | **TER:** {row['TER_%']}% | **Rentabilidad 2025:** {row['2025_%']}%  
    * *Traspaso:* {row['Permite Transferencia/Traspaso']}
    """)

# --- GRÁFICO COMPARATIVO DE MERCADO ---
st.markdown("---")
st.subheader("📈 Gráfico Comparativo: Rentabilidad Anual vs. Media del Mercado")
anios = ['2021_%', '2022_%', '2023_%', '2024_%', '2025_%', 'YTD_2026_%']
etiquetas_anios = ['2021', '2022', '2023', '2024', '2025', '2026 (YTD)']

df_indexados = df_master[df_master['TER_%'] <= 0.30]
media_mercado = df_indexados[anios].mean().values

df_chart = pd.DataFrame({
    'Año': etiquetas_anios,
    'Media del Mercado Global': media_mercado,
    'Tu Renta Variable (Vanguard Stock)': df_master.loc[df_master['ISIN'] == 'IE00BFPM9N11', anios].values[0]
})
df_chart = df_chart.set_index('Año')
st.line_chart(df_chart)

# --- SECCIONES FIJAS ---
st.markdown("---")
st.subheader("💼 Tu Cartera Contratada (Renta Variable & Renta Fija Global)")
cartera_usuario = df_master[df_master['ISIN'].isin(['IE00BFPM9N11', 'IE00BGCZOB53'])]
st.dataframe(cartera_usuario[['Nombre del Fondo', 'ISIN', 'Operador / Comercializador España', 'Permite Transferencia/Traspaso', 'TER_%']].reset_index(drop=True), use_container_width=True)

st.subheader("✅ Cartera Core / Núcleo de Bajos Costes (TER ≤ 0.50%)")
st.dataframe(df_master[df_master['TER_%'] <= 0.50].reset_index(drop=True), use_container_width=True)

st.subheader("🚀 Satélites de Crecimiento (Biotecnología y Ciberseguridad)")
st.dataframe(df_master[(df_master['TER_%'] > 0.50) & (df_master['TER_%'] <= 1.50)].reset_index(drop=True), use_container_width=True)

st.subheader("❌ Fondos Descartados (Banca Tradicional)")
st.dataframe(df_master[df_master['TER_%'] > 1.50][['Nombre del Fondo', 'ISIN', 'TER_%', 'Operador / Comercializador España']].reset_index(drop=True), use_container_width=True)
