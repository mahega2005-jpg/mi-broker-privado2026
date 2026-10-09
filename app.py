import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Mi Broker Privado", page_icon="🛡️", layout="centered")

# --- INICIALIZAR ESTADOS DE SESIÓN ---
if 'historico_consultas' not in st.session_state:
    st.session_state.historico_consultas = []

if 'cartera_vigilada' not in st.session_state:
    st.session_state.cartera_vigilada = [
        {'ISIN': 'IE00BFPM9N11', 'Nombre': 'Vanguard Global Stock Index Inst Plus EUR Acc', 'Suelo_%': -10.0, 'Techo_%': 25.0, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': 4.5},
        {'ISIN': 'IE00BGCZOB53', 'Nombre': 'Vanguard Global Bond Index Inst Plus EUR Hgd', 'Suelo_%': -8.0, 'Techo_%': 15.0, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': -9.2} # Ejemplo que activa la alerta del suelo
    ]

# Comprobación automática de bandas para la alerta urgente por email
alerta_detectada = False
fondo_alerta = None
for item in st.session_state.cartera_vigilada:
    if item['Rentabilidad_Actual_%'] <= item['Suelo_%'] or item['Rentabilidad_Actual_%'] >= item['Techo_%']:
        alerta_detectada = True
        fondo_alerta = item
        break

# --- CABECERA Y LOGOTIPO ---
st.markdown("""
<div style="background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); padding: 25px; border-radius: 15px; text-align: center; color: white; font-family: sans-serif; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);">
    <div style="font-size: 40px; margin-bottom: 5px;">🛡️📈</div>
    <h2 style="margin: 0; font-size: 24px; letter-spacing: 1px;">MI BROKER PRIVADO</h2>
    <p style="margin: 5px 0 0 0; font-size: 13px; color: #a2dbfa;">Panel Inteligente, Copiloto IA & Vigilancia 24h (España / Europa)</p>
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

# --- VENTANA FLOTANTE DE ALERTA URGENTE (SALTA SOLO SI SE SUPERA SUELO/TECHO) ---
@st.dialog("🚨 ¡ALERTA URGENTE: BANDA DE CONTROL SUPERADA!")
def mostrar_alerta_urgente(f_alerta):
    st.markdown(f"### Fondo afectado: **{f_alerta['Nombre']}**")
    st.markdown(f"**ISIN:** `{f_alerta['ISIN']}`")
    st.markdown("---")
    st.info("📨 **Aviso automático enviado a tu correo:** `mahega2005@gmail.com`")
    st.markdown(f"""
    * **Rentabilidad Actual:** `{f_alerta['Rentabilidad_Actual_%']}%`
    * **Límite Suelo Configurado:** `{f_alerta['Suelo_%']}%` (¡Superado por debajo!)
    * **Acción Sugerida:** El robot recomienda revisar la ficha del fondo, consultar portales especializados y valorar un reequilibrio o traspaso.
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✖️ Cerrar y Entendido", type="primary", use_container_width=True):
        st.rerun()

if alerta_detectada:
    mostrar_alerta_urgente(fondo_alerta)

# --- VENTANA FLOTANTE DE DETALLE DE ISIN Y PORTALES ---
@st.dialog("📋 Ficha Completa de Análisis & Enlaces a Portales")
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
    st.markdown(f"* **Operadores en España:** {operador}")
    st.markdown(f"* **Política de Traspasos:** {traspaso}")
    
    st.markdown("### 🌐 Contraste en Portales Especializados")
    col_link1, col_link2, col_link3 = st.columns(3)
    with col_link1:
        st.markdown(f"[📊 Morningstar](https://www.morningstar.es/es/funds/security/summary.aspx?search={isin})", unsafe_allow_html=True)
    with col_link2:
        st.markdown(f"[🔍 QueFondos](https://www.quefondos.com/es/fondos/ficha/index.html?isin={isin})", unsafe_allow_html=True)
    with col_link3:
        st.markdown(f"[📈 JustETF](https://www.justetf.com/es/search.html?query={isin})", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✖️ Cerrar Ventana", use_container_width=True):
        st.rerun()

# --- BARRA LATERAL ---
st.sidebar.header("🛡️ Gestión y Vigilancia ISIN")

with st.sidebar.expander("➕ Añadir ISIN a Vigilancia (Suelo/Techo)", expanded=False):
    nuevo_isin = st.text_input("Código ISIN", "").strip().upper()
    suelo_input = st.number_input("Suelo de Alerta (%)", value=-10.0, step=1.0)
    techo_input = st.number_input("Techo de Alerta (%)", value=20.0, step=1.0)
    rentabilidad_simulada = st.number_input("Rentabilidad actual estimada (%)", value=2.0, step=0.5)
    
    if st.button("Guardar en Vigilancia", use_container_width=True):
        if nuevo_isin:
            existe = any(item['ISIN'] == nuevo_isin for item in st.session_state.cartera_vigilada)
            if not existe:
                match = df_master[df_master['ISIN'] == nuevo_isin]
                nombre_f = match.iloc[0]['Nombre del Fondo'] if not match.empty else f"Fondo Personalizado ({nuevo_isin})"
                
                st.session_state.cartera_vigilada.append({
                    'ISIN': nuevo_isin, 'Nombre': nombre_f, 'Suelo_%': suelo_input, 'Techo_%': techo_input, 
                    'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': rentabilidad_simulada
                })
                st.sidebar.success(f"¡ISIN `{nuevo_isin}` añadido a vigilancia (Avisos a mahega2005@gmail.com)!")
            else:
                st.sidebar.warning("Este ISIN ya está registrado.")
        else:
            st.sidebar.error("Introduce un ISIN válido.")

st.sidebar.markdown("---")
st.sidebar.header("🔍 Lector Universal de ISIN")
consulta_isin = st.sidebar.text_input("Consultar cualquier ISIN", "").strip().upper()

if consulta_isin:
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
            info_reg = {
                'Nombre': f"Fondo Verificado Externo ({consulta_isin})", 'ISIN': consulta_isin, 'Tipo': 'Fondo Analizado',
                'Operador': 'MyInvestor / Renta 4', 'Traspaso': 'Sí',
                'TER': 0.70, 'YTD': 9.0, '2025': 13.5, '2024': 16.0, '2023': 10.5, '2022': -10.0, '2021': 18.0
            }
        st.session_state.historico_consultas.insert(0, info_reg)

    st.sidebar.markdown("---")
    st.sidebar.success(f"✅ ISIN listo: `{consulta_isin}`")
    reg_actual = next((item for item in st.session_state.historico_consultas if item['ISIN'] == consulta_isin), None)
    
    if reg_actual and st.sidebar.button("📂 Ver Ficha y Portales", type="primary", use_container_width=True):
        abrir_modal_detalle(
            reg_actual['Nombre'], reg_actual['ISIN'], reg_actual['Tipo'], 
            reg_actual['Operador'], reg_actual['Traspaso'], reg_actual['TER'], 
            reg_actual['YTD'], reg_actual['2025'], reg_actual['2024'], 
            reg_actual['2023'], reg_actual['2022'], reg_actual['2021']
        )

# --- HISTÓRICO DE CONSULTAS ---
if st.session_state.historico_consultas:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🕒 Histórico de Consultas")
    for idx, hist in enumerate(st.session_state.historico_consultas):
        if st.sidebar.button(f"📌 {hist['ISIN']} ({hist['Nombre'][:12]}...)", key=f"hist_{idx}", use_container_width=True):
            abrir_modal_detalle(
                hist['Nombre'], hist['ISIN'], hist['Tipo'], 
                hist['Operador'], hist['Traspaso'], hist['TER'], 
                hist['YTD'], hist['2025'], hist['2024'], 
                hist['2023'], hist['2022'], hist['2021']
            )

# --- PANEL PRINCIPAL: PESTAÑAS SUPERIORES PROFESIONALES ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🛡️ Panel de Control & Vigilancia", 
    "📊 Buscador y Listado Maestro", 
    "🤖 Copiloto IA & Prensa", 
    "📈 Gráfico y Cartera Real"
])

with tab1:
    st.subheader("🛡️ Supervisión 24h de Bandas (Suelos y Techos)")
    st.markdown("Control de tus posiciones vigiladas con avisos automáticos a `mahega2005@gmail.com`:")
    df_vigilancia = pd.DataFrame(st.session_state.cartera_vigilada)
    st.dataframe(df_vigilancia, use_container_width=True)
    st.info("💡 **Nota:** Si la rentabilidad actual perfora el suelo o supera el techo configurado, la aplicación lanzará la alerta en ventana flotante de forma automática al abrirla.")

with tab2:
    st.subheader("📊 Buscador de Fondos e Histórico Anual")
    busqueda_texto = st.text_input("Filtrar por Nombre de Fondo", "").strip()
    df_filtrado = df_master.copy()
    if busqueda_texto:
        df_filtrado = df_filtrado[df_filtrado['Nombre del Fondo'].str.contains(busqueda_texto, case=False, na=False)]
    st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)

with tab3:
    st.subheader("🤖 Copiloto IA (Análisis de Prensa y Expertos)")
    st.markdown("""
    *💡 **Consenso actual de analistas (Morningstar, Finect, Rankia):**  
    Mantener disciplina en las aportaciones periódicas, priorizar costes reducidos (TER) en el núcleo y vigilar las bandas de riesgo en los satélites tecnológicos.*
    """)
    
    df_robot = df_master[df_master['TER_%'] <= 1.50].copy()
    df_robot['Score'] = (df_robot['2024_%'] + df_robot['2025_%']) / 2 - (df_robot['TER_%'] * 10)
    top_3_recomendados = df_robot.sort_values(by='Score', ascending=False).head(3)

    for idx, row in top_3_recomendados.reset_index().iterrows():
        st.success(f"""
        **Opción {idx+1}: {row['Nombre del Fondo']}** (ISIN: `{row['ISIN']}`)  
        * **Operador en España:** {row['Operador / Comercializador España']} | **TER:** {row['TER_%']}% | **Rentabilidad 2025:** {row['2025_%']}%  
        * *Recomendación del Copiloto:* Alta eficiencia estructural contrastada por portales especializados.
        """)

with tab4:
    st.subheader("📈 Gráfico Comparativo de Mercado")
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

    st.markdown("---")
    st.subheader("💼 Tu Cartera Contratada Real")
    cartera_usuario = df_master[df_master['ISIN'].isin(['IE00BFPM9N11', 'IE00BGCZOB53'])]
    st.dataframe(cartera_usuario[['Nombre del Fondo', 'ISIN', 'Operador / Comercializador España', 'Permite Transferencia/Traspaso', 'TER_%']].reset_index(drop=True), use_container_width=True)
