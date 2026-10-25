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
st.sidebar.header("🛡️ Panel Táctico")

with st.sidebar.expander("🧪 Test de Alertas", expanded=False):
  if st.button("🚀 Comprobar Estado", use_container_width=True):
    st.success("Sistemas operativos y escáner autónomo activo.")

with st.sidebar.expander("➕ Añadir / 🗑️ Eliminar ISIN", expanded=False):
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
          st.warning("El ISIN ya
