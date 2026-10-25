import datetime
import streamlit as st

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Mi Broker Privado",
    page_icon="🛡️",
    layout="wide",
)

# --- CABECERA SUPERIOR Y BOTÓN DE GITHUB ESTILIZADO ---
col_head1, col_head2 = st.columns([8, 2])

with col_head1:
    st.markdown(
        """
        <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px; border: 1px solid #90caf9; text-align: center;">
            <h2 style="color: #0d47a1; margin: 0;">🛡️ 📈 MI BROKER PRIVADO</h2>
            <p style="color: #1565c0; margin: 5px 0 0 0; font-weight: 500;">
                Panel Táctico • Hora Oficial España: {}
            </p>
        </div>
        """.format(
            datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ),
        unsafe_allow_html=True,
    )

with col_head2:
    st.markdown(
        """
        <div style="display: flex; justify-content: flex-end; align-items: center; height: 100%;">
            <a href="https://github.com/mahega2005-jpg/mi-broker-privado2026" target="_blank" 
               style="background-color: #24292e; color: white; padding: 10px 18px; border-radius: 6px; 
                      text-decoration: none; font-weight: bold; font-size: 14px; display: inline-flex; align-items: center; gap: 8px;">
                <svg height="18" width="18" viewBox="0 0 16 16" version="1.1" fill="white">
                    <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.22 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
                GitHub
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# --- NAVEGACIÓN POR PESTAÑAS (AMPLIADA A 5) ---
tabs = st.tabs(
    [
        "Control & Bandas",
        "Buscador Maestro",
        "Radar de Tendencias & Estrategias",
        "Gráficos & Cartera Core",
        "📰 Prensa & Inteligencia Sectorial",
    ]
)

# Pestaña 1: Control & Bandas
with tabs[0]:
    st.markdown("### 🛡️ Supervisión 24h de Bandas (Suelos y Techos)")
    st.write("Edita las bandas de control de tus posiciones activas:")

    # Datos de ejemplo de la tabla operativa
    import pandas as pd

    data_bandas = pd.DataFrame(
        {
            "ISIN": ["IE00BFPM9N11", "IE00BGCZOB53"],
            "Nombre": [
                "Vanguard Global Stock Index Inst Plus EUR Acc",
                "Vanguard Global Bond Index Inst Plus EUR Hgd",
            ],
            "Suelo_%": [-10, -8],
            "Techo_%": [25, 15],
            "Email": ["mahega2005@gmail.com", "mahega2005@gmail.com"],
        }
    )
    st.dataframe(data_bandas, use_container_width=True)

# Pestaña 2: Buscador Maestro
with tabs[1]:
    st.markdown("### 🔍 Buscador Maestro de Activos")
    st.info("Utiliza el panel lateral para introducir ISINs y consultar datos.")

# Pestaña 3: Radar de Tendencias
with tabs[2]:
    st.markdown("### 🎯 Radar de Tendencias & Estrategias")
    st.write(
        "Seguimiento de sectores estratégicos (Agrifood, Biotecnología, Seguridad)."
    )

# Pestaña 4: Gráficos & Cartera Core
with tabs[3]:
    st.markdown("### 📊 Gráficos & Cartera Core")
    st.write("Evolución de participaciones y fondos Indexa Capital / Vanguard.")

# Pestaña 5: Prensa & Inteligencia Sectorial (NUEVA)
with tabs[4]:
    st.markdown("### 📰 Prensa Especializada & Buscador Inteligente de Inversión")
    st.write(
        "Consulta noticias, boletines y análisis que afectan directamente a tus fondos y carteras a través de nuestras cajitas de filtrado inteligente."
    )

    # Contenedor en diseño de tarjetas / cajitas
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

    # Cajita del Buscador Inteligente
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
        # Simulación de resultados inteligentes adaptados al sector
        st.success(
            f"Filtro activo -> Categoría: **{filtro_categoria}** | Etiqueta: **{tag_seleccionado or 'Ninguna'}** | Consulta: **{query_busqueda or 'General'}**"
        )

        # Tarjetas de ejemplo de noticias relevantes
        st.markdown(
            """
            - **[Análisis Vanguard]** Tendencias en la gestión indexada global y comportamiento de carteras conservadoras y dinámicas frente al entorno macroeconómico actual.
            - **[Prensa Económica]** Actualización de políticas monetarias de los principales Bancos Centrales y su impacto directo en la renta fija y variable europea.
            - **[Radar Sectorial]** Oportunidades de inversión a largo plazo en fondos especializados de innovación, biotecnología y transición alimentaria.
            """
        )
    else:
        st.info(
            "💡 Introduce un término en el buscador, selecciona una etiqueta o elige una categoría para desplegar la información de prensa especializada."
        )
