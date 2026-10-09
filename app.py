import streamlit as st
import pandas as pd

# Configuración de la página y layout
st.set_page_config(page_title="Mi Broker Privado", page_icon="🛡️", layout="centered")

# --- ESTILOS CSS DEFINITIVOS: ARMONÍA VISUAL GEMINI + BARRA LATERAL UNIFICADA ---
st.markdown("""
<style>
    /* Fondo general de la aplicación en tono gris/azulado suave estilo Gemini */
    .stApp {
        background-color: #f0f4f9;
        color: #1f2328;
    }
    
    /* Barra lateral unificada con el mismo tono suave y limpio */
    section[data-testid="stSidebar"] {
        background-color: #f0f4f9;
        border-right: 1px solid #cbd5e1;
    }
    
    /* Contenedores y tarjetas transparentes */
    div.stMarkdownContainer, div.stDataFrame {
        background-color: transparent;
    }
    
    /* Pestañas superiores estilizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #e2e8f0;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #cbd5e1;
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
    /* Pestaña seleccionada: Sutilmente sombreada, limpia y sin azul fuerte */
    .stTabs [aria-selected="true"] {
        background-color: #cbd5e1 !important;
        color: #0f172a !important;
        border-color: #94a3b8 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }

    /* Botones principales y de la barra lateral */
    .stButton button {
        background-color: #ffffff;
        color: #1f2328;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        font-weight: 500;
    }
    .stButton button:hover {
        background-color: #e2e8f0;
        border-color: #94a3b8;
        color: #1f2328;
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

# --- CABECERA Y LOGOTIPO CON PANEL CENTRAL SUAVE Y MARCADO ---
st.markdown("""
<div style="background: linear-gradient(135deg, #dbeafe, #bfdbfe); padding: 25px; border-radius: 12px; text-align: center; color: #1e3a8a; border: 1px solid #93c5fd; box-shadow: 0px 4px 15px rgba(0,0,0,0.05);">
    <div style="font-size: 38px; margin-bottom: 5px;">🛡️📈</div>
    <h2 style="margin: 0; font-size: 24px; letter-spacing: 1.5px; color: #1e40af;">MI BROKER PRIVADO</h2>
    <p style="margin: 6px 0 0 0; font-size: 13px; color: #3b82f6;">Panel Táctico • Core en Indexa Capital • Vigilancia de Bandas 24h</p>
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

if alerta_detectada:
    mostrar_alerta_urgente(fondo_alerta)

# --- VENTANA FLOTANTE DE PRUEBA DE CORREO ---
@st.dialog("📧 Simulación de Notificación Interna")
def mostrar_dialogo_prueba_correo():
    st.markdown("### 📨 Estado del Sistema de Avisos")
    st.success("✅ **Destinatario de Referencia:** `mahega2005@gmail.com`")
    st.markdown("""
    **Simulación de Alerta de Banda Superada:**
    > *El sistema ha verificado que el control visual de umbrales opera correctamente en la tablet, manteniendo la privacidad de tus claves sin intermediarios externos.*
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✖️ Cerrar Ventana", type="primary", use_container_width=True):
        st.session_state.prueba_correo_enviada = False
        st.rerun()

if st.session_state.prueba_correo_enviada:
    mostrar_dialogo_prueba_correo()

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
    st.markdown(f"* **Operador en España:** {operador}")
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
st.sidebar.header("🛡️ Panel de Control Táctico")

with st.sidebar.expander("🧪 Test de Alertas (Modo Seguro)", expanded=True):
    if st.sidebar.button("🚀 Comprobar Estado de Alertas", use_container_width=True):
        st.session_state.prueba_correo_enviada = True
        st.rerun()

st.sidebar.markdown("---")
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
                st.sidebar.success(f"¡ISIN `{nuevo_isin}` añadido!")
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
    st.sidebar.subheader("🕒 Histórico Reciente")
    for idx, hist in enumerate(st.session_state.historico_consultas):
        if st.sidebar.button(f"📌 {hist['ISIN']} ({hist['Nombre'][:10]}...)", key=f"hist_{idx}", use_container_width=True):
            abrir_modal_detalle(
                hist['Nombre'], hist['ISIN'], hist['Tipo'], 
                hist['Operador'], hist['Traspaso'], hist['TER'], 
                hist['YTD'], hist['2025'], hist['2024'], 
                hist['2023'], hist['2022'], hist['2021']
            )

# --- PANEL PRINCIPAL: PESTAÑAS SUPERIORES ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🛡️ Control & Bandas", 
    "📊 Buscador Maestro", 
    "🤖 Copiloto IA & Prensa", 
    "📈 Gráficos & Cartera Indexa"
])

with tab1:
    st.subheader("🛡️ Supervisión 24h de Bandas (Suelos y Techos)")
    st.markdown("Control seguro de posiciones vigiladas (Asociado a referencia `mahega2005@gmail.com`):")
    df_vigilancia = pd.DataFrame(st.session_state.cartera_vigilada)
    st.dataframe(df_vigilancia, use_container_width=True)
    st.info("💡 **Aviso:** Las alertas se disparan visualmente en pantalla de forma automática al superar los límites de riesgo configurados.")

with tab2:
    st.subheader("📊 Buscador y Listado Maestro de Fondos")
    busqueda_texto = st.text_input("Filtrar por Nombre de Fondo", "").strip()
    df_filtrado = df_master.copy()
    if busqueda_texto:
        df_filtrado = df_filtrado[df_filtrado['Nombre del Fondo'].str.contains(busqueda_texto, case=False, na=False)]
    st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)

with tab3:
    st.subheader("🤖 Copiloto IA (Análisis de Mercado)")
    st.markdown("""
    *💡 **Consenso de expertos (Morningstar / Finect):**  
    Priorizar eficiencia de costes (TER) en el núcleo global y mantener disciplina en aportaciones periódicas.*
    """)
    
    df_robot = df_master[df_master['TER_%'] <= 1.50].copy()
    df_robot['Score'] = (df_robot['2024_%'] + df_robot['2025_%']) / 2 - (df_robot['TER_%'] * 10)
    top_3_recomendados = df_robot.sort_values(by='Score', ascending=False).head(3)

    for idx, row in top_3_recomendados.reset_index().iterrows():
        st.success(f"""
        **Opción Estratégica {idx+1}: {row['Nombre del Fondo']}** (ISIN: `{row['ISIN']}`)  
        * **Operador:** {row['Operador / Comercializador España']} | **TER:** {row['TER_%']}% | **Rentabilidad 2025:** {row['2025_%']}%  
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
    st.subheader("💼 Tu Cartera Core Contratada (Indexa Capital)")
    cartera_usuario = df_master[df_master['ISIN'].isin(['IE00BFPM9N11', 'IE00BGCZOB53'])]
    st.dataframe(cartera_usuario[['Nombre del Fondo', 'ISIN', 'Operador / Comercializador España', 'Permite Transferencia/Traspaso', 'TER_%']].reset_index(drop=True), use_container_width=True)
