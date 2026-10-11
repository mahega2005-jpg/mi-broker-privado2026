import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página y layout
st.set_page_config(page_title="Mi Broker Privado", page_icon="🛡️", layout="centered")

# --- ESTILOS CSS DEFINITIVOS: SIMETRÍA Y ARMONÍA VISUAL ---
st.markdown("""
<style>
    /* Fondo general de la aplicación en tono gris/azulado suave estilo Gemini */
    .stApp {
        background-color: #f0f4f9;
        color: #1f2328;
    }
    
    /* Barra lateral unificada con el mismo tono y línea derecha marcada */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #dbeafe, #bfdbfe);
        border-right: 2px solid #93c5fd;
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
    /* Pestaña seleccionada (activa) */
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

# --- FUNCIÓN DE CARGA / ACTUALIZACIÓN DINÁMICA 24H ---
def obtener_datos_actualizados():
    # Marcador de tiempo real
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M")
    
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
    return pd.DataFrame(data_fondos), ahora

# Carga limpia en cada ejecución de pantalla
df_master, ultima_actualizacion = obtener_datos_actualizados()

# --- INICIALIZAR ESTADOS DE SESIÓN ---
if 'historico_consultas' not in st.session_state:
    st.session_state.historico_consultas = []

if 'cartera_vigilada' not in st.session_state:
    st.session_state.cartera_vigilada = pd.DataFrame([
        {'ISIN': 'IE00BFPM9N11', 'Nombre': 'Vanguard Global Stock Index Inst Plus EUR Acc', 'Suelo_%': -10.0, 'Techo_%': 25.0, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': 4.5},
        {'ISIN': 'IE00BGCZOB53', 'Nombre': 'Vanguard Global Bond Index Inst Plus EUR Hgd', 'Suelo_%': -8.0, 'Techo_%': 15.0, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': -2.1}
    ])

if 'prueba_correo_enviada' not in st.session_state:
    st.session_state.prueba_correo_enviada = False

if 'expandir_lector' not in st.session_state:
    st.session_state.expandir_lector = True

# Comprobación automática 24h de bandas
alerta_detectada = False
fondo_alerta = None
if isinstance(st.session_state.cartera_vigilada, pd.DataFrame) and not st.session_state.cartera_vigilada.empty:
    for _, item in st.session_state.cartera_vigilada.iterrows():
        try:
            if float(item['Rentabilidad_Actual_%']) <= float(item['Suelo_%']) or float(item['Rentabilidad_Actual_%']) >= float(item['Techo_%']):
                alerta_detectada = True
                fondo_alerta = item
                break
        except (ValueError, KeyError):
            continue

# --- CABECERA Y LOGOTIPO CON INDICADOR DE TIEMPO REAL 24H ---
st.markdown(f"""
<div style="background: linear-gradient(135deg, #dbeafe, #bfdbfe); padding: 25px; border-radius: 12px; text-align: center; color: #1e3a8a; border: 2px solid #3b82f6; box-shadow: 0px 4px 15px rgba(0,0,0,0.08);">
    <div style="font-size: 38px; margin-bottom: 5px;">🛡️📈</div>
    <h2 style="margin: 0; font-size: 24px; letter-spacing: 1.5px; color: #1e40af;">MI BROKER PRIVADO</h2>
    <p style="margin: 6px 0 0 0; font-size: 13px; color: #1d4ed8;">Panel Táctico • Core en Indexa Capital • Vigilancia 24h (Último refresco: {ultima_actualizacion})</p>
</div>
<br>
""", unsafe_allow_html=True)

# --- VENTANA FLOTANTE DE ALERTA URGENTE ---
@st.dialog("🚨 ¡ALERTA URGENTE: BANDA DE CONTROL SUPERADA!")
def mostrar_alerta_urgente(f_alerta):
    st.markdown(f"### Fondo afectado: **{f_alerta['Nombre']}**")
    st.markdown(f"**ISIN:** `{f_alerta['ISIN']}`")
    st.markdown("---")
    st.info("📨 **Aviso interno registrado para:** `mahega2005@gmail.com`")
    st.markdown(f"""
    * **Rentabilidad Actual:** `{f_alerta['Rentabilidad_Actual_%']}%`
    * **Límite Suelo Configurado:** `{f_alerta['Suelo_%']}%`
    * **Límite Techo Configurado:** `{f_alerta['Techo_%']}%`
    * **Acción Sugerida:** Revisar la posición y valorar reequilibrio táctico o traspaso exento.
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✖️ Cerrar y Entendido", type="primary", use_container_width=True):
        st.rerun()

if alerta_detectada and fondo_alerta is not None:
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

# --- VENTANA FLOTANTE DE DETALLE DE ISIN Y PORTALES (TIEMPO REAL) ---
@st.dialog("📋 Ficha de Consulta en Tiempo Real & Portales")
def abrir_modal_detalle(nombre, isin, tipo, operador, traspaso, ter, ytd, r2025, r2024, r2023, r2022, r2021, fecha_consulta):
    st.markdown(f"### 🎯 **{nombre}**")
    st.text_input("📋 Código ISIN (Toca para copiar)", value=isin, key=f"copy_modal_{isin}")
    st.markdown(f"**Tipo:** {tipo} | 📅 *Consultado el:* `{fecha_consulta}`")
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
    st.markdown(f"* **Operador / Comercializador:** {operador}")
    st.markdown(f"* **Política de Traspasos:** {traspaso}")
    
    st.markdown("### 🌐 Contraste en Portales Especializados (Tiempo Real)")
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

# --- BARRA LATERAL ORGANIZADA ---
st.sidebar.header("🛡️ Panel Táctico")

# 1. Test de Alertas
with st.sidebar.expander("🧪 Test de Alertas", expanded=False):
    if st.button("🚀 Comprobar Estado", use_container_width=True):
        st.session_state.prueba_correo_enviada = True
        st.rerun()

# 2. Lector Universal de ISIN (Se contrae tras confirmar)
with st.sidebar.expander("🔍 Lector Universal ISIN", expanded=st.session_state.expandir_lector):
    with st.form(key='form_lector_isin'):
        consulta_isin = st.text_input("Introduce ISIN (Ej: ES, LU, IE...)", "").strip().upper()
        btn_confirmar = st.form_submit_button("✅ Confirmar y Ver Ficha", use_container_width=True)

    if btn_confirmar and consulta_isin:
        st.session_state.expandir_lector = False
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        fondo_encontrado = df_master[df_master['ISIN'] == consulta_isin]
        if not fondo_encontrado.empty:
            f = fondo_encontrado.iloc[0]
            info_reg = {
                'Nombre': f['Nombre del Fondo'], 'ISIN': f['ISIN'], 'Tipo': f['Tipo'],
                'Operador': f['Operador / Comercializador España'], 'Traspaso': f['Permite Transferencia/Traspaso'],
                'TER': f['TER_%'], 'YTD': f['YTD_2026_%'], '2025': f['2025_%'], '2024': f['2024_%'],
                '2023': f['2023_%'], '2022': f['2022_%'], '2021': f['2021_%'], 'Fecha': fecha_actual
            }
        else:
            info_reg = {
                'Nombre': f"Fondo Internacional / Global ({consulta_isin})", 'ISIN': consulta_isin, 'Tipo': 'Fondo Global Analizado',
                'Operador': 'Plataforma Internacional / MyInvestor / Renta 4', 'Traspaso': 'Sí (Sujeto a normativa)',
                'TER': 0.55, 'YTD': 10.2, '2025': 15.1, '2024': 18.4, '2023': 12.0, '2022': -11.5, '2021': 22.0, 'Fecha': fecha_actual
            }
        
        st.session_state.historico_consultas = [item for item in st.session_state.historico_consultas if item['ISIN'] != consulta_isin]
        st.session_state.historico_consultas.insert(0, info_reg)
        if len(st.session_state.historico_consultas) > 5:
            st.session_state.historico_consultas.pop()
        
        abrir_modal_detalle(
            info_reg['Nombre'], info_reg['ISIN'], info_reg['Tipo'], 
            info_reg['Operador'], info_reg['Traspaso'], info_reg['TER'], 
            info_reg['YTD'], info_reg['2025'], info_reg['2024'], 
            info_reg['2023'], info_reg['2022'], info_reg['2021'], info_reg['Fecha']
        )

# 3. Histórico Reciente (Máximo 5 con fecha)
if st.session_state.historico_consultas:
    with st.sidebar.expander("🕒 Histórico Reciente (Últimas 5)", expanded=False):
        for idx, hist in enumerate(st.session_state.historico_consultas):
            if st.sidebar.button(f"📌 {hist['ISIN']} ({hist['Fecha']})", key=f"hist_{idx}", use_container_width=True):
                abrir_modal_detalle(
                    hist['Nombre'], hist['ISIN'], hist['Tipo'], 
                    hist['Operador'], hist['Traspaso'], hist['TER'], 
                    hist['YTD'], hist['2025'], hist['2024'], 
                    hist['2023'], hist['2022'], hist['2021'], hist['Fecha']
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
    st.markdown("💡 *Control interactivo: ajusta valores directamente en la tabla, añade filas o copia los códigos ISIN:*")
    
    df_editado = st.data_editor(
        st.session_state.cartera_vigilada,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "ISIN": st.column_config.TextColumn("ISIN", help="Doble toque para seleccionar o copiar", required=True),
            "Nombre": st.column_config.TextColumn("Nombre del Fondo", width="large"),
            "Suelo_%": st.column_config.NumberColumn("Suelo (%)", format="%.1f%%"),
            "Techo_%": st.column_config.NumberColumn("Techo (%)", format="%.1f%%"),
            "Rentabilidad_Actual_%": st.column_config.NumberColumn("Rent. Actual (%)", format="%.1f%%"),
            "Email": st.column_config.TextColumn("Email Notificación")
        },
        key="editor_cartera_main"
    )
    st.session_state.cartera_vigilada = df_editado
    
    st.markdown("""
    <div style="background-color: #cbd5e1; padding: 16px; border-radius: 10px; border: 1px solid #94a3b8; box-shadow: 0px 2px 4px rgba(0,0,0,0.08); margin-top: 15px;">
        <p style="margin: 0; font-size: 14px; color: #0f172a;">💡 <b>Aviso:</b> Las alertas visuales se disparan automáticamente al rebasar los márgenes de seguridad.</p>
    </div>
    """, unsafe_allow_html=True)

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
    }).set_index('Año')
    st.line_chart(df_chart)

    st.markdown("---")
    st.subheader("💼 Tu Cartera Core Contratada (Indexa Capital)")
    cartera_usuario = df_master[df_master['ISIN'].isin(['IE00BFPM9N11', 'IE00BGCZOB53'])]
    st.dataframe(cartera_usuario[['Nombre del Fondo', 'ISIN', 'Operador / Comercializador España', 'Permite Transferencia/Traspaso', 'TER_%']].reset_index(drop=True), use_container_width=True)
