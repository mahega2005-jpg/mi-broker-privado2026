import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Mi Broker Privado", page_icon="🛡️", layout="centered")

# Estilos CSS (Estilo Gemini)
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

# BASE DE DATOS MAESTRA CENTRAL (FONDOS OPERABLES EN ESPAÑA - COMISIÓN BAJA & TRASPASABLES)
data_fondos = {
    'Nombre del Fondo': [
        'Vanguard Global Stock Index Inst Plus EUR Acc', 
        'Vanguard Global Bond Index Inst Plus EUR Hgd', 
        'Polar Capital Biotechnology EUR R Acc',
        'Polar Capital Biotechnology I EUR Dis',
        'Abante Global Funds Spanish Opportunities C EUR Cap',
        'Pictet - Security P EUR',
        'Amundi Index MSCI World AE-C',
        'Banco Tradicional Cartera Activa'
    ],
    'ISIN': [
        'IE00BFPM9N11', 'IE00BGCZOB53', 'IE00B43VBZ18', 'IE00B3WVRB16', 'LU1121307729', 'LU0503631872', 'LU1681048899', 'ES0111222333'
    ],
    'Tipo': [
        'Renta Variable Global', 'Renta Fija Global', 'Biotecnología', 'Biotecnología (Clase I)', 'Renta Variable España', 'Ciberseguridad', 'Indexado Global', 'Gestión Activa'
    ],
    'Operador / Comercializador España': [
        'Indexa Capital', 'Indexa Capital', 'MyInvestor / Renta 4', 'MyInvestor / Renta 4', 'Abante Asesores', 'MyInvestor / IronIA', 'MyInvestor / Openbank', 'Banco Tradicional'
    ],
    'Permite Transferencia/Traspaso': [
        'Sí (Exento peaje fiscal)', 'Sí (Exento peaje fiscal)', 'Sí (Traspasable)', 'Sí (Traspasable)', 'Sí (Traspasable)', 'Sí (Traspasable)', 'Sí (Traspasable)', 'Sí (Sujeto a comisiones)'
    ],
    'Min_Inversion': ['Desde 10€', 'Desde 10€', '1 Participación', '1 Participación', '1 Participación', '1 Participación', 'Desde 10€', 'Desde 500€'],
    'TER_%': [0.06, 0.10, 1.25, 1.00, 1.35, 1.00, 0.30, 1.85],       
    'YTD_2026_%': [18.55, -3.35, 11.50, 10.90, 8.20, 14.20, 7.90, 2.10],
    '2025_%': [6.73, 2.89, 14.00, 12.50, 9.10, 22.50, 19.20, 4.20],
    '2024_%': [26.59, 0.88, 8.50, 24.85, 11.40, 25.10, 21.90, 5.00],
    '2023_%': [19.63, 4.74, 6.20, 14.89, 14.20, 18.00, 14.80, 3.50],
    '2022_%': [-12.79, -15.03, -12.40, 11.97, -8.30, -20.10, -18.50, -8.50]
}
df_master = pd.DataFrame(data_fondos)

# ESTADOS DE SESIÓN
if 'historico_consultas' not in st.session_state:
    st.session_state.historico_consultas = []

if 'input_isin_key' not in st.session_state:
    st.session_state.input_isin_key = ""

if 'cartera_vigilada' not in st.session_state:
    st.session_state.cartera_vigilada = pd.DataFrame([
        {'ISIN': 'IE00BFPM9N11', 'Nombre': 'Vanguard Global Stock Index Inst Plus EUR Acc', 'Suelo_%': -10.0, 'Techo_%': 25.0, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': 4.5},
        {'ISIN': 'IE00BGCZOB53', 'Nombre': 'Vanguard Global Bond Index Inst Plus EUR Hgd', 'Suelo_%': -8.0, 'Techo_%': 15.0, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': -2.1}
    ])

if 'prueba_correo_enviada' not in st.session_state:
    st.session_state.prueba_correo_enviada = False

# CABECERA CON BOTÓN DE RECARGA
col_head1, col_head2 = st.columns([4, 1])

with col_head1:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #dbeafe, #bfdbfe); padding: 20px; border-radius: 12px; text-align: center; color: #1e3a8a; border: 2px solid #3b82f6;">
        <div style="font-size: 32px; margin-bottom: 3px;">🛡️📈</div>
        <h2 style="margin: 0; font-size: 22px; color: #1e40af;">MI BROKER PRIVADO</h2>
        <p style="margin: 4px 0 0 0; font-size: 12px; color: #1d4ed8;">Panel Táctico • Refresco 24h: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    </div>
    """, unsafe_allow_html=True)

with col_head2:
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Actualizar", use_container_width=True, help="Recargar aplicación"):
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# LÓGICA DE BÚSQUEDA BASADA EN EL CATÁLOGO MAESTRO CENTRAL
def consultar_catalogo_maestro(isin):
    isin = isin.strip().upper()
    match = df_master[df_master['ISIN'] == isin]
    
    if not match.empty:
        f = match.iloc[0]
        return {
            'Nombre': f['Nombre del Fondo'],
            'ISIN': f['ISIN'],
            'Tipo': f['Tipo'],
            'Operador': f['Operador / Comercializador España'],
            'Traspaso': f['Permite Transferencia/Traspaso'],
            'Minimo': f['Min_Inversion'],
            'TER': f"{f['TER_%']}%",
            'YTD': f"{f['YTD_2026_%']}%",
            '2025': f"{f['2025_%']}%",
            '2024': f"{f['2024_%']}%",
            '2023': f"{f['2023_%']}%",
            '2022': f"{f['2022_%']}%",
            'EnMaestro': True
        }
    
    return {
        'Nombre': f"Fondo No Registrado ({isin})",
        'ISIN': isin,
        'Tipo': 'Estudio Externe',
        'Operador': 'Consultar Comercializador España',
        'Traspaso': 'Verificar normativa',
        'Minimo': 'N/D',
        'TER': 'N/D', 'YTD': 'N/D', '2025': 'N/D', '2024': 'N/D', '2023': 'N/D', '2022': 'N/D',
        'EnMaestro': False
    }

# MODAL DE FICHA TÉCNICA Y ANÁLISIS
@st.dialog("📋 Ficha Técnica & Análisis de Inversión")
def abrir_modal_detalle(info_reg):
    st.markdown(f"### 🎯 **{info_reg['Nombre']}**")
    st.text_input("📋 Código ISIN (Copiar)", value=info_reg['ISIN'], key=f"copy_modal_{info_reg['ISIN']}")
    st.markdown(f"📅 *Consultado el:* `{datetime.now().strftime('%d/%m/%Y %H:%M')}`")
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
            st.metric("Rentabilidad 2022", info_reg['2022'])

        st.markdown("---")
        st.markdown(f"* **Operador en España:** {info_reg['Operador']}")
        st.markdown(f"* **Traspasabilidad:** {info_reg['Traspaso']}")
        st.markdown(f"* **Mínimo Inversión:** {info_reg['Minimo']}")
    else:
        st.warning("⚠️ Este ISIN no está en tu Catálogo Maestro Central. Utiliza los portales de contraste para revisar sus condiciones de inversión:")

    st.markdown("### 🌐 Enlaces de Análisis y Estudio Directo")
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

# 1. Test Alertas
with st.sidebar.expander("🧪 Test de Alertas", expanded=False):
    if st.button("🚀 Comprobar Estado", use_container_width=True):
        st.session_state.prueba_correo_enviada = True
        st.rerun()

# 2. Gestión ISIN
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

# 3. LECTOR UNIVERSAL DE ISIN (CON BORRADOR DE CASILLA TRAS CONSULTAR)
with st.sidebar.expander("🔍 Lector Universal ISIN", expanded=True):
    consulta_isin = st.text_input("Introduce ISIN a analizar", value=st.session_state.input_isin_key, key="txt_input_isin").strip().upper()
    
    if st.button("✅ Consultar e Incorporar a Histórico", use_container_width=True):
        if consulta_isin:
            res = consultar_catalogo_maestro(consulta_isin)
            res['FechaConsulta'] = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            # Guardar en histórico (máximo 5)
            st.session_state.historico_consultas = [i for i in st.session_state.historico_consultas if i['ISIN'] != consulta_isin]
            st.session_state.historico_consultas.insert(0, res)
            if len(st.session_state.historico_consultas) > 5:
                st.session_state.historico_consultas.pop()
            
            # Limpiar la casilla para la próxima consulta
            st.session_state.input_isin_key = ""
            
            abrir_modal_detalle(res)

# 4. HISTÓRICO DE ÚLTIMAS 5 CONSULTAS CON FECHA Y HORA
if st.session_state.historico_consultas:
    with st.sidebar.expander("🕒 Histórico Reciente (Últimas 5)", expanded=False):
        for idx, hist in enumerate(st.session_state.historico_consultas):
            etiqueta = f"📌 {hist['ISIN']} ({hist.get('FechaConsulta','')})"
            if st.sidebar.button(etiqueta, key=f"hist_{idx}", use_container_width=True):
                abrir_modal_detalle(hist)

# PANEL PRINCIPAL
tab1, tab2, tab3, tab4 = st.tabs(["🛡️ Control & Bandas", "📊 Buscador Maestro", "🤖 Copiloto IA & Prensa", "📈 Gráficos & Cartera Indexa"])

with tab1:
    st.subheader("🛡️ Supervisión 24h de Bandas (Suelos y Techos)")
    df_editado = st.data_editor(st.session_state.cartera_vigilada, num_rows="dynamic", use_container_width=True, key="ed_cartera")
    st.session_state.cartera_vigilada = df_editado

with tab2:
    st.subheader("📊 Buscador y Listado Maestro de Fondos Operables en España")
    st.markdown("💡 *Filtro de operabilidad: Bajas comisiones (TER), traspasables y accesibles desde España:*")
    st.dataframe(df_master, use_container_width=True)

with tab3:
    st.subheader("🤖 Copiloto IA")
    st.success("Criterio: Priorizar fondos indexados con TER ≤ 0.30% y traspasabilidad sin peaje fiscal.")

with tab4:
    st.subheader("📈 Gráficos")
    st.line_chart(df_master[['2021_%', '2022_%', '2023_%', '2024_%', '2025_%', 'YTD_2026_%']].T)
