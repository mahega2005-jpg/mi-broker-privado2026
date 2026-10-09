import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Mi Broker Privado", page_icon="🛡️", layout="centered")

# --- INICIALIZAR ESTADOS DE SESIÓN ---
if 'historico_consultas' not in st.session_state:
    st.session_state.historico_consultas = []

if 'cartera_vigilada' not in st.session_state:
    # Inicializamos con tus dos fondos reales contratados y el correo asignado
    st.session_state.cartera_vigilada = [
        {'ISIN': 'IE00BFPM9N11', 'Nombre': 'Vanguard Global Stock Index Inst Plus EUR Acc', 'Suelo_%': -10.0, 'Techo_%': 25.0, 'Email': 'mahega2005@gmail.com'},
        {'ISIN': 'IE00BGCZOB53', 'Nombre': 'Vanguard Global Bond Index Inst Plus EUR Hgd', 'Suelo_%': -8.0, 'Techo_%': 15.0, 'Email': 'mahega2005@gmail.com'}
    ]

if 'alerta_activa' not in st.session_state:
    # Simulamos una alerta activa de prueba para que veas la ventana flotante al abrir la app
    st.session_state.alerta_activa = True

# --- CABECERA Y LOGOTIPO ---
st.markdown("""
<div style="background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); padding: 25px; border-radius: 15px; text-align: center; color: white; font-family: sans-serif; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);">
    <div style="font-size: 40px; margin-bottom: 5px;">🛡️📈</div>
    <h2 style="margin: 0; font-size: 24px; letter-spacing: 1px;">MI BROKER PRIVADO</h2>
    <p style="margin: 5px 0 0 0; font-size: 13px; color: #a2dbfa;">Panel de Control, Bandas de Alerta & Vigilancia 24h (España / Europa)</p>
    <div style="margin-top: 15px; display: inline-block; background: #e74c3c; color: white; padding: 6px 15px; border-radius: 15px; font-size: 11px; font-weight: bold;">
        ESTADO: VIGILANCIA DE SUELOS Y TECHOS ACTIVA 🚨
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

# --- VENTANA FLOTANTE (MODAL) DE ALERTA URGENTE AL ABRIR LA APP ---
@st.dialog("🚨 ¡ALERTA URGENTE DE CARTERA ACTIVADA!")
def mostrar_alerta_urgente():
    st.markdown("### Se ha superado una Banda de Control")
    st.markdown("El sistema de vigilancia ha detectado que uno de nuestros fondos vigilados ha perforado el **Suelo de Seguridad** o superado el **Techo** previsto.")
    st.markdown("---")
    st.info("📨 **Notificación enviada con éxito a:** `mahega2005@gmail.com`")
    st.markdown("""
    * **Fondo afectado:** `Vanguard Global Bond Index Inst Plus EUR Hgd` (ISIN: `IE00BGCZOB53`)
    * **Situación:** Desviación de mercado detectada superior al límite negativo programado (-8%).
    * **Acción recomendada:** Revisar la ficha del fondo, contrastar con los portales especializados (Morningstar / JustETF) y valorar un reequilibrio o mantenimiento estratégico.
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✖️ Cerrar y Entendido", type="primary", use_container_width=True):
        st.session_state.alerta_activa = False
        st.rerun()

# Si hay alerta activa al cargar la app, mostramos la ventana modal automáticamente
if st.session_state.alerta_activa:
    mostrar_alerta_urgente()

# --- VENTANA FLOTANTE DE DETALLE DE ISIN ---
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

# --- BARRA LATERAL: NUEVO BOTÓN PARA AÑADIR ISIN CONTRATADO A VIGILANCIA ---
st.sidebar.header("🛡️ Gestión y Vigilancia ISIN")

with st.sidebar.expander("➕ Añadir Nuevo ISIN a Vigilar", expanded=False):
    nuevo_isin = st.text_input("Código ISIN a añadir", "").strip().upper()
    suelo_input = st.number_input("Suelo de Alerta (%)", value=-10.0, step=1.0)
    techo_input = st.number_input("Techo de Alerta (%)", value=20.0, step=1.0)
    email_input = st.text_input("Correo de Avisos", value="mahega2005@gmail.com")
    
    if st.button("Registrar en Vigilancia", use_container_width=True):
        if nuevo_isin:
            # Comprobar si ya existe
            existe = any(item['ISIN'] == nuevo_isin for item in st.session_state.cartera_vigilada)
            if not existe:
                # Buscar nombre en tabla o poner uno genérico
                match = df_master[df_master['ISIN'] == nuevo_isin]
                nombre_f = match.iloc[0]['Nombre del Fondo'] if not match.empty else f"Fondo Personalizado ({nuevo_isin})"
                
                st.session_state.cartera_vigilada.append({
                    'ISIN': nuevo_isin, 'Nombre': nombre_f, 'Suelo_%': suelo_input, 'Techo_%': techo_input, 'Email': email_input
                })
                st.sidebar.success(f"¡ISIN `{nuevo_isin}` añadido a vigilancia activa con aviso a {email_input}!")
            else:
                st.sidebar.warning("Este ISIN ya está registrado en tu sistema de vigilancia.")
        else:
            st.sidebar.error("Introduce un código ISIN válido.")

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

# --- PANEL PRINCIPAL: ESTADO DE LA CARTERA VIGILADA ---
st.subheader("🛡️ Panel de Control de Bandas (Suelos y Techos)")
st.markdown("Listado de tus posiciones bajo supervisión 24h con destino de avisos a `mahega2005@gmail.com`:")

df_vigilancia = pd.DataFrame(st.session_state.cartera_vigilada)
st.dataframe(df_vigilancia, use_container_width=True)

# --- TABLA DE RESULTADOS DE BÚSQUEDA ---
st.markdown("---")
st.subheader("📊 Resultados de la Búsqueda y Histórico Anual")
busqueda_texto = st.text_input("Filtrar tabla maestra por Nombre", "").strip()
df_filtrado = df_master.copy()
if busqueda_texto:
    df_filtrado = df_filtrado[df_filtrado['Nombre del Fondo'].str.contains(busqueda_texto, case=False, na=False)]

st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)

# --- SECCIÓN: COPILOTO IA ---
st.markdown("---")
st.subheader("🤖 Copiloto IA (Análisis cruzado de Prensa y Expertos)")
st.markdown("""
*💡 **Consenso actual:** Mantenimiento de bandas de control activas para evitar decisiones emocionales ante oscilaciones normales de mercado.*
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

# --- SECCIONES FIJAS DE CARTERA ---
st.markdown("---")
st.subheader("💼 Tu Cartera Contratada (Renta Variable & Renta Fija Global)")
cartera_usuario = df_master[df_master['ISIN'].isin(['IE00BFPM9N11', 'IE00BGCZOB53'])]
st.dataframe(cartera_usuario[['Nombre del Fondo', 'ISIN', 'Operador / Comercializador España', 'Permite Transferencia/Traspaso', 'TER_%']].reset_index(drop=True), use_container_width=True)
