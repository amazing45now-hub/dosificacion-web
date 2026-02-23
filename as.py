import streamlit as st
import pandas as pd

# Configuración estética de la página
st.set_page_config(page_title="Dosificación de Hormigón - Aduviri", layout="wide")

# Estilo personalizado para parecerse a la app de tu amigo
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stNumberInput { border-radius: 10px; }
    .result-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .titulo-principal {
        color: white;
        background-color: #1e3d59;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="titulo-principal"><h1>DOSIFICACIÓN VOLUMÉTRICA (GUÍA ADUVIRI)</h1></div>', unsafe_allow_html=True)

# --- BLOQUES DE ENTRADA (Como las tarjetas de la foto) ---
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown('<div class="result-card"><h3>1️⃣ Diseño Base</h3>', unsafe_allow_html=True)
    p_are = st.number_input("Partes Arena", value=2.0, step=0.1)
    p_gra = st.number_input("Partes Grava", value=3.0, step=0.1)
    ac_base = st.number_input("Relación A/C", value=0.52, format="%.3f")
    st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="result-card"><h3>2️⃣ Propiedades Físicas</h3>', unsafe_allow_html=True)
    temp = st.number_input("Temp. Agua (°C)", value=16.1)
    e = st.number_input("% Esponjamiento", value=15.0)
    st.markdown('</div>', unsafe_allow_html=True)

with col_c:
    st.markdown('<div class="result-card"><h3>3️⃣ Humedad y Absorción</h3>', unsafe_allow_html=True)
    ha = st.number_input("% Humedad Arena", value=4.5)
    absa = st.number_input("% Abs. Arena", value=1.2)
    hg = st.number_input("% Humedad Grava", value=1.5)
    absg = st.number_input("% Abs. Grava", value=0.8)
    st.markdown('</div>', unsafe_allow_html=True)

# --- LÓGICA DE CÁLCULO ---
# Interpolación Densidad Agua (Pág 10)
rho_w = 999.01 + (temp - 15.6) * (998.54 - 999.01) / (18.3 - 15.6)
# Arena Corregida (Pág 14)
are_b = p_are * (1 + e/100)
# Agua Corregida (Pág 16)
aporte_a = ((ha - absa) / 100) * p_are
aporte_g = ((hg - absg) / 100) * p_gra
agua_b = ac_base - aporte_a - aporte_g

# --- RESULTADOS (La tabla pro de la foto) ---
st.markdown("---")
st.markdown('<h2 style="text-align: center;">📊 RESULTADOS: PLANILLA OPERATIVA</h2>', unsafe_allow_html=True)

# Cuadros de resumen arriba de la tabla
res1, res2, res3 = st.columns(3)
res1.metric("Densidad H2O", f"{rho_w:.2f} kg/m³")
res2.metric("Aporte Humedad Agregados", f"{aporte_a + aporte_g:.3f} vol.")
res3.metric("Relación A/C Real", f"{ac_base:.3f}")

# Tabla final
df_res = pd.DataFrame({
    "MATERIAL": ["AGUA (L)", "CEMENTO", "GRAVA", "ARENA"],
    "COL A (Base)": [f"{ac_base:.3f}", "1.00", f"{p_gra:.2f}", f"{p_are:.2f}"],
    "COL B (Ajustada)": [f"{agua_b:.3f}", "1.00", f"{p_gra:.2f}", f"{are_b:.2f}"],
    "OBSERVACIONES": [f"Dens: {rho_w:.2f}", "Referencia", "Sin cambios", f"Corr. E={e}%"]
})

st.table(df_res)

st.markdown('<p style="text-align: center; color: gray;">Desarrollado según Guía Aduviri - Ingeniería Civil</p>', unsafe_allow_html=True)
