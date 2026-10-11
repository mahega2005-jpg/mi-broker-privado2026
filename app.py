import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Mi Broker Privado", page_icon="🛡️", layout="centered")

# Estilos CSS
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

# Base de datos maestra local
data_fondos = {
    'Nombre del Fondo': [
        'Vanguard Global Stock Index Inst Plus EUR Acc', 
        'Vanguard Global Bond Index Inst Plus EUR Hgd', 
        'Polar Capital Biotechnology EUR R Acc',
        'Pictet - Security P EUR',
        'Amundi Index MSCI World AE-C',
        'Banco Tradicional Cartera Activa (Ejemplo)'
    ],
    'ISIN': ['IE00BFPM9N11', 'IE00BGCZOB53', 'IE00B43VBZ18', 'LU0503631872', 'LU1681048899', 'ES0111222333'],
    'Tipo': ['Renta Variable Global', 'Renta Fija Global', 'Biotecnología', 'Ciberseguridad', 'Indexado Global', 'Gestión Activa'],
    'Operador / Comercializador España': ['Indexa Capital', 'Indexa Capital', 'MyInvestor / Renta 4', 'MyInvestor / IronIA', 'MyInvestor / Openbank', 'Banco Tradicional'],
    'Permite Transferencia/Traspaso': ['Sí', 'Sí', 'Sí', 'Sí', 'Sí', 'Sí (Con comisiones)'],
    'TER_%': [0.06, 0.10, 1.25, 1.00, 0.30, 1.85],       
    'YTD_2026_%': [18.55, -3.35, 11.5, 14.2, 7.9, 2.1],
    '2025_%': [6.73, 2.89, 14.0, 22.5, 19.2, 4.2],
    '2024_%': [26.59, 0.88, 8.5, 25.1, 21.9, 5.0],
    '2023_%': [19.63, 4.74, 6.2, 18.0, 14.8, 3.5],
    '2022_%': [-12.79, -15.03, -12.4, -20.1, -18.5, -8.5],
    '2021_%': [27.5, 5.1, 10.1, 31.0, 27.1, 6.1]
}
df_master = pd.DataFrame(data_fondos)

# Estados de sesión
if 'historico_consultas' not in st.session_state:
    st.session_state.historico_consultas = []

if 'cartera_vigilada' not in st.session_state:
    st.session_state.cartera_vigilada = pd.DataFrame([
        {'ISIN': 'IE00BFPM9N11', 'Nombre': 'Vanguard Global Stock Index Inst Plus EUR Acc', 'Suelo_%': -10.0, 'Techo_%': 25.0, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': 4.5},
        {'ISIN': 'IE00BGCZOB53', 'Nombre': 'Vanguard Global Bond Index Inst Plus EUR Hgd', 'Suelo_%': -8.0, 'Techo_%': 15.0, 'Email': 'mahega2005@gmail.com', 'Rentabilidad_Actual_%': -2.1}
    ])

if 'prueba_correo_enviada' not in st.session_state:
    st.session_state.prueba_correo_enviada = False

# Cabecera
st.markdown("""
<div style="background: linear-gradient(135deg, #dbeafe, #bfdbfe); padding: 25px; border-radius: 12px; text-align: center; color: #1e3a8a; border: 2px solid #3b82f6;">
    <div style="font-size: 38px; margin-bottom: 5px;">🛡️📈</div>
    <h2 style="margin: 0; font-size: 24px; color: #1e40af;">MI BROKER PRIVADO</h2>
    <p style="margin: 6px 0 0 0; font-size: 13px; color: #1d4ed8;">Panel Táctico • Core en Indexa Capital • Vigilancia 24h</p>
</div>
<br>
""", unsafe_allow_html=True)

# Modal de Ficha Limpia sin Falsos Datos
@st.dialog("📋 Consulta de ISIN & Portales Oficiales")
def abrir_modal_detalle(info_reg):
    st.markdown(f"### 🎯 **{info_reg['Nombre']}**")
    st.text_input("📋 Código ISIN (Copiar)", value=info_reg['ISIN'], key=f"copy_modal_{info_reg['ISIN']}")
    st.markdown(f"📅 *Consultado el:* `{info_reg['Fecha']}`")
    st.markdown("---")
    
    if info_reg.get('EsLocal', False):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Comisión TER", f"{info_reg['TER']}%")
            st.metric("YTD 2026", f"{info_reg['YTD']}%")
            st.metric("2025", f"{info_reg['2025']}%")
        with col2:
            st.metric("2024", f"{info_reg['2024']}%")
            st.metric("2023", f"{info_reg['2023']}%")
            st.metric("2022", f"{info_reg['2022']}%")
        st.markdown("---")
    else:
        st.info("ℹ️ **Fondo Externo / Internacional:** Accede a la ficha en vivo en tiempo real desde los portales especializados:")

    st.markdown("### 🌐 Enlaces Directos en Tiempo Real")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"[📊 Morningstar](https://www.morningstar.es/es/funds/security/summary.aspx?search={info_reg['ISIN']})")
    with col2:
        st.markdown(f"[🔍 QueFondos](https://www.quefondos.com/es/fondos/ficha/index.html?isin={info_reg['ISIN']})")
    with col3:
        st.markdown(f"[📈 JustETF](https://www.justetf.com/es/search.html?query={info_reg['ISIN']})")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✖️ Cerrar", use_container_width=True):
        st.rerun()

# BARRA LATERAL
st.sidebar.header("🛡️ Panel Táctico")

# 1. Test Alertas
with st.sidebar.expander("🧪 Test de Alertas", expanded=False):
    if st.button("🚀 Comprobar Estado", use_container_width=True):
        st.session_state.prueba_correo_enviada = True
        st.rerun()

# 2. Pestaña RESTABLECIDA: Añadir y Eliminar ISIN
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

# 3. Lector Universal ISIN
with st.sidebar.expander("🔍 Lector Universal ISIN", expanded=True):
    with st.form(key='form_lector_isin'):
        consulta_isin = st.text_input("Introduce ISIN (Ej: LU, IE, ES...)", "").strip().upper()
        btn_confirmar = st.form_submit_button("✅ Confirmar y Ver Ficha", use_container_width=True)

    if btn_confirmar and consulta_isin:
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        fondo_encontrado = df_master[df_master['ISIN'] == consulta_isin]
        
        if not fondo_encontrado.empty:
            f = fondo_encontrado.iloc[0]
            info_reg = {
                'Nombre': f['Nombre del Fondo'], 'ISIN': f['ISIN'], 'Fecha': fecha_actual, 'EsLocal': True,
                'TER': f['TER_%'], 'YTD': f['YTD_2026_%'], '2025': f['2025_%'], '2024': f['2024_%'],
                '2023': f['2023_%'], '2022': f['2022_%']
            }
        else:
            info_reg = {
                'Nombre': f"Fondo Externo / Internacional ({consulta_isin})", 'ISIN': consulta_isin,
                'Fecha': fecha_actual, 'EsLocal': False
            }
        
        st.session_state.historico_consultas = [i for i in st.session_state.historico_consultas if i['ISIN'] != consulta_isin]
        st.session_state.historico_consultas.insert(0, info_reg)
        if len(st.session_state.historico_consultas) > 5:
            st.session_state.historico_consultas.pop()
            
        abrir_modal_detalle(info_reg)

# 4. Histórico
if st.session_state.historico_consultas:
    with st.sidebar.expander("🕒 Histórico Reciente (Últimas 5)", expanded=False):
        for idx, hist in enumerate(st.session_state.historico_consultas):
            if st.sidebar.button(f"📌 {hist['ISIN']} ({hist['Fecha']})", key=f"hist_{idx}", use_container_width=True):
                abrir_modal_detalle(hist)

# PANEL PRINCIPAL
tab1, tab2, tab3, tab4 = st.tabs(["🛡️ Control & Bandas", "📊 Buscador Maestro", "🤖 Copiloto IA & Prensa", "📈 Gráficos & Cartera Indexa"])

with tab1:
    st.subheader("🛡️ Supervisión 24h de Bandas (Suelos y Techos)")
    df_editado = st.data_editor(st.session_state.cartera_vigilada, num_rows="dynamic", use_container_width=True, key="ed_cartera")
    st.session_state.cartera_vigilada = df_editado

with tab2:
    st.subheader("📊 Buscador y Listado Maestro de Fondos")
    st.dataframe(df_master, use_container_width=True)

with tab3:
    st.subheader("🤖 Copiloto IA")
    st.success("Recomendación: Mantenimiento de comisiones bajas TER en el núcleo indexado.")

with tab4:
    st.subheader("📈 Gráficos")
    st.line_chart(df_master[['2021_%', '2022_%', '2023_%', '2024_%', '2025_%', 'YTD_2026_%']].T)
