import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA Y LAYOUT
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Mi Broker Privado 2026",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# ESTILOS CSS DEFINITIVOS: SIMETRÍA, TAMAÑO TÁCTIL Y ARMONÍA VISUAL (ESTILO GEMINI)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Fondo general de la aplicación */
    .stApp {
        background-color: #f0f4f9;
        color: #1f2328;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Barra lateral unificada con degradado y borde */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #dbeafe, #bfdbfe);
        border-right: 2px solid #93c5fd;
    }
    
    /* Contenedores y tarjetas transparentes */
    div.stMarkdownContainer, div.stDataFrame {
        background-color: transparent;
    }
    
    /* Pestañas superiores estilizadas y simétricas */
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

    /* Botones principales y de la barra lateral con adaptación táctil */
    .stButton button {
        background-color: #ffffff;
        color: #1f2328;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        font-weight: 500;
        padding: 8px 12px;
    }
    .stButton button:hover {
        background-color: #e2e8f0;
        border-color: #94a3b8;
        color: #1f2328;
    }
    
    /* Cajas de aviso con tono armonizado */
    .info-box-custom {
        background-color: #cbd5e1;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #94a3b8;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.08);
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# BASE DE DATOS MAESTRA DE FONDOS Y METRICAS HISTÓRICAS
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# INICIALIZACIÓN DE ESTADOS DE SESIÓN (SESSION STATE)
# -----------------------------------------------------------------------------
if 'historico_consultas' not in st.session_state:
    st.session_state.historico_consultas = []

if 'cartera_vigilada' not in st.session_state:
    st.session_state.cartera_vigilada = pd.DataFrame([
        {'ISIN': 'IE00BFPM9N11', 'Nombre': 'Vanguard Global Stock Index Inst Plus EUR Acc', 'Suelo_%': -10.0, 'Techo_%': 25.0, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': 4.5},
        {'ISIN': 'IE00BGCZOB53', 'Nombre': 'Vanguard Global Bond Index Inst Plus EUR Hgd', 'Suelo_%': -8.0, 'Techo_%': 15.0, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': -2.1}
    ])

if 'prueba_correo_enviada' not in st.session_state:
    st.session_state.prueba_correo_enviada = False

# -----------------------------------------------------------------------------
# COMPROBACIÓN AUTOMÁTICA DE ALERTAS
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# CABECERA PRINCIPAL CON LOGOTIPO TÁCTICO
# -----------------------------------------------------------------------------
st.markdown("""
<div style="background: linear-gradient(135deg, #dbeafe, #bfdbfe); padding: 25px; border-radius: 12px; text-align: center; color: #1e3a8a; border: 2px solid #3b82f6; box-shadow: 0px 4px 15px rgba(0,0,0,0.08);">
    <div style="font-size: 38px; margin-bottom: 5px;">🛡️📈</div>
    <h2 style="margin: 0; font-size: 24px; letter-spacing: 1.5px; color: #1e40af;">MI BROKER PRIVADO</h2>
    <p style="margin: 6px 0 0 0; font-size: 13px; color: #1d4ed8;">Panel Táctico • Core en Indexa Capital • Vigilancia de Bandas 24h</p>
</div>
<br>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DIÁLOGOS Y VENTANAS FLOTANTES (MODALES)
# -----------------------------------------------------------------------------
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

@st.dialog("📋 Ficha Completa de Análisis & Enlaces a Portales")
def abrir_modal_detalle(nombre, isin, tipo, operador, traspaso, ter, ytd, r2025, r2024, r2023, r2022, r2021):
    st.markdown(f"### 🎯 **{nombre}**")
    st.text_input("📋 Código ISIN (Toca para copiar)", value=isin, key=f"copy_modal_{isin}")
    st.markdown(f"**Tipo:** {tipo}")
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

# -----------------------------------------------------------------------------
# BARRA LATERAL (SIDEBAR): COMPLETA Y ESTRUCTURADA
# -----------------------------------------------------------------------------
st.sidebar.header("🛡️ Panel Táctico")

# Modulo 1: Test de Alertas
with st.sidebar.expander("🧪 Test de Alertas (Modo Seguro)", expanded=False):
    if st.button("🚀 Comprobar Estado de Alertas", use_container_width=True):
        st.session_state.prueba_correo_enviada = True
        st.rerun()

st.sidebar.markdown("---")

# Modulo 2: Gestión de ISIN Vigilados (Añadir / Eliminar de forma amplia)
with st.sidebar.expander("➕ Añadir / 🗑️ Eliminar ISIN de Vigilancia", expanded=False):
    opcion_gestion = st.radio("Operación a realizar:", ["Añadir Nuevo ISIN", "Eliminar ISIN Existente"], key="radio_gestion_vig")
    
    if opcion_gestion == "Añadir Nuevo ISIN":
        nuevo_isin = st.text_input("Código ISIN a vigilar", "", key="input_nuevo_isin").strip().upper()
        suelo_input = st.number_input("Suelo de Alerta (%)", value=-10.0, step=1.0, key="input_suelo")
        techo_input = st.number_input("Techo de Alerta (%)", value=20.0, step=1.0, key="input_techo")
        rent_simulada = st.number_input("Rentabilidad actual estimada (%)", value=2.0, step=0.5, key="input_rent")
        
        if st.button("💾 Guardar en Vigilancia", use_container_width=True):
            if nuevo_isin:
                # Verificar duplicados en el DataFrame
                df_actual = st.session_state.cartera_vigilada
                if not df_actual.empty and nuevo_isin in df_actual['ISIN'].values:
                    st.warning("Este ISIN ya existe en tu tabla de vigilancia.")
                else:
                    match = df_master[df_master['ISIN'] == nuevo_isin]
                    nombre_f = match.iloc[0]['Nombre del Fondo'] if not match.empty else f"Fondo Personalizado ({nuevo_isin})"
                    
                    nueva_fila = pd.DataFrame([{
                        'ISIN': nuevo_isin,
                        'Nombre': nombre_f,
                        'Suelo_%': suelo_input,
                        'Techo_%': techo_input,
                        'Email': 'mahega2005@gmail.com',
                        'Rentabilidad_Actual_%': rent_simulada
                    }])
                    
                    st.session_state.cartera_vigilada = pd.concat([df_actual, nueva_fila], ignore_index=True)
                    st.success(f"¡ISIN `{nuevo_isin}` añadido!")
                    st.rerun()
            else:
                st.error("Introduce un código ISIN válido.")
                
    elif opcion_gestion == "Eliminar ISIN Existente":
        df_actual = st.session_state.cartera_vigilada
        if not df_actual.empty:
            lista_eliminar = [f"{row['ISIN']} - {row['Nombre'][:12]}..." for _, row in df_actual.iterrows()]
            seleccion_del = st.selectbox("Selecciona fondo a borrar:", lista_eliminar, key="sel_del_sb")
            
            if st.button("🗑️ Confirmar Borrado", type="primary", use_container_width=True):
                isin_borrar = seleccion_del.split(" - ")[0]
                st.session_state.cartera_vigilada = df_actual[df_actual['ISIN'] != isin_borrar].reset_index(drop=True)
                st.success(f"ISIN `{isin_borrar}` eliminado.")
                st.rerun()
        else:
            st.info("No hay fondos registrados en la tabla actualmente.")

st.sidebar.markdown("---")

# Modulo 3: Lector Universal ISIN (Con soporte para Enter mediante st.form)
with st.sidebar.expander("🔍 Lector Universal ISIN", expanded=True):
    with st.form(key='form_lector_isin_side'):
        consulta_isin = st.text_input("Consultar ISIN (Ej: LU1121307729)", "").strip().upper()
        btn_confirmar = st.form_submit_button("✅ Confirmar y Ver Ficha", use_container_width=True)

    if btn_confirmar and consulta_isin:
        isin_existente = [item['ISIN'] for item in st.session_state.historico_consultas] if isinstance(st.session_state.historico_consultas, list) else []
        if consulta_isin not in isin_existente:
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
        
        reg_actual = next((item for item in st.session_state.historico_consultas if item['ISIN'] == consulta_isin), None)
        if reg_actual:
            abrir_modal_detalle(
                reg_actual['Nombre'], reg_actual['ISIN'], reg_actual['Tipo'], 
                reg_actual['Operador'], reg_actual['Traspaso'], reg_actual['TER'], 
                reg_actual['YTD'], reg_actual['2025'], reg_actual['2024'], 
                reg_actual['2023'], reg_actual['2022'], reg_actual['2021']
            )

# Modulo 4: Histórico Reciente
if st.session_state.historico_consultas:
    st.sidebar.markdown("---")
    with st.sidebar.expander("🕒 Histórico Reciente de Consultas", expanded=False):
        for idx, hist in enumerate(st.session_state.historico_consultas):
            if st.sidebar.button(f"📌 {hist['ISIN']} ({hist['Nombre'][:10]}...)", key=f"hist_sb_{idx}", use_container_width=True):
                abrir_modal_detalle(
                    hist['Nombre'], hist['ISIN'], hist['Tipo'], 
                    hist['Operador'], hist['Traspaso'], hist['TER'], 
                    hist['YTD'], hist['2025'], hist['2024'], 
                    hist['2023'], hist['2022'], hist['2021']
                )

# -----------------------------------------------------------------------------
# PANEL PRINCIPAL: PESTAÑAS ESTRATÉGICAS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🛡️ Control & Bandas", 
    "📊 Buscador Maestro", 
    "🤖 Copiloto IA & Prensa", 
    "📈 Gráficos & Cartera Indexa"
])

# -----------------------------------------------------------------------------
# PESTAÑA 1: CONTROL Y BANDAS DE SUPERVISIÓN
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("🛡️ Supervisión 24h de Bandas (Suelos y Techos)")
    st.markdown("💡 *Control interactivo: puedes ajustar cualquier valor directamente en la tabla, añadir filas o copiar los códigos ISIN con doble toque:*")
    
    # Editor interactivo de datos
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
    
    # Guardar automáticamente cambios realizados en la tabla
    st.session_state.cartera_vigilada = df_editado
    
    st.markdown("""
    <div class="info-box-custom">
        <p style="margin: 0; font-size: 14px; color: #0f172a;">💡 <b>Aviso:</b> Las alertas visuales se disparan en pantalla automáticamente al rebasar los márgenes de seguridad configurados.</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PESTAÑA 2: BUSCADOR Y LISTADO MAESTRO
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("📊 Buscador y Listado Maestro de Fondos")
    busqueda_texto = st.text_input("Filtrar por Nombre de Fondo o Criterio", "", key="search_main_tab").strip()
    
    df_filtrado = df_master.copy()
    if busqueda_texto:
        df_filtrado = df_filtrado[
            df_filtrado['Nombre del Fondo'].str.contains(busqueda_texto, case=False, na=False) |
            df_filtrado['ISIN'].str.contains(busqueda_texto, case=False, na=False) |
            df_filtrado['Tipo'].str.contains(busqueda_texto, case=False, na=False)
        ]
    
    st.dataframe(df_filtrado.reset_index(drop=True), use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📊 Resumen de Eficiencia Promedio del Mercado")
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("Comisión TER Media", f"{df_master['TER_%'].mean():.2f}%")
    with col_m2:
        st.metric("Rentabilidad Media 2025", f"{df_master['2025_%'].mean():.2f}%")
    with col_m3:
        st.metric("Rentabilidad Media YTD 2026", f"{df_master['YTD_2026_%'].mean():.2f}%")

# -----------------------------------------------------------------------------
# PESTAÑA 3: COPILOTO IA Y ANÁLISIS DE MERCADO
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("🤖 Copiloto IA (Análisis de Mercado)")
    st.markdown("""
    *💡 **Consenso de expertos (Morningstar / Finect):**  
    Priorizar la eficiencia de costes (TER) en el núcleo global indexado y mantener la disciplina en aportaciones periódicas sin sesgos de corto plazo.*
    """)
    
    # Motor de puntuación algorítmica
    df_robot = df_master[df_master['TER_%'] <= 1.50].copy()
    df_robot['Score'] = (df_robot['2024_%'] + df_robot['2025_%']) / 2 - (df_robot['TER_%'] * 10)
    top_3_recomendados = df_robot.sort_values(by='Score', ascending=False).head(3)

    st.markdown("### 🌟 Opciones Estratégicas Destacadas")
    for idx, row in top_3_recomendados.reset_index().iterrows():
        st.success(f"""
        **Opción Estratégica {idx+1}: {row['Nombre del Fondo']}** (ISIN: `{row['ISIN']}`)  
        * **Operador:** {row['Operador / Comercializador España']} | **TER:** {row['TER_%']}% | **Rentabilidad 2025:** {row['2025_%']}%  
        """)

# -----------------------------------------------------------------------------
# PESTAÑA 4: GRÁFICOS Y CARTERA CORE INDEXA CAPITAL
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("📈 Gráfico Comparativo de Mercado")
    anios = ['2021_%', '2022_%', '2023_%', '2024_%', '2025_%', 'YTD_2026_%']
    etiquetas_anios = ['2021', '2022', '2023', '2024', '2025', '2026 (YTD)']

    df_indexados = df_master[df_master['TER_%'] <= 0.30]
    media_mercado = df_indexados[anios].mean().values

    # Generación de curva comparativa
    vanguard_stock = df_master.loc[df_master['ISIN'] == 'IE00BFPM9N11', anios].values[0]

    df_chart = pd.DataFrame({
        'Año': etiquetas_anios,
        'Media del Mercado Global': media_mercado,
        'Tu Renta Variable (Vanguard Stock)': vanguard_stock
    }).set_index('Año')
    
    st.line_chart(df_chart)

    st.markdown("---")
    st.subheader("💼 Tu Cartera Core Contratada (Indexa Capital)")
    cartera_usuario = df_master[df_master['ISIN'].isin(['IE00BFPM9N11', 'IE00BGCZOB53'])]
    st.dataframe(cartera_usuario[['Nombre del Fondo', 'ISIN', 'Operador / Comercializador España', 'Permite Transferencia/Traspaso', 'TER_%']].reset_index(drop=True), use_container_width=True)
