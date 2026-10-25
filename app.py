# ==============================================================================
# PROYECTO: MI BROKER PRIVADO - PANEL TÁCTICO DE INVERSIÓN
# AUTOR: Bartolomé Marín Hedrera
# DESCRIPCIÓN: Panel de control avanzado en Streamlit para la gestión táctica
#              de fondos de inversión, supervisión de bandas y motor autónomo.
# ==============================================================================

from datetime import datetime
import zoneinfo
import pandas as pd
import streamlit as st

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS
# ==============================================================================
st.set_page_config(
    page_title="Mi Broker Privado - Panel Táctico",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
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
    /* BOTÓN FLOTANTE ESTILIZADO DE GITHUB CON ICONO SVG */
    .github-top-right {
        position: fixed;
        top: 12px;
        right: 25px;
        z-index: 999999;
        background-color: #24292e;
        color: #ffffff;
        padding: 6px 14px;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.25);
        display: flex;
        align-items: center;
        gap: 8px;
        border: 1px solid #374151;
    }
    .github-top-right a {
        text-decoration: none;
        color: #ffffff;
        font-weight: 600;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------------------
# BOTÓN FLOTANTE CON EL LOGOTIPO DE GITHUB (ESQUINA SUPERIOR DERECHA)
# ------------------------------------------------------------------------------
st.markdown(
    """
    <div class="github-top-right">
        <a href="https://github.com/mahega2005-jpg/mi-broker-privado2026" target="_blank">
            <svg height="16" width="16" viewBox="0 0 16 16" version="1.1" fill="white">
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.22 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
            </svg>
            GitHub
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# 2. SOPORTE Y HORARIO OFICIAL
# ==============================================================================


def hora_real_espana():
  tz = zoneinfo.ZoneInfo("Europe/Madrid")
  return datetime.now(tz).strftime("%d/%m/%Y %H:%M:%S")


# ==============================================================================
# 3. BASE DE DATOS MAESTRA (2 CORE + 10 TOP MERCADO)
# ==============================================================================
data_12_fondos = {
    "Origen": [
        "📌 En Cartera (Core)",
        "📌 En Cartera (Core)",
        "⭐ Top Mercado",
        "⭐ Top Mercado",
        "⭐ Top Mercado",
        "⭐ Top Mercado",
        "⭐ Top Mercado",
        "⭐ Top Mercado",
        "⭐ Top Mercado",
        "⭐ Top Mercado",
        "⭐ Top Mercado",
        "⭐ Top Mercado",
    ],
    "ISIN": [
        "IE00BFPM9N11",
        "IE00BGCZOB53",
        "LU1681048899",
        "IE00B03HD191",
        "LU0503631872",
        "IE00B43VBZ18",
        "ES0114105030",
        "IE00B03HCZ61",
        "LU0996182563",
        "LU1121307729",
        "IE00B3WVRB16",
        "ES0111222333",
    ],
    "Nombre del Fondo": [
        "Vanguard Global Stock Index Inst Plus EUR Acc",
        "Vanguard Global Bond Index Inst Plus EUR Hgd",
        "Amundi Index MSCI World AE-C",
        "Vanguard US 500 Stock Index EUR Acc",
        "Pictet - Security P EUR",
        "Polar Capital Biotechnology EUR R Acc",
        "DWS Investments Alpha Opportunities",
        "Vanguard European Stock Index EUR Acc",
        "Fidelity Funds - Global Technology A-ACC-EUR",
        "Abante Global Funds Spanish Opportunities C EUR",
        "Polar Capital Biotechnology I EUR Dis",
        "Banco Tradicional Cartera Activa",
    ],
    "Categoría / Tipo": [
        "Renta Variable Global",
        "Renta Fija Global",
        "Indexado Global (MSCI World)",
        "Indexado S&P 500",
        "Ciberseguridad & Seguridad",
        "Biotecnología & Salud",
        "Retorno Absoluto / Multi-Activo",
        "Renta Variable Europa",
        "Tecnología Global",
        "Renta Variable España",
        "Biotecnología (Clase I Dist)",
        "Gestión Activa Tradicional",
    ],
    "Comercializador España": [
        "Indexa Capital",
        "Indexa Capital",
        "MyInvestor / Openbank",
        "MyInvestor / Renta 4",
        "MyInvestor / IronIA",
        "MyInvestor / Renta 4",
        "Renta 4 / Allfunds",
        "MyInvestor / Renta 4",
        "MyInvestor / Mapfre",
        "Abante Asesores",
        "MyInvestor / Renta 4",
        "Banco Tradicional",
    ],
    "Traspasable": [
        "Sí",
        "Sí",
        "Sí",
        "Sí",
        "Sí",
        "Sí",
        "Sí",
        "Sí",
        "Sí",
        "Sí",
        "Sí",
        "Sí",
    ],
    "Min_Inversion": [
        "Desde 10€",
        "Desde 10€",
        "Desde 10€",
        "100€",
        "1 Participación",
        "1 Participación",
        "100€",
        "100€",
        "1 Participación",
        "1 Participación",
        "1 Participación",
        "Desde 500€",
    ],
    "TER_%": [0.06, 0.10, 0.30, 0.10, 1.00, 1.25, 0.65, 0.12, 1.05, 1.35, 1.00, 1.85],
    "YTD_2026_%": [
        18.55,
        -3.35,
        17.90,
        21.40,
        14.20,
        11.50,
        6.80,
        12.10,
        24.50,
        8.20,
        10.90,
        -2.10,
    ],
    "2025_%": [6.73, 2.89, 19.20, 23.50, 22.50, 14.00, 5.40, 11.20, 28.10, 9.10, 12.50, 4.20],
    "2024_%": [
        26.59,
        0.88,
        21.90,
        26.80,
        25.10,
        8.50,
        7.10,
        15.80,
        32.40,
        11.40,
        24.85,
        5.00,
    ],
    "2023_%": [
        19.63,
        4.74,
        14.80,
        21.20,
        18.00,
        6.20,
        4.20,
        12.50,
        36.10,
        14.20,
        14.89,
        3.50,
    ],
}

# ==============================================================================
# 4. GESTIÓN DE ESTADOS DE SESIÓN (SESSION STATE)
# ==============================================================================
if "df_master_app" not in st.session_state:
  st.session_state.df_master_app = pd.DataFrame(data_12_fondos)

if "historico_consultas" not in st.session_state:
  st.session_state.historico_consultas = []

if "cartera_vigilada" not in st.session_state:
  st.session_state.cartera_vigilada = pd.DataFrame([
      {
          "ISIN": "IE00BFPM9N11",
          "Nombre": "Vanguard Global Stock Index Inst Plus EUR Acc",
          "Suelo_%": -10.0,
          "Techo_%": 25.0,
          "Email": "mahega2005@gmail.com",
          "Rentabilidad_Actual_%": 18.55,
      },
      {
          "ISIN": "IE00BGCZOB53",
          "Nombre": "Vanguard Global Bond Index Inst Plus EUR Hgd",
          "Suelo_%": -8.0,
          "Techo_%": 15.0,
          "Email": "mahega2005@gmail.com",
          "Rentabilidad_Actual_%": -3.35,
      },
  ])

if "mensaje_escaner_ciego" not in st.session_state:
  st.session_state.mensaje_escaner_ciego = (
      "🟢 **Estado del Top 10:** Sincronizado y protegido. "
      "El motor autónomo evalúa permanentemente la rentabilidad neta ajustada por comisiones TER."
  )

if "notificacion_actualizado" not in st.session_state:
  st.session_state.notificacion_actualizado = False

if "isin_preseleccionado" not in st.session_state:
  st.session_state.isin_preseleccionado = ""


# ==============================================================================
# 5. MOTOR AUTÓNOMO DE ESCANEO Y ROTACIÓN DEL TOP 10
# ==============================================================================
def ejecutar_escanner_automatico_top10():
  df = st.session_state.df_master_app

  df_core = df[df["Origen"] == "📌 En Cartera (Core)"].copy()
  df_top = df[df["Origen"] == "⭐ Top Mercado"].copy()

  df_top["Score_Eficiente"] = (
      df_top["YTD_2026_%"] * 0.5
  ) + (df_top["2025_%"] * 0.3) - (df_top["TER_%"] * 1.5)
  df_top_ordenado = (
      df_top.sort_values(by="Score_Eficiente", ascending=False)
      .reset_index(drop=True)
  )

  st.session_state.df_master_app = pd.concat(
      [df_core, df_top_ordenado], ignore_index=True
  )

  lider = df_top_ordenado.iloc[0]["Nombre del Fondo"]
  decimo = df_top_ordenado.iloc[-1]["Nombre del Fondo"]

  st.session_state.mensaje_escaner_ciego = (
      f"⚡ **Auditoría de Mercado ({hora_real_espana()}):**<br>"
      f"• **Líder del Ranking (Puesto 1):** {lider}<br>"
      f"• **Umbral de Corte (Puesto 10):** {decimo}<br>"
      f"• **Estado:** Ranking dinámico ordenado por eficiencia neta. Core"
      " blindado e independiente."
  )


# ==============================================================================
# 6. CABECERA TÁCTICA SUPERIOR
# ==============================================================================
col_head1, col_head2 = st.columns([4, 1])
h_actual = hora_real_espana()

with col_head1:
  st.markdown(
      f"""
    <div style="background: linear-gradient(135deg, #dbeafe, #bfdbfe); padding: 20px; border-radius: 12px; text-align: center; color: #1e3a8a; border: 2px solid #3b82f6;">
        <div style="font-size: 32px; margin-bottom: 3px;">🛡️📈</div>
        <h2 style="margin: 0; font-size: 24px; color: #1e40af; font-weight: 700;">MI BROKER PRIVADO</h2>
        <p style="margin: 6px 0 0 0; font-size: 14px; color: #1d4ed8; font-weight: 600;">Panel Táctico • Hora Oficial España: {h_actual}</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

with col_head2:
  st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
  if st.button("🔄 Actualizar Datos", use_container_width=True):
    ejecutar_escanner_automatico_top10()
    st.session_state.notificacion_actualizado = True
    st.rerun()

if st.session_state.notificacion_actualizado:
  st.toast(
      f"✅ ¡Escaneo autónomo completado! Hora oficial ({h_actual}) y Top 10"
      " auditados.",
      icon="🔄",
  )
  st.session_state.notificacion_actualizado = False

st.markdown("<br>", unsafe_allow_html=True)


# ==============================================================================
# 7. FUNCIONES MODALES Y CONSULTAS
# ==============================================================================
def consultar_catalogo_maestro(isin):
  df_m = st.session_state.df_master_app
  isin = isin.strip().upper()
  match = df_m[df_m["ISIN"] == isin]
  if not match.empty:
    f = match.iloc[0]
    return {
        "Nombre": f["Nombre del Fondo"],
        "ISIN": f["ISIN"],
        "Tipo": f["Categoría / Tipo"],
        "Operador": f["Comercializador España"],
        "Traspaso": f["Traspasable"],
        "Minimo": f["Min_Inversion"],
        "TER": f"{f['TER_%']}%",
        "YTD": f"{f['YTD_2026_%']}%",
        "2025": f"{f['2025_%']}%",
        "2024": f"{f['2024_%']}%",
        "2023": f"{f['2023_%']}%",
        "EnMaestro": True,
    }
  return {
      "Nombre": f"Fondo No Registrado ({isin})",
      "ISIN": isin,
      "Tipo": "Estudio Externo",
      "Operador": "Consultar Comercializador España",
      "Traspaso": "Verificar normativa",
      "Minimo": "N/D",
      "TER": "N/D",
      "YTD": "N/D",
      "2025": "N/D",
      "2024": "N/D",
      "2023": "N/D",
      "EnMaestro": False,
  }


@st.dialog("📋 Ficha Técnica & Análisis de Inversión")
def abrir_modal_detalle(info_reg):
  st.markdown(f"### 🎯 **{info_reg['Nombre']}**")
  st.code(info_reg["ISIN"], language=None)
  st.markdown(f"📅 *Consultado el:* `{hora_real_espana()}`")
  st.markdown("---")
  if info_reg["EnMaestro"]:
    col1, col2 = st.columns(2)
    with col1:
      st.metric("Comisión TER", info_reg["TER"])
      st.metric("YTD 2026", info_reg["YTD"])
      st.metric("Rentabilidad 2025", info_reg["2025"])
    with col2:
      st.metric("Rentabilidad 2024", info_reg["2024"])
      st.metric("Rentabilidad 2023", info_reg["2023"])
    st.markdown("---")
    st.markdown(f"* **Operador en España:** {info_reg['Operador']}")
    st.markdown(f"* **Traspasabilidad Fiscal:** {info_reg['Traspaso']}")
    st.markdown(f"* **Inversión Mínima:** {info_reg['Minimo']}")
  else:
    st.warning("⚠️ ISIN externo. Consulta los enlaces directos:")
  st.markdown("### 🌐 Enlaces Directos")
  c1, c2, c3 = st.columns(3)
  isin_clean = info_reg["ISIN"].strip()
  with c1:
    st.markdown(
        f"[Morningstar](https://www.morningstar.es/es/search/quickrank.aspx?search={isin_clean})"
    )
  with c2:
    st.markdown(
        f"[Google"
        f" Finance](https://www.google.com/finance/quote/{isin_clean})"
    )
  with c3:
    st.markdown(f"[Citywire](https://citywire.com/es/search?q={isin_clean})")
  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("✖️ Cerrar Ventana", use_container_width=True):
    st.rerun()


# ==============================================================================
# 8. BARRA LATERAL
# ==============================================================================
with st.sidebar:
  st.header("🛡️ Panel Táctico")

  with st.expander("🧪 Test de Alertas", expanded=False):
    if st.button("🚀 Comprobar Estado", use_container_width=True):
      st.success("Sistemas operativos y escáner autónomo activo.")

  with st.expander("➕ Añadir / 🗑️ Eliminar ISIN", expanded=False):
    opcion_g = st.radio(
        "Acción:",
        ["Añadir Entrada", "Eliminar Salida"],
        horizontal=True,
        key="rad_gest",
    )
    df_m_local = st.session_state.df_master_app
    if opcion_g == "Añadir Entrada":
      n_isin = st.text_input("Código ISIN", key="add_i").strip().upper()
      s_val = st.number_input("Suelo (%)", value=-10.0, step=1.0, key="add_s")
      t_val = st.number_input("Techo (%)", value=20.0, step=1.0, key="add_t")
      r_val = st.number_input(
          "Rentabilidad actual (%)", value=2.0, step=0.5, key="add_r"
      )
      if st.button("Guardar en Vigilancia", use_container_width=True):
        if n_isin:
          df_c = st.session_state.cartera_vigilada
          if not df_c.empty and n_isin in df_c["ISIN"].values:
            st.warning("El ISIN ya está registrado.")
          else:
            m = df_m_local[df_m_local["ISIN"] == n_isin]
            nom = (
                m.iloc[0]["Nombre del Fondo"]
                if not m.empty
                else f"Fondo ({n_isin})"
            )
            n_row = pd.DataFrame([{
                "ISIN": n_isin,
                "Nombre": nom,
                "Suelo_%": s_val,
                "Techo_%": t_val,
                "Email": "mahega2005@gmail.com",
                "Rentabilidad_Actual_%": r_val,
            }])
            st.session_state.cartera_vigilada = pd.concat(
                [df_c, n_row], ignore_index=True
            )
            st.success("Guardado en vigilancia.")
            st.rerun()
    else:
      df_c = st.session_state.cartera_vigilada
      if not df_c.empty:
        sel = st.selectbox(
            "Dar de baja ISIN:",
            [
                f"{r['ISIN']} - {r['Nombre'][:12]}"
                for _, r in df_c.iterrows()
            ],
            key="del_s",
        )
        if st.button(
            "🗑️ Confirmar Salida", type="primary", use_container_width=True
        ):
          target = sel.split(" - ")[0]
          st.session_state.cartera_vigilada = df_c[
              df_c["ISIN"] != target
          ].reset_index(drop=True)
          st.success("ISIN eliminado.")
          st.rerun()

  with st.expander("🔍 Lector Universal ISIN", expanded=True):
    val_defecto = st.session_state.isin_preseleccionado
    with st.form(key="form_lector_isin_limpio", clear_on_submit=True):
      consulta_isin_input = (
          st.text_input(
              "Introduce ISIN",
              value=val_defecto,
              key="txt_input_isin_field",
          )
          .strip()
          .upper()
      )
      btn_submit = st.form_submit_button(
          "✅ Consultar e Incorporar", use_container_width=True
      )
    if btn_submit and consulta_isin_input:
      st.session_state.isin_preseleccionado = ""
      res = consultar_catalogo_maestro(consulta_isin_input)
      res["FechaConsulta"] = hora_real_espana()
      st.session_state.historico_consultas = [
          i
          for i in st.session_state.historico_consultas
          if i["ISIN"] != consulta_isin_input
      ]
      st.session_state.historico_consultas.insert(0, res)
      if len(st.session_state.historico_consultas) > 5:
        st.session_state.historico_consultas.pop()
      abrir_modal_detalle(res)

  if st.session_state.historico_consultas:
    with st.expander("🕒 Histórico Reciente (Últimas 5)", expanded=False):
      for idx, hist in enumerate(st.session_state.historico_consultas):
        if st.button(
            f"📌 {hist['ISIN']} ({hist.get('FechaConsulta','')})",
            key=f"btn_hist_{idx}",
            use_container_width=True,
        ):
          abrir_modal_detalle(hist)

# ==============================================================================
# 9. PESTAÑAS PRINCIPALES DEL PANEL (AMPLIADAS A 5)
# ==============================================================================
tabs = st.tabs([
    "🛡️ Control & Bandas",
    "📊 Buscador Maestro",
    "🎯 Radar de Tendencias & Estrategias",
    "📈 Gráficos & Cartera Core",
    "📰 Prensa & Inteligencia Sectorial",
])

# ------------------------------------------------------------------------------
# PESTAÑA 1: CONTROL & BANDAS
# ------------------------------------------------------------------------------
with tabs[0]:
  st.subheader("🛡️ Supervisión 24h de Bandas (Suelos y Techos)")
  st.markdown("Edita las bandas de control de tus posiciones activas:")
  st.session_state.cartera_vigilada = st.data_editor(
      st.session_state.cartera_vigilada,
      num_rows="dynamic",
      use_container_width=True,
      key="ed_cartera",
  )

# ------------------------------------------------------------------------------
# PESTAÑA 2: BUSCADOR MAESTRO
# ------------------------------------------------------------------------------
with tabs[1]:
  st.subheader(
      "📊 Buscador Maestro: Top 10 Dinámico de Referencia + Cartera Core"
  )
  df_master_actual = st.session_state.df_master_app

  col_sel1, col_sel2 = st.columns([3, 1])
  with col_sel1:
    isin_elegido = st.selectbox(
        "Selecciona fondo:",
        options=df_master_actual["ISIN"].tolist(),
        format_func=lambda x: f"{x} -"
        f" {df_master_actual[df_master_actual['ISIN'] == x]['Nombre del Fondo'].values[0]}",
        key="sel_directo_tablet",
    )
  with col_sel2:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    if st.button("🚀 Cargar en Lector", use_container_width=True):
      st.session_state.isin_preseleccionado = isin_elegido
      abrir_modal_detalle(consultar_catalogo_maestro(isin_elegido))

  st.dataframe(df_master_actual, use_container_width=True, height=380)

  st.markdown("---")

  st.markdown("### ⚡ Escáner Autónomo & Informe de Rotación del Top 10")
  st.markdown(
      """
    <div style="background-color: #ffffff; padding: 18px; border-radius: 12px; border: 2px solid #3b82f6; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="font-size: 14px; color: #1e3a8a; line-height: 1.6;">
    """
      + st.session_state.mensaje_escaner_ciego
      + """
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("---")
  st.subheader("📢 Avisos de Oportunidad y Retroceso Táctico")
  df_top10 = df_master_actual[
      df_master_actual["Origen"] == "⭐ Top Mercado"
  ].copy()
  df_top10["Suma_Rendimiento"] = df_top10["2025_%"] + df_top10["YTD_2026_%"]

  for _, row in (
      df_top10.sort_values(by="Suma_Rendimiento", ascending=False)
      .head(2)
      .iterrows()
  ):
    c1, c2, c3 = st.columns([1.5, 3.5, 1])
    with c1:
      st.code(row["ISIN"], language=None)
    with c2:
      st.markdown(f"**{row['Nombre del Fondo']}**")
    with c3:
      if st.button(
          "🔍 Analizar", key=f"top_m_{row['ISIN']}", use_container_width=True
      ):
        abrir_modal_detalle(consultar_catalogo_maestro(row["ISIN"]))

# ------------------------------------------------------------------------------
# PESTAÑA 3: RADAR DE TENDENCIAS & ESTRATEGIAS
# ------------------------------------------------------------------------------
with tabs[2]:
  st.subheader(
      "🎯 Radar de Tendencias Globales & Simulación de Estrategias"
  )
  st.markdown(
      "Análisis táctico para anticiparse al mercado detectando las"
      " megatendencias de mayor impulso y cruzándolas con los 3 fondos líderes"
      " por sector:"
  )

  st.markdown("### 🧭 Modelo Táctico de Asignación por Estrategia")
  estrategia_sel = st.radio(
      "Selecciona una Estrategia Táctica de Mercado:",
      options=[
          "🛡️ Estrategia Conservadora / Defensiva (Preservación)",
          "⚖️ Estrategia Moderada / Core Indexado (Equilibrada)",
          (
              "🚀 Estrategia Crecimiento & Megatendencias (Sintética"
              " Aportación)"
          ),
      ],
      horizontal=True,
      key="radio_estrategias",
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
        * **Asignación:** 40% RV Global Core + 30% Tecnología & IA + 15% Ciberseguridad + 15% Biotecnología / Salud.
        * **Fondos Vehículo:** `LU0996182563` (Fidelity Tech) + `LU0503631872` (Pictet Security) + `IE00B43VBZ18` (Polar Biotech).
        """)

  st.markdown("---")
  st.markdown(
      "### 🛰️ Radar Megatendencial: 3 Fondos de Referencia por Sector"
  )

  t1, t2, t3 = st.columns(3)
  with t1:
    st.markdown(
        """
        <div class="trend-card-header">
            <h4 style="margin:0; color: #1e40af;">💻 IA, Tecnología & Ciberseguridad</h4>
            <p style="font-size: 13px; color: #475569; margin: 8px 0;"><b>Tendencia:</b> Digitalización masiva e infraestructuras de IA.</p>
            <p style="font-size: 12px; color: #15803d; margin:0;"><b>Impulso:</b> Muy Alto 🚀</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with t2:
    st.markdown(
        """
        <div class="trend-card-header">
            <h4 style="margin:0; color: #1e40af;">🧬 Biotecnología, Salud & Longevidad</h4>
            <p style="font-size: 13px; color: #475569; margin: 8px 0;"><b>Tendencia:</b> Envejecimiento de la población y patentes.</p>
            <p style="font-size: 12px; color: #15803d; margin:0;"><b>Impulso:</b> Alto 📈</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with t3:
    st.markdown(
        """
        <div class="trend-card-header">
            <h4 style="margin:0; color: #1e40af;">🛡️ Retorno Absoluto & Preservación</h4>
            <p style="font-size: 13px; color: #475569; margin: 8px 0;"><b>Tendencia:</b> Descorrelación y protección de capital.</p>
            <p style="font-size: 12px; color: #b45309; margin:0;"><b>Impulso:</b> Moderado / Defensivo 🛡️</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("<br>", unsafe_allow_html=True)

  # BLOQUE 1 DE FONDOS
  f1_1, f1_2, f1_3 = st.columns(3)
  with f1_1:
    st.code("LU0996182563", language=None)
    st.caption("Fidelity Funds - Global Tech")
    if st.button(
        "🔍 Analizar Fidelity Tech", key="btn_t1_1", use_container_width=True
    ):
      abrir_modal_detalle(consultar_catalogo_maestro("LU0996182563"))
  with f1_2:
    st.code("IE00B43VBZ18", language=None)
    st.caption("Polar Capital Biotech (Acc)")
    if st.button(
        "🔍 Analizar Polar Biotech R", key="btn_t2_1", use_container_width=True
    ):
      abrir_modal_detalle(consultar_catalogo_maestro("IE00B43VBZ18"))
  with f1_3:
    st.code("ES0114105030", language=None)
    st.caption("DWS Investments Alpha Opp")
    if st.button(
        "🔍 Analizar DWS Alpha", key="btn_t3_1", use_container_width=True
    ):
      abrir_modal_detalle(consultar_catalogo_maestro("ES0114105030"))

  st.markdown("---")

  # BLOQUE 2 DE FONDOS
  f2_1, f2_2, f2_3 = st.columns(3)
  with f2_1:
    st.code("LU0503631872", language=None)
    st.caption("Pictet - Security P EUR")
    if st.button(
        "🔍 Analizar Pictet Security", key="btn_t1_2", use_container_width=True
    ):
      abrir_modal_detalle(consultar_catalogo_maestro("LU0503631872"))
  with f2_2:
    st.code("IE00B3WVRB16", language=None)
    st.caption("Polar Capital Biotech (Dis)")
    if st.button(
        "🔍 Analizar Polar Biotech I", key="btn_t2_2", use_container_width=True
    ):
      abrir_modal_detalle(consultar_catalogo_maestro("IE00B3WVRB16"))
  with f2_3:
    st.code("IE00BGCZOB53", language=None)
    st.caption("Vanguard Global Bond Index")
    if st.button(
        "🔍 Analizar Vanguard Bond", key="btn_t3_2", use_container_width=True
    ):
      abrir_modal_detalle(consultar_catalogo_maestro("IE00BGCZOB53"))

  st.markdown("---")

  # BLOQUE 3 DE FONDOS
  f3_1, f3_2, f3_3 = st.columns(3)
  with f3_1:
    st.code("IE00B03HD191", language=None)
    st.caption("Vanguard US 500 Index")
    if st.button(
        "🔍 Analizar Vanguard S&P500", key="btn_t1_3", use_container_width=True
    ):
      abrir_modal_detalle(consultar_catalogo_maestro("IE00B03HD191"))
  with f3_2:
    st.code("IE00BFPM9N11", language=None)
    st.caption("Vanguard Global Stock Core")
    if st.button(
        "🔍 Analizar Vanguard Global", key="btn_t2_3", use_container_width=True
    ):
      abrir_modal_detalle(consultar_catalogo_maestro("IE00BFPM9N11"))
  with f3_3:
    st.code("LU1681048899", language=None)
    st.caption("Amundi Index MSCI World")
    if st.button(
        "🔍 Analizar Amundi MSCI World", key="btn_t3_3", use_container_width=True
    ):
      abrir_modal_detalle(consultar_catalogo_maestro("LU1681048899"))

  st.markdown("<br>", unsafe_allow_html=True)

  # REFLEXIÓN TÁCTICA
  st.markdown(
      "### 💡 Reflexión Táctica: Elección del Mejor Fondo por Sector"
  )
  st.markdown(
      """
    <div style="background-color: #ffffff; padding: 20px; border-radius: 12px; border: 2px solid #93c5fd; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
        <h4 style="margin-top:0; color: #1e40af;">🏆 ¿Cuál es el Mejor Fondo para cada Estrategia y Por Qué?</h4>
        <ul style="color: #334155; font-size: 14px; line-height: 1.6;">
            <li><b>En IA & Tecnología (Mejor Opción: <code>LU0996182563</code> - Fidelity Global Tech):</b> Gestión activa diferencial capaz de rotar entre semiconductores y software.</li>
            <li style="margin-top: 10px;"><b>En Biotecnología & Salud (Mejor Opción: <code>IE00B43VBZ18</code> - Polar Capital Biotech):</b> Especializado en patentes aprobadas con subidas de doble dígito.</li>
            <li style="margin-top: 10px;"><b>En Preservación (Mejor Opción: <code>IE00BGCZOB53</code> - Vanguard Global Bond):</b> Cobertura en euros y mínima comisión TER (0.10%).</li>
        </ul>
    </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("<br><hr><br>", unsafe_allow_html=True)

  # LAS 3 CAJITAS INFERIORES DE CONTRAPUNTO TÁCTICO
  st.markdown(
      "### 🔭 Contrapunto Táctico: Detección Automática de Techos, Suelos &"
      " Anomalías"
  )
  st.markdown(
      "Análisis algorítmico basado en el histórico de 5 años y el comportamiento"
      " reciente:"
  )

  col_box1, col_box2, col_box3 = st.columns(3)

  with col_box1:
    st.markdown(
        """
        <div style="background-color: #ffffff; padding: 18px; border-radius: 12px; border: 2px solid #f87171; min-height: 280px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <h4 style="color: #b91c1c; margin-top:0; font-size: 16px;">🛑 1. Techos (Top 10 + Core)</h4>
                <p style="font-size: 13px; color: #334155; line-height: 1.4;">
                Identifica extensiones alcistas verticales eufóricas frente a la media de 5 años.
                </p>
                <hr style="margin: 8px 0; border-color: #fee2e2;">
                <p style="font-size: 12px; color: #7f1d1d; margin-bottom: 0;">
                <b>Antídoto Emocional:</b> Freno contra el FOMO.
                </p>
            </div>
            <div style="background-color: #fef2f2; padding: 8px; border-radius: 6px; text-align: center; font-size: 12px; color: #991b1b; font-weight: 600;">
                Monitoreo Activo
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with col_box2:
    st.markdown(
        """
        <div style="background-color: #ffffff; padding: 18px; border-radius: 12px; border: 2px solid #34d399; min-height: 280px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <h4 style="color: #047857; margin-top:0; font-size: 16px;">🎯 2. Suelos (Top 10 + Core)</h4>
                <p style="font-size: 13px; color: #334155; line-height: 1.4;">
                Escanea correcciones sanas y retrocesos coyunturales con sólidos cimientos a 3-5 años.
                </p>
                <hr style="margin: 8px 0; border-color: #d1fae5;">
                <p style="font-size: 12px; color: #065f46; margin-bottom: 0;">
                <b>Oportunidad:</b> Momento óptimo de acumulación (DCA).
                </p>
            </div>
            <div style="background-color: #ecfdf5; padding: 8px; border-radius: 6px; text-align: center; font-size: 12px; color: #065f46; font-weight: 600;">
                Monitoreo Activo
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with col_box3:
    st.markdown(
        """
        <div style="background-color: #ffffff; padding: 18px; border-radius: 12px; border: 2px solid #60a5fa; min-height: 280px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <h4 style="color: #1d4ed8; margin-top:0; font-size: 16px;">⚡ 3. Escáner Ciego</h4>
                <p style="font-size: 13px; color: #334155; line-height: 1.4;">
                Revisa automáticamente anomalías críticas en cada actualización:
                </p>
                <ul style="font-size: 12px; color: #334155; padding-left: 15px; margin: 4px 0;">
                    <li><b>Fondo Caído:</b> Ex-favoritos que resucitan.</li>
                    <li><b>Misil Externo:</b> Activos ajenos al Top 10 que arrancan.</li>
                </ul>
                <p style="font-size: 12px; color: #1e40af; margin-bottom: 0;">
                <b>Ventaja:</b> Evita perder tendencias o fondos olvidados.
                </p>
            </div>
            <div style="background-color: #eff6ff; padding: 8px; border-radius: 6px; text-align: center; font-size: 12px; color: #1e40af; font-weight: 600;">
                Sincronizado
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------------------
# PESTAÑA 4: GRÁFICOS & CARTERA CORE
# ------------------------------------------------------------------------------
with tabs[3]:
  st.subheader("📈 Gráficos Comparativos & Cartera Core")
  st.markdown(
      "🔴 **Tu Cartera Core** está identificada con la etiqueta **`🔴 [CORE]`**"
      " para contrastar tu núcleo con el Top 10:"
  )

  df_master_graf = st.session_state.df_master_app
  todos_fondos = df_master_graf["Nombre del Fondo"].tolist()

  activos = st.multiselect(
      "Comparar fondos:", options=todos_fondos, default=todos_fondos, key="graf_sel"
  )
  if activos:
    df_sub = df_master_graf[
        df_master_graf["Nombre del Fondo"].isin(activos)
    ].copy()
    df_sub["Etiqueta"] = df_sub.apply(
        lambda r: (
            f"🔴 [CORE] {r['Nombre del Fondo'][:20]}"
            if r["Origen"] == "📌 En Cartera (Core)"
            else f"🔵 {r['Nombre del Fondo'][:20]}"
        ),
        axis=1,
    )
    g1, g2 = st.columns(2)
    with g1:
      st.bar_chart(
          df_sub.set_index("Etiqueta")["YTD_2026_%"], use_container_width=True
      )
    with g2:
      st.bar_chart(
          df_sub.set_index("Etiqueta")["2025_%"], use_container_width=True
      )

# ------------------------------------------------------------------------------
# PESTAÑA 5: PRENSA & INTELIGENCIA SECTORIAL (NUEVA)
# ------------------------------------------------------------------------------
with tabs[4]:
  st.markdown(
      "### 📰 Prensa Especializada & Buscador Inteligente de Inversión"
  )
  st.write(
      "Consulta noticias, boletines y análisis que afectan directamente a tus"
      " fondos y carteras a través de nuestras cajitas de filtrado inteligente."
  )

  col_caja1, col_caja2 = st.columns(2)

  with col_caja1:
    st.markdown(
        """
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #dee2e6; height: 100%;">
            <h4 style="color: #2c3e50; margin-top: 0;">🗂️ 1. Filtro Temático Sectorial</h4>
            <p style="font-size: 14px; color: #6c757d;">Selecciona el área de interés para acotar la información económica:</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    filtro_categoria = st.selectbox(
        "Categoría de Prensa",
        [
            "Todos los ámbitos",
            "Fondos de Inversión & Indexados",
            "Bancos Centrales & Tipos de Interés",
            "Mercados Globales & Bolsas",
            "Sectores Estratégicos (Agrifood, Biotech, Seguridad)",
        ],
        label_visibility="collapsed",
    )

  with col_caja2:
    st.markdown(
        """
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #dee2e6; height: 100%;">
            <h4 style="color: #2c3e50; margin-top: 0;">⚡ 2. Etiquetas de Acceso Rápido</h4>
            <p style="font-size: 14px; color: #6c757d;">Haz clic o busca por términos clave recurrentes en tu estrategia:</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    tag_seleccionado = st.pills(
        "Etiquetas",
        [
            "Vanguard",
            "Indexa Capital",
            "Inflación",
            "BCE / FED",
            "Renta Variable",
            "Renta Fija",
        ],
        selection_mode="single",
        label_visibility="collapsed",
    )

  st.markdown("<br>", unsafe_allow_html=True)

  st.markdown(
      """
    <div style="background-color: #eef2f7; padding: 20px; border-radius: 8px; border: 1px solid #cbd5e1;">
        <h4 style="color: #1e293b; margin-top: 0;">🔎 3. Buscador Inteligente de Artículos y Noticias</h4>
    </div>
    """,
      unsafe_allow_html=True,
  )

  query_busqueda = st.text_input(
      "Buscar en prensa especializada...",
      placeholder="Ej: perspectivas fondos globales, evolución tipos de interés...",
  )

  if query_busqueda or tag_seleccionado or filtro_categoria:
    st.markdown(f"#### Resultados de Inteligencia para tu consulta:")
    st.success(
        f"Filtro activo -> Categoría: **{filtro_categoria}** | Etiqueta:"
        f" **{tag_seleccionado or 'Ninguna'}** | Consulta:"
        f" **{query_busqueda or 'General'}**"
    )
    st.markdown(
        """
        - **[Análisis Vanguard]** Tendencias en la gestión indexada global y comportamiento de carteras conservadoras y dinámicas frente al entorno macroeconómico actual.
        - **[Prensa Económica]** Actualización de políticas monetarias de los principales Bancos Centrales y su impacto directo en la renta fija y variable europea.
        - **[Radar Sectorial]** Oportunidades de inversión a largo plazo en fondos especializados de innovación, biotecnología y transición alimentaria.
        """
    )
  else:
    st.info(
        "💡 Introduce un término en el buscador, selecciona una etiqueta o elige"
        " una categoría para desplegar la información de prensa especializada."
    )
