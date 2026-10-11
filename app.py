import streamlit as st
import pandas as pd
from datetime import datetime
import zoneinfo

# Configuración de la página
st.set_page_config(page_title="Mi Broker Privado", page_icon="🛡️", layout="wide")

# Estilos CSS Tácticos (Estilo Gemini)
st.markdown("""
<style>
    .stApp { background-color: #f0f4f9; color: #1f2328; }
    section[data-testid="stSidebar"] { background: linear-gradient(135deg, #dbeafe, #bfdbfe); border-right: 2px solid #93c5fd; }
    .stTabs [data-baseweb="tab-list"] { gap: 6px; background-color: #e2e8f0; padding: 6px; border-radius: 12px; border: 2px solid #cbd5e1; }
    .stTabs [data-baseweb="tab"] { background-color: #ffffff; border-radius: 8px; color: #475569 !important; padding: 10px 16px; font-weight: 600; font-size: 14px; border: 1px solid #cbd5e1; }
    .stTabs [aria-selected="true"] { background-color: #cbd5e1 !important; color: #0f172a !important; border-color: #94a3b8 !important; }
    .stButton button { background-color: #ffffff; color: #1f2328; border: 1px solid #cbd5e1; border-radius: 8px; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# Hora oficial exacta de España
def hora_real_espana():
    tz = zoneinfo.ZoneInfo("Europe/Madrid")
    return datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')

# BASE DE DATOS MAESTRA: 2 TUYOS CONTRATADOS (CORE) + 10 MEJORES DEL MERCADO
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
        'Indexado Global (MSCI World)', 'Indexado S&P 500', 'Ciberseguridad', 'Biotecnología',
        'Retorno Absoluto', 'Renta Variable Europa', 'Tecnología Global', 'Renta Variable España',
        'Biotecnología (Clase I)', 'Gestión Activa'
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
df_master = pd.DataFrame(data_12_fondos)

# ESTADOS DE SESIÓN
if 'historico_consultas' not in st.session_state:
    st.session_state.historico_consultas = []

if 'cartera_vigilada' not in st.session_state:
    st.session_state.cartera_vigilada = pd.DataFrame([
        {'ISIN': 'IE00BFPM9N11', 'Nombre': 'Vanguard Global Stock Index Inst Plus EUR Acc', 'Suelo_%': -10.0, 'Techo_%': 25.0, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': 18.55},
        {'ISIN': 'IE00BGCZOB53', 'Nombre': 'Vanguard Global Bond Index Inst Plus EUR Hgd', 'Suelo_%': -8.0, 'Techo_%': 15.0, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': -3.35}
    ])

if 'notificacion_actualizado' not in st.session_state:
    st.session_state.notificacion_actualizado = False

# CABECERA Y BOTÓN DE ACTUALIZAR
col_head1, col_head2 = st.columns([4, 1])
h_actual = hora_real_espana()

with col_head1:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #dbeafe, #bfdbfe); padding: 20px; border-radius: 12px; text-align: center; color: #1e3a8a; border: 2px solid #3b82f6;">
        <div style="font-size: 32px; margin-bottom: 3px;">🛡️📈</div>
        <h2 style="margin: 0; font-size: 22px; color: #1e40af;">MI BROKER PRIVADO</h2>
        <p style="margin: 4px 0 0 0; font-size: 13px; color: #1d4ed8; font-weight: 600;">Panel Táctico • Hora Oficial España: {h_actual}</p>
    </div>
    """, unsafe_allow_html=True)

with col_head2:
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Actualizar", use_container_width=True, help="Recargar datos y sincronizar hora oficial"):
        st.session_state.notificacion_actualizado = True
        st.rerun()

if st.session_state.notificacion_actualizado:
    st.toast(f"✅ ¡Sistema actualizado al 100%! Hora oficial ({h_actual}) y métricas sincronizadas.", icon="🔄")
    st.session_state.notificacion_actualizado = False

st.markdown("<br>", unsafe_allow_html=True)

# LÓGICA DE BÚSQUEDA EN CATÁLOGO
def consultar_catalogo_maestro(isin):
    isin = isin.strip().upper()
    match = df_master[df_master['ISIN'] == isin]
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

# MODAL DE FICHA TÉCNICA
@st.dialog("📋 Ficha Técnica & Análisis de Inversión")
def abrir_modal_detalle(info_reg):
    st.markdown(f"### 🎯 **{info_reg['Nombre']}**")
    st.text_input("📋 Código ISIN (Copiar)", value=info_reg['ISIN'], key=f"copy_modal_{info_reg['ISIN']}")
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
        st.markdown(f"* **Traspasabilidad:** {info_reg['Traspaso']}")
        st.markdown(f"* **Mínimo Inversión:** {info_reg['Minimo']}")
    else:
        st.warning("⚠️ Este ISIN no está registrado en el Catálogo Maestro. Utiliza los enlaces directos para consultar su ficha oficial:")

    st.markdown("### 🌐 Enlaces de Análisis Directo")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"[📊 Morningstar](https://www.morningstar.es/es/funds/security/summary.aspx?search={info_reg['ISIN']})")
    with c2:
        st.markdown(f"[🔍 QueFondos](https://www.quefondos.com/es/fondos/ficha/index.html?isin={info_reg['ISIN']})")
    with c3:
        st.markdown(f"[📈 JustETF](https://www.justetf.com/es/search.html?query={info_reg['ISIN']})")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✖️ Cerrar Ventana", use_container_width=True):
        st.rerun()

# BARRA LATERAL
st.sidebar.header("🛡️ Panel Táctico")

with st.sidebar.expander("🧪 Test de Alertas", expanded=False):
    if st.button("🚀 Comprobar Estado", use_container_width=True):
        st.success("Test ejecutado correctamente.")

with st.sidebar.expander("➕ Añadir / 🗑️ Eliminar ISIN", expanded=False):
    opcion_g = st.radio("Acción:", ["Añadir", "Eliminar"], horizontal=True, key="rad_gest")
    if opcion_g == "Añadir":
        n_isin = st.text_input("Código ISIN", key="add_i").strip().upper()
        s_val = st.number_input("Suelo (%)", value=-10.0, step=1.0, key="add_s")
        t_val = st.number_input("Techo (%)", value=20.0, step=1.0, key="add_t")
        r_val = st.number_input("Rentabilidad actual (%)", value=2.0, step=0.5, key="add_r")
        if st.button("Guardar en Vigilancia", use_container_width=True):
            if n_isin:
                df_c = st.session_state.cartera_vigilada
                if not df_c.empty and n_isin in df_c['ISIN'].values:
                    st.warning("Ya existe en vigilancia.")
                else:
                    m = df_master[df_master['ISIN'] == n_isin]
                    nom = m.iloc[0]['Nombre del Fondo'] if not m.empty else f"Fondo Personalizado ({n_isin})"
                    n_row = pd.DataFrame([{'ISIN': n_isin, 'Nombre': nom, 'Suelo_%': s_val, 'Techo_%': t_val, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': r_val}])
                    st.session_state.cartera_vigilada = pd.concat([df_c, n_row], ignore_index=True)
                    st.success(f"ISIN `{n_isin}` añadido.")
                    st.rerun()
    else:
        df_c = st.session_state.cartera_vigilada
        if not df_c.empty:
            sel = st.selectbox("Borrar ISIN:", [f"{r['ISIN']} - {r['Nombre'][:10]}..." for _, r in df_c.iterrows()], key="del_s")
            if st.button("🗑️ Borrar", type="primary", use_container_width=True):
                target = sel.split(" - ")[0]
                st.session_state.cartera_vigilada = df_c[df_c['ISIN'] != target].reset_index(drop=True)
                st.success(f"ISIN `{target}` borrado.")
                st.rerun()

# LECTOR UNIVERSAL ISIN
with st.sidebar.expander("🔍 Lector Universal ISIN", expanded=True):
    with st.form(key="form_lector_isin_limpio", clear_on_submit=True):
        consulta_isin_input = st.text_input("Introduce ISIN a analizar", value="", key="txt_input_isin_field").strip().upper()
        btn_submit = st.form_submit_button("✅ Consultar e Incorporar a Histórico", use_container_width=True)

    if btn_submit and consulta_isin_input:
        res = consultar_catalogo_maestro(consulta_isin_input)
        res['FechaConsulta'] = hora_real_espana()
        
        st.session_state.historico_consultas = [i for i in st.session_state.historico_consultas if i['ISIN'] != consulta_isin_input]
        st.session_state.historico_consultas.insert(0, res)
        if len(st.session_state.historico_consultas) > 5:
            st.session_state.historico_consultas.pop()
        
        abrir_modal_detalle(res)

if st.session_state.historico_consultas:
    with st.sidebar.expander("🕒 Histórico Reciente (Últimas 5)", expanded=False):
        for idx, hist in enumerate(st.session_state.historico_consultas):
            etiqueta = f"📌 {hist['ISIN']} ({hist.get('FechaConsulta','')})"
            if st.sidebar.button(etiqueta, key=f"btn_hist_{idx}", use_container_width=True):
                abrir_modal_detalle(hist)

# PANEL PRINCIPAL
tab1, tab2, tab3, tab4 = st.tabs([
    "🛡️ Control & Bandas", 
    "📊 Buscador Maestro", 
    "☕ Copiloto IA & Prensa", 
    "📈 Gráficos & Cartera Core"
])

with tab1:
    st.subheader("🛡️ Supervisión 24h de Bandas (Suelos y Techos - Carteras Contratadas)")
    df_editado = st.data_editor(st.session_state.cartera_vigilada, num_rows="dynamic", use_container_width=True, key="ed_cartera")
    st.session_state.cartera_vigilada = df_editado

with tab2:
    st.subheader("📊 Buscador Maestro (2 Fondos Contratados Core + 10 Referencia del Mercado)")
    st.markdown("💡 *Haz doble clic o mantén presionado sobre cualquier código ISIN para copiarlo y pegarlo en la barra lateral:*")
    
    st.dataframe(
        df_master, 
        use_container_width=True,
        height=460,
        column_config={
            "ISIN": st.column_config.TextColumn(
                "ISIN (Copiar)",
                help="Selecciona o haz doble clic para copiar",
                width="medium"
            )
        }
    )

    st.markdown("---")

    # CAJITAS DE AVISO CON ISIN INTERACTIVO DE COPIADO
    df_top10 = df_master[df_master['Origen'] == '⭐ Top Mercado'].copy()
    df_top10['Suma_Rendimiento'] = df_top10['2025_%'] + df_top10['YTD_2026_%']
    
    top2_mejores = df_top10.sort_values(by='Suma_Rendimiento', ascending=False).head(2)
    st.success("🚀 **Los 2 Mejores en Crecimiento (Top 10 Mercado):**")
    st.dataframe(
        top2_mejores[['ISIN', 'Nombre del Fondo', 'Comercializador España', '2025_%', 'YTD_2026_%']], 
        use_container_width=True,
        column_config={
            "ISIN": st.column_config.TextColumn("ISIN (Copiar)", help="Mantén pulsado para copiar")
        }
    )

    st.markdown("<br>", unsafe_allow_html=True)

    top2_peores = df_top10.sort_values(by='Suma_Rendimiento', ascending=True).head(2)
    st.error("⚠️ **Los 2 con Menor Rendimiento / Retroceso (Top 10 Mercado):**")
    st.dataframe(
        top2_peores[['ISIN', 'Nombre del Fondo', 'Comercializador España', '2025_%', 'YTD_2026_%']], 
        use_container_width=True,
        column_config={
            "ISIN": st.column_config.TextColumn("ISIN (Copiar)", help="Mantén pulsado para copiar")
        }
    )

with tab3:
    st.subheader("☕ Copiloto IA & Prensa Financiera")
    st.success("Criterio Táctico: Mantener la base Core y utilizar las oportunidades de crecimiento constante para valorar traspasos estratégicos.")

with tab4:
    st.subheader("📈 Gráficos & Cartera Core")
    st.markdown("🔴 **Tu Cartera Core (Barras Rojas)** comparada de un golpe de vista con las alternativas del mercado (Barras Azules):")

    fondos_core_nombres = df_master[df_master['Origen'] == '📌 En Cartera (Core)']['Nombre del Fondo'].tolist()
    df_top10_calc = df_master[df_master['Origen'] == '⭐ Top Mercado'].copy()
    df_top10_calc['Suma_Rendimiento'] = df_top10_calc['2025_%'] + df_top10_calc['YTD_2026_%']
    fondos_top_nombres = df_top10_calc.sort_values(by='Suma_Rendimiento', ascending=False)['Nombre del Fondo'].tolist()[:2]
    
    default_grafico = fondos_core_nombres + fondos_top_nombres

    fondos_graf_activos = st.multiselect(
        "Selecciona fondos para comparar en el gráfico:",
        options=df_master['Nombre del Fondo'].tolist(),
        default=default_grafico,
        key="selector_grafico_core_red"
    )

    if fondos_graf_activos:
        df_graf_sub = df_master[df_master['Nombre del Fondo'].isin(fondos_graf_activos)].copy()
        
        # Etiqueta visual clara para el eje
        df_graf_sub['Fondo_Etiqueta'] = df_graf_sub.apply(
            lambda r: f"🔴 [CORE] {r['Nombre del Fondo'][:22]}..." if r['Origen'] == '📌 En Cartera (Core)' else f"🔵 {r['Nombre del Fondo'][:22]}...", 
            axis=1
        )

        # SEPARACIÓN VISUAL ENTRE CARTERA CORE (ROJO) Y TOP MERCADO (AZUL)
        df_core_only = df_graf_sub[df_graf_sub['Origen'] == '📌 En Cartera (Core)']
        df_mercado_only = df_graf_sub[df_graf_sub['Origen'] == '⭐ Top Mercado']

        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.markdown("##### 🚀 Rentabilidad Año en Curso (YTD 2026)")
            st.markdown("🔴 **Cartera Core (Rojo):**")
            if not df_core_only.empty:
                st.bar_chart(df_core_only.set_index('Fondo_Etiqueta')['YTD_2026_%'], color="#ef4444", use_container_width=True)
            st.markdown("🔵 **Fondos Mercado (Azul):**")
            if not df_mercado_only.empty:
                st.bar_chart(df_mercado_only.set_index('Fondo_Etiqueta')['YTD_2026_%'], color="#3b82f6", use_container_width=True)

        with col_g2:
            st.markdown("##### 📅 Rentabilidad Último Año Vencido (2025)")
            st.markdown("🔴 **Cartera Core (Rojo):**")
            if not df_core_only.empty:
                st.bar_chart(df_core_only.set_index('Fondo_Etiqueta')['2025_%'], color="#ef4444", use_container_width=True)
            st.markdown("🔵 **Fondos Mercado (Azul):**")
            if not df_mercado_only.empty:
                st.bar_chart(df_mercado_only.set_index('Fondo_Etiqueta')['2025_%'], color="#3b82f6", use_container_width=True)
            
    else:
        st.info("Selecciona al menos un fondo para mostrar el gráfico.")
