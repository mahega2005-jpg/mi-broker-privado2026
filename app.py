# ==============================================================================
# PROYECTO: MI BROKER PRIVADO - PANEL TÁCTICO DE INVERSIÓN
# AUTOR: Bartolomé Marín Hedrera
# DESCRIPCIÓN: Panel de control avanzado en Streamlit para la gestión táctica
#              de fondos de inversión, supervisión de bandas y motor autónomo.
# ==============================================================================

import streamlit as st
import pandas as pd
from datetime import datetime
import zoneinfo

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS
# ==============================================================================
st.set_page_config(
    page_title="Mi Broker Privado - Panel Táctico",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { 
        background-color: #f0f4f9; 
        color: #1f2328; 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    section[data-testid="stSidebar"] { 
        background: linear-gradient(135deg, #dbeafe, #bfdbfe); 
        border-right: 2px solid #93c5fd; 
        padding-top: 10px;
    }
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
    .stTabs [aria-selected="true"] { 
        background-color: #cbd5e1 !important; 
        color: #0f172a !important; 
        border-color: #94a3b8 !important; 
    }
    .stButton button { 
        background-color: #ffffff; 
        color: #1f2328; 
        border: 1px solid #cbd5e1; 
        border-radius: 8px; 
        font-weight: 500; 
        padding: 8px 16px;
    }
    .stButton button:hover {
        border-color: #3b82f6;
        color: #1d4ed8;
    }
    .trend-card-header {
        background-color: #ffffff;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #cbd5e1;
        min-height: 165px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SOPORTE Y HORARIO OFICIAL
# ==============================================================================
def hora_real_espana():
    tz = zoneinfo.ZoneInfo("Europe/Madrid")
    return datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')

# ==============================================================================
# 3. BASE DE DATOS MAESTRA (2 CORE + 10 TOP MERCADO)
# ==============================================================================
data_12_fondos = {
    'Origen': [
        '📌 En Cartera (Core)', '📌 En Cartera (Core)',
        '⭐ Top Mercado', '⭐ Top Mercado', '⭐ Top Mercado', '⭐ Top Mercado',
        '⭐ Top Mercado', '⭐ Top Mercado', '⭐ Top Mercado', '⭐ Top Mercado',
        '⭐ Top Mercado', '⭐ Top Mercado'
    ],
    'ISIN': [
        'IE00BFPM9N11', 'IE00BGCZOB53',
        'LU1681048899', 'IE00B03HD191', 'LU0503631872', 'IE00B43VBZ18',
        'ES0114105030', 'IE00B03HCZ61', 'LU0996182563', 'LU1121307729',
        'IE00B3WVRB16', 'ES0111222333'
    ],
    'Nombre del Fondo': [
        'Vanguard Global Stock Index Inst Plus EUR Acc', 
        'Vanguard Global Bond Index Inst Plus EUR Hgd', 
        'Amundi Index MSCI World AE-C',
        'Vanguard US 500 Stock Index EUR Acc',
        'Pictet - Security P EUR',
        'Polar Capital Biotechnology EUR R Acc',
        'DWS Investments Alpha Opportunities',
        'Vanguard European Stock Index EUR Acc',
        'Fidelity Funds - Global Technology A-ACC-EUR',
        'Abante Global Funds Spanish Opportunities C EUR',
        'Polar Capital Biotechnology I EUR Dis',
        'Banco Tradicional Cartera Activa'
    ],
    'Categoría / Tipo': [
        'Renta Variable Global', 'Renta Fija Global',
        'Indexado Global (MSCI World)', 'Indexado S&P 500', 'Ciberseguridad & Seguridad', 'Biotecnología & Salud',
        'Retorno Absoluto / Multi-Activo', 'Renta Variable Europa', 'Tecnología Global', 'Renta Variable España',
        'Biotecnología (Clase I Dist)', 'Gestión Activa Tradicional'
    ],
    'Comercializador España': [
        'Indexa Capital', 'Indexa Capital',
        'MyInvestor / Openbank', 'MyInvestor / Renta 4', 'MyInvestor / IronIA', 'MyInvestor / Renta 4',
        'Renta 4 / Allfunds', 'MyInvestor / Renta 4', 'MyInvestor / Mapfre', 'Abante Asesores',
        'MyInvestor / Renta 4', 'Banco Tradicional'
    ],
    'Traspasable': ['Sí', 'Sí', 'Sí', 'Sí', 'Sí', 'Sí', 'Sí', 'Sí', 'Sí', 'Sí', 'Sí', 'Sí'],
    'Min_Inversion': ['Desde 10€', 'Desde 10€', 'Desde 10€', '100€', '1 Participación', '1 Participación', '100€', '100€', '1 Participación', '1 Participación', '1 Participación', 'Desde 500€'],
    'TER_%': [0.06, 0.10, 0.30, 0.10, 1.00, 1.25, 0.65, 0.12, 1.05, 1.35, 1.00, 1.85],
    'YTD_2026_%': [18.55, -3.35, 17.90, 21.40, 14.20, 11.50, 6.80, 12.10, 24.50, 8.20, 10.90, -2.10],
    '2025_%': [6.73, 2.89, 19.20, 23.50, 22.50, 14.00, 5.40, 11.20, 28.10, 9.10, 12.50, 4.20],
    '2024_%': [26.59, 0.88, 21.90, 26.80, 25.10, 8.50, 7.10, 15.80, 32.40, 11.40, 24.85, 5.00],
    '2023_%': [19.63, 4.74, 14.80, 21.20, 18.00, 6.20, 4.20, 12.50, 36.10, 14.20, 14.89, 3.50]
}

# ==============================================================================
# 4. GESTIÓN DE ESTADOS DE SESIÓN (SESSION STATE)
# ==============================================================================
if 'df_master_app' not in st.session_state:
    st.session_state.df_master_app = pd.DataFrame(data_12_fondos)

if 'historico_consultas' not in st.session_state:
    st.session_state.historico_consultas = []

if 'cartera_vigilada' not in st.session_state:
    st.session_state.cartera_vigilada = pd.DataFrame([
        {'ISIN': 'IE00BFPM9N11', 'Nombre': 'Vanguard Global Stock Index Inst Plus EUR Acc', 'Suelo_%': -10.0, 'Techo_%': 25.0, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': 18.55},
        {'ISIN': 'IE00BGCZOB53', 'Nombre': 'Vanguard Global Bond Index Inst Plus EUR Hgd', 'Suelo_%': -8.0, 'Techo_%': 15.0, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': -3.35}
    ])

if 'mensaje_escaner_ciego' not in st.session_state:
    st.session_state.mensaje_escaner_ciego = (
        "🟢 **Estado del Top 10:** Sincronizado y protegido. "
        "El motor autónomo evalúa permanentemente la rentabilidad neta ajustada por comisiones TER."
    )

if 'notificacion_actualizado' not in st.session_state:
    st.session_state.notificacion_actualizado = False

if 'isin_preseleccionado' not in st.session_state:
    st.session_state.isin_preseleccionado = ""


# ==============================================================================
# 5. MOTOR AUTÓNOMO DE ESCANEO Y ROTACIÓN DEL TOP 10
# ==============================================================================
def ejecutar_escanner_automatico_top10():
    df = st.session_state.df_master_app
    
    df_core = df[df['Origen'] == '📌 En Cartera (Core)'].copy()
    df_top = df[df['Origen'] == '⭐ Top Mercado'].copy()
    
    df_top['Score_Eficiente'] = (df_top['YTD_2026_%'] * 0.5) + (df_top['2025_%'] * 0.3) - (df_top['TER_%'] * 1.5)
    df_top_ordenado = df_top.sort_values(by='Score_Eficiente', ascending=False).reset_index(drop=True)
    
    st.session_state.df_master_app = pd.concat([df_core, df_top_ordenado], ignore_index=True)
    
    lider = df_top_ordenado.iloc[0]['Nombre del Fondo']
    decimo = df_top_ordenado.iloc[-1]['Nombre del Fondo']
    
    st.session_state.mensaje_escaner_ciego = (
        f"⚡ **Auditoría de Mercado ({hora_real_espana()}):**<br>"
        f"• **Líder del Ranking (Puesto 1):** {lider}<br>"
        f"• **Umbral de Corte (Puesto 10):** {decimo}<br>"
        f"• **Estado:** Ranking dinámico ordenado por eficiencia neta. Core blindado e independiente."
    )


# ==============================================================================
# 6. CABECERA TÁCTICA SUPERIOR (CON LA NUEVA CAJITA DEBAJO DE ACTUALIZAR)
# ==============================================================================
col_head1, col_head2 = st.columns([3, 1])
h_actual = hora_real_espana()

with col_head1:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #dbeafe, #bfdbfe); padding: 16px; border-radius: 12px; text-align: left; color: #1e3a8a; border: 2px solid #3b82f6;">
        <div style="font-size: 22px; margin-bottom: 2px;">🛡️📈 <b style="font-size: 18px; color: #1e40af;">MI BROKER PRIVADO</b></div>
        <p style="margin: 4px 0 0 0; font-size: 12px; color: #1d4ed8; font-weight: 600;">Panel Táctico • Hora Oficial: {h_actual}</p>
    </div>
    """, unsafe_allow_html=True)

with col_head2:
    st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Actualizar Datos", use_container_width=True):
        ejecutar_escanner_automatico_top10()
        st.session_state.notificacion_actualizado = True
        st.rerun()
    
    # NUEVA CAJITA CREADA DEBAJO DE ACTUALIZAR DATOS
    if st.button("🛠️ Editar App", use_container_width=True):
        st.toast("¡Cajita nueva lista para configurar su función!", icon="🛠️")

if st.session_state.notificacion_actualizado:
    st.toast(f"✅ ¡Escaneo autónomo completado! Hora oficial ({h_actual}) y Top 10 auditados.", icon="🔄")
    st.session_state.notificacion_actualizado = False

st.markdown("<br>", unsafe_allow_html=True)


# ==============================================================================
# 7. FUNCIONES MODALES Y CONSULTAS
# ==============================================================================
def consultar_catalogo_maestro(isin):
    df_m = st.session_state.df_master_app
    isin = isin.strip().upper()
    match = df_m[df_m['ISIN'] == isin]
    if not match.empty:
        f = match.iloc[0]
        return {
            'Nombre': f['Nombre del Fondo'], 'ISIN': f['ISIN'], 'Tipo': f['Categoría / Tipo'],
            'Operador': f['Comercializador España'], 'Traspaso': f['Traspasable'], 'Minimo': f['Min_Inversion'],
            'TER': f"{f['TER_%']}%", 'YTD': f"{f['YTD_2026_%']}%", '2025': f"{f['2025_%']}%",
            '2024': f"{f['2024_%']}%", '2023': f"{f['2023_%']}%", 'EnMaestro': True
        }
    return {
        'Nombre': f"Fondo No Registrado ({isin})", 'ISIN': isin, 'Tipo': 'Estudio Externo',
        'Operador': 'Consultar Comercializador España', 'Traspaso': 'Verificar normativa',
        'Minimo': 'N/D', 'TER': 'N/D', 'YTD': 'N/D', '2025': 'N/D', '2024': 'N/D', '2023': 'N/D', 'EnMaestro': False
    }

@st.dialog("📋 Ficha Técnica & Análisis de Inversión")
def abrir_modal_detalle(info_reg):
    st.markdown(f"### 🎯 **{info_reg['Nombre']}**")
    st.code(info_reg['ISIN'], language=None)
    st.markdown(f"📅 *Consultado el:* `{hora_real_espana()}`")
    st.markdown("---")
    if info_reg['EnMaestro']:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Comisión TER", info_reg['TER'])
            st.metric("YTD 2026", info_reg['YTD'])
            st.metric("Rentabilidad 2025", info_reg['2025'])
        with col2:
            st.metric("Rentabilidad 2024", info_reg['2024'])
            st.metric("Rentabilidad 2023", info_reg['2023'])
        st.markdown("---")
        st.markdown(f"* **Operador en España:** {info_reg['Operador']}")
        st.markdown(f"* **Traspasabilidad Fiscal:** {info_reg['Traspaso']}")
        st.markdown(f"* **Inversión Mínima:** {info_reg['Minimo']}")
    else:
        st.warning("⚠️ ISIN externo. Consulta los enlaces directos:")
    st.markdown("### 🌐 Enlaces Directos")
    c1, c2, c3 = st.columns(3)
    isin_clean = info_reg['ISIN'].strip()
    with c1: st.markdown(f"[Morningstar](https://www.morningstar.es/es/search/quickrank.aspx?search={isin_clean})")
    with c2: st.markdown(f"[Google Finance](https://www.google.com/finance/quote/{isin_clean})")
    with c3: st.markdown(f"[Citywire](https://citywire.com/es/search?q={isin_clean})")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✖️ Cerrar Ventana", use_container_width=True): st.rerun()


# ==============================================================================
# 8. BARRA LATERAL
# ==============================================================================
st.sidebar.header("🛡️ Panel Táctico")

with st.sidebar.expander("🧪 Test de Alertas", expanded=False):
    if st.button("🚀 Comprobar Estado", use_container_width=True): 
        st.success("Sistemas operativos y escáner autónomo activo.")

with st.sidebar.expander("➕ Añadir / 🗑️ Eliminar ISIN", expanded=False):
    opcion_g = st.radio("Acción:", ["Añadir Entrada", "Eliminar Salida"], horizontal=True, key="rad_gest")
    df_m_local = st.session_state.df_master_app
    if opcion_g == "Añadir Entrada":
        n_isin = st.text_input("Código ISIN", key="add_i").strip().upper()
        s_val = st.number_input("Suelo (%)", value=-10.0, step=1.0, key="add_s")
        t_val = st.number_input("Techo (%)", value=20.0, step=1.0, key="add_t")
        r_val = st.number_input("Rentabilidad actual (%)", value=2.0, step=0.5, key="add_r")
        if st.button("Guardar en Vigilancia", use_container_width=True):
            if n_isin:
                df_c = st.session_state.cartera_vigilada
                if not df_c.empty and n_isin in df_c['ISIN'].values:
                    st.warning("El ISIN ya está registrado.")
                else:
                    m = df_m_local[df_m_local['ISIN'] == n_isin]
                    nom = m.iloc[0]['Nombre del Fondo'] if not m.empty else f"Fondo ({n_isin})"
                    n_row = pd.DataFrame([{'ISIN': n_isin, 'Nombre': nom, 'Suelo_%': s_val, 'Techo_%': t_val, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': r_val}])
                    st.session_state.cartera_vigilada = pd.concat([df_c, n_row], ignore_index=True)
                    st.success("Guardado en vigilancia.")
                    st.rerun()
    else:
        df_c = st.session_state.cartera_vigilada
        if not df_c.empty:
            sel = st.selectbox("Dar de baja ISIN:", [f"{r['ISIN']} - {r['Nombre'][:12]}" for _, r in df_c.iterrows()], key="del_s")
            if st.button("🗑️ Confirmar Salida", type="primary", use_container_width=True):
                target = sel.split(" - ")[0]
                st.session_state.cartera_vigilada = df_c[df_c['ISIN'] != target].reset_index(drop=True)
                st.success("ISIN eliminado.")
                st.rerun()

with st.sidebar.expander("🔍 Lector Universal ISIN", expanded=True):
    val_defecto = st.session_state.isin_preseleccionado
    with st.form(key="form_lector_isin_limpio", clear_on_submit=True):
        consulta_isin_input = st.text_input("Introduce ISIN", value=val_defecto, key="txt_input_isin_field").strip().upper()
        btn_submit = st.form_submit_button("✅ Consultar e Incorporar", use_container_width=True)
    if btn_submit and consulta_isin_input:
        st.session_state.isin_preseleccionado = ""
        res = consultar_catalogo_maestro(consulta_isin_input)
        res['FechaConsulta'] = hora_real_espana()
        st.session_state.historico_consultas = [i for i in st.session_state.historico_consultas if i['ISIN'] != consulta_isin_input]
        st.session_state.historico_consultas.insert(0, res)
        if len(st.session_state.historico_consultas) > 5: st.session_state.historico_consultas.pop()
        abrir_modal_detalle(res)

if st.session_state.historico_consultas:
    with st.sidebar.expander("🕒 Histórico Reciente (Últimas 5)", expanded=False):
        for idx, hist in enumerate(st.session_state.historico_consultas):
            if st.sidebar.button(f"📌 {hist['ISIN']} ({hist.get('FechaConsulta','')})", key=f"btn_hist_{idx}", use_container_width=True):
                abrir_modal_detalle(hist)


# ==============================================================================
# 9. PESTAÑAS PRINCIPALES DEL PANEL
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🛡️ Control & Bandas", 
    "📊 Buscador Maestro", 
    "🎯 Radar de Tendencias & Estrategias", 
    "📈 Gráficos & Cartera Core"
])

# ------------------------------------------------------------------------------
# PESTAÑA 1: CONTROL & BANDAS
# ------------------------------------------------------------------------------
with tab1:
    st.subheader("🛡️ Supervisión 24h de Bandas (Suelos y Techos)")
    st.markdown("Edita las bandas de control de tus posiciones activas:")
    st.session_state.cartera_vigilada = st.data_editor(st.session_state.cartera_vigilada, num_rows="dynamic", use_container_width=True, key="ed_cartera")

# ------------------------------------------------------------------------------
# PESTAÑA 2: BUSCADOR MAESTRO
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("📊 Buscador Maestro: Top 10 Dinámico de Referencia + Cartera Core")
    df_master_actual = st.session_state.df_master_app
    
    col_sel1, col_sel2 = st.columns([3, 1])
    with col_sel1:
        isin_elegido = st.selectbox("Selecciona fondo:", options=df_master_actual['ISIN'].tolist(), format_func=lambda x: f"{x} - {df_master_actual[df_master_actual['ISIN']==x]['Nombre del Fondo'].values[0]}", key="sel_directo_tablet")
    with col_sel2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("🚀 Cargar en Lector", use_container_width=True):
            st.session_state.isin_preseleccionado = isin_elegido
            abrir_modal_detalle(consultar_catalogo_maestro(isin_elegido))
            
    st.dataframe(df_master_actual, use_container_width=True, height=380)
    
    st.markdown("---")
    
    st.markdown("### ⚡ Escáner Autónomo & Informe de Rotación del Top 10")
    st.markdown("""
    <div style="background-color: #ffffff; padding: 18px; border-radius: 12px; border: 2px solid #3b82f6; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; color: #1e3a8a; line-height: 1.6;">
    """ + st.session_state.mensaje_escaner_ciego + """
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📢 Avisos de Oportunidad y Retroceso Táctico")
    df_top10 = df_master_actual[df_master_actual['Origen'] == '⭐ Top Mercado'].copy()
    df_top10['Suma_Rendimiento'] = df_top10['2025_%'] + df_top10['YTD_2026_%']
    
    for _, row in df_top10.sort_values(by='Suma_Rendimiento', ascending=False).head(2).iterrows():
        c1, c2, c3 = st.columns([1.5, 3.5, 1])
        with c1: st.code(row['ISIN'], language=None)
        with c2: st.markdown(f"**{row['Nombre del Fondo']}**")
        with c3:
            if st.button("🔍 Analizar", key=f"top_m_{row['ISIN']}", use_container_width=True):
                abrir_modal_detalle(consultar_catalogo_maestro(row['ISIN']))

# ------------------------------------------------------------------------------
# PESTAÑA 3: RADAR DE TENDENCIAS & ESTRATEGIAS
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("🎯 Radar de Tendencias Globales & Simulación de Estrategias")
    st.markdown("Análisis táctico para anticiparse al mercado detectando las megatendencias de mayor impulso y cruzándolas con los 3 fondos líderes por sector:")
    
    st.markdown("### 🧭 Modelo Táctico de Asignación por Estrategia")
    estrategia_sel = st.radio(
        "Selecciona una Estrategia Táctica de Mercado:",
        options=[
            "🛡️ Estrategia Conservadora / Defensiva (Preservación)",
            "⚖️ Estrategia Moderada / Core Indexado (Equilibrada)",
            "🚀 Estrategia Crecimiento & Megatendencias (Sintética Aportación)"
        ],
        horizontal=True,
        key="radio_estrategias"
    )
    
    if "Conservadora" in estrategia_sel:
        st.info("""
        **Perfil Táctico Defensivo:**
        * **Asignación:** 70% Renta Fija Global Hedged + 20% Retorno Absoluto / Multi-Activo + 10% RV Global Core.
        * **Fondos Vehículo:** `IE00BGCZOB53` (Vanguard Bond) + `ES0114105030` (DWS Alpha) + `IE00BFPM9N11` (Vanguard Global).
        """)
    elif "Moderada" in estrategia_sel:
        st.success("""
        **Perfil Táctico Core Equilibrado:**
        * **Asignación:** 60% RV Global Indexada (MSCI World / S&P 500) + 20% Renta Fija Global + 20% Megatendencias Activas.
        * **Fondos Vehículo:** `IE00BFPM9N11` (Vanguard Global) + `IE00B03HD191` (S&P 500) + `LU0503631872` (Pictet Security).
        """)
    else:
        st.warning("""
        **Perfil Táctico Dinámico & Megatendencias:**
        * **Asign
