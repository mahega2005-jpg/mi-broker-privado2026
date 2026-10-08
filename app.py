import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Mi Broker Privado", page_icon="🛡️", layout="centered")

# --- CABECERA Y LOGOTIPO ---
st.markdown("""
<div style="background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); padding: 25px; border-radius: 15px; text-align: center; color: white; font-family: sans-serif; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);">
    <div style="font-size: 40px; margin-bottom: 5px;">🛡️📈</div>
    <h2 style="margin: 0; font-size: 24px; letter-spacing: 1px;">MI BROKER PRIVADO</h2>
    <p style="margin: 5px 0 0 0; font-size: 13px; color: #a2dbfa;">Panel de Control, Cartera Eficiente & Analizador ISIN (España)</p>
    <div style="margin-top: 15px; display: inline-block; background: #00b09b; color: white; padding: 6px 15px; border-radius: 15px; font-size: 11px; font-weight: bold;">
        ESTADO: CARTERA EFICIENTE & ANALIZADOR ACTIVO 🇪🇸
    </div>
</div>
<br>
""", unsafe_allow_html=True)

# --- BASE DE DATOS DE TU CARTERA Y FONDOS DE REFERENCIA ---
data_fondos = {
    'Nombre del Fondo': [
        'Vanguard Global Stock Index Institutional Plus EUR', 
        'Vanguard Global Bond Index Institutional Plus EUR', 
        'Polar Capital Biotechnology EUR R Acc',
        'Pictet - Security P EUR',
        'Banco Tradicional Cartera Activa (Ejemplo)'
    ],
    'ISIN': [
        'IE00BFPM9N11', 'IE00BGCZOB53', 'IE00B43VBZ18', 'LU0503631872', 'ES0111222333'
    ],
    'Tipo': [
        'Renta Variable Global', 'Renta Fija Global (Hedged)', 'Biotecnología (Satélite)', 'Ciberseguridad (Satélite)', 'Gestión Activa (Banco)'
    ],
    'TER_%': [0.10, 0.10, 1.25, 1.00, 1.85],       
    'YTD_2026_%': [18.55, -3.35, 11.5, 14.2, 2.1],
    '2025_%': [6.73, 2.89, 14.0, 22.5, 4.2],
    '2024_%': [26.59, 0.88, 8.5, 25.1, 5.0],
    '2023_%': [19.63, 4.74, 6.2, 18.0, 3.5],
    '2022_%': [-12.79, -15.03, -12.4, -20.1, -8.5],
    'Política / Destino de los Fondos': [
        'Invierte en acciones de grandes y medianas empresas de mercados desarrollados globales replicando el MSCI World.',
        'Proporciona rendimientos en consonancia con la renta fija global de gobiernos y corporaciones con cobertura en euros.',
        'Invierte globalmente en empresas del sector biotecnológico, ciencias de la salud e innovación farmacéutica.',
        'Se enfoca en empresas de ciberseguridad, protección de datos e infraestructuras tecnológicas críticas.',
        'Cartera activa tradicional gestionada por entidades bancarias con comisiones elevadas.'
    ],
    'Operador / Contratación en España': [
        'MyInvestor / Renta 4 (Transferencia bancaria o efectivo)', 
        'MyInvestor / Renta 4 (Transferencia bancaria o efectivo)', 
        'MyInvestor / Openbank / Bróker europeo', 
        'MyInvestor / Allfunds / Renta 4', 
        'Tu Banco Tradicional (Evitar)'
    ]
}

df_master = pd.DataFrame(data_fondos)

# --- NUEVA SECCIÓN: ANALIZADOR EXPRÉS POR CÓDIGO ISIN ---
st.subheader("🔍 Analizador Exprés por Código ISIN")
st.markdown("Pega o introduce un código ISIN a continuación para generar un informe rápido con su política, comisiones y rentabilidades históricas:")

isin_input = st.text_input("Introduce el ISIN (ej: IE00BFPM9N11)", "").strip().upper()

if isin_input:
    fondo_encontrado = df_master[df_master['ISIN'] == isin_input]
    if not fondo_encontrado.empty:
        row = fondo_encontrado.iloc[0]
        st.success(f"### 📋 Informe de Fondo: {row['Nombre_del_Fondo'] if 'Nombre_del_Fondo' in row else row['Nombre del Fondo']}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Comisión TER", f"{row['TER_%']}%")
        with col2:
            st.metric("Rentabilidad YTD 2026", f"{row['YTD_2026_%']}%")
        with col3:
            st.metric("Rentabilidad 2024", f"{row['2024_%']}%")

        st.markdown(f"**📌 Tipo de Activo:** {row['Tipo']}")
        st.markdown(f"**🎯 Destino / Política de Inversión:** {row['Política / Destino de los Fondos']}")
        st.markdown(f"**🏦 Dónde contratarlo en España:** {row['Operador / Contratación en España']}")
        
        # Desglose detallado anual
        st.markdown("**📊 Histórico de Rentabilidades Anuales:**")
        df_hist = pd.DataFrame({
            'Año': ['2022', '2023', '2024', '2025', '2026 (YTD)'],
            'Rentabilidad (%)': [row['2022_%'], row['2023_%'], row['2024_%'], row['2025_%'], row['YTD_2026_%']]
        })
        st.dataframe(df_hist.set_index('Año'), use_container_width=True)
    else:
        st.warning(f"El ISIN `{isin_input}` no está registrado en tu base de datos interna actual. Puedes añadirlo fácilmente modificando el diccionario de Python en GitHub.")

st.markdown("---")

# --- BARRA LATERAL: FILTROS DE CARTERA ---
st.sidebar.header("🎛️ Filtros de Cartera")
ter_limite = st.sidebar.slider("Filtrar por TER Máximo (%)", min_value=0.0, max_value=3.0, value=3.0, step=0.05)
filtro_tipo = st.sidebar.selectbox("Filtrar por Tipo", ["Todos", "Renta Variable Global", "Renta Fija Global (Hedged)", "Biotecnología (Satélite)", "Ciberseguridad (Satélite)"])

df_filtrado = df_master[df_master['TER_%'] <= ter_limite]
if filtro_tipo != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Tipo'] == filtro_tipo]

# --- VISUALIZACIÓN DE TU CARTERA EFICIENTE ---
st.subheader("💼 Tu Cartera Eficiente Actual")
st.dataframe(df_filtrado[['Nombre del Fondo', 'ISIN', 'Tipo', 'TER_%', 'YTD_2026_%', '2025_%', '2024_%', 'Operador / Contratación en España']].reset_index(drop=True), use_container_width=True)
