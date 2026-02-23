import streamlit as st
import pandas as pd

# Configuración estética de la página
st.set_page_config(page_title="Dosificación de Hormigón - Aduviri", layout="wide")

# Estilo personalizado para tarjetas y títulos (Nivel UMSA)
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
        height: 100%;
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

# --- BLOQUES DE ENTRADA (Ahora solo 2 columnas principales) ---
col_b, col_c = st.columns(2)

with col_b:
    st.markdown('<div class="result-card"><h3>1️⃣ Propiedades Físicas</h3>', unsafe_allow_html=True)
    temp = st.number_input("Temp. Agua (°C)", value=16.1)
    e = st.number_input("% Esponjamiento de la Arena", value=15.0)
    p_are_fija = 2.0  # Valor base si no se pide entrada
    p_gra_fija = 3.0  # Valor base si no se pide entrada
    ac_base_fija = 0.520 # Valor base
    st.markdown('</div>', unsafe_allow_html=True)

with col_c:
    st.markdown('<div class="result-card"><h3>2️⃣ Humedad y Absorción</h3>', unsafe_allow_html=True)
    ha = st.number_input("% Humedad Arena", value=4.5)
    absa = st.number_input("% Abs. Arena", value=1.2)
    hg = st.number_input("% Humedad Grava", value=1.5)
    absg = st.number_input("% Abs. Grava", value=0.8)
    st.markdown('</div>', unsafe_allow_html=True)

# --- LÓGICA DE CÁLCULO ADUVIRI ---
# Interpolación Densidad Agua
rho_w = 999.01 + (temp - 15.6) * (998.54 - 999.01) / (18.3 - 15.6)
# Arena Corregida por Esponjamiento
are_b = p_are_fija * (1 + e/100)
# Agua Corregida por Aportes de Humedad
aporte_a = ((ha - absa) / 100) * p_are_fija
aporte_g = ((hg - absg) / 100) * p_gra_fija
agua_b = ac_base_fija - aporte_a - aporte_g

# --- SECCIÓN DE RESULTADOS ---
st.markdown("---")
st.markdown('<h2 style="text-align: center;">📊 RESULTADOS: PLANILLA OPERATIVA</h2>', unsafe_allow_html=True)

# Métricas de resumen (Estilo UMSA)
res1, res2, res3, res4 = st.columns(4)
res1.metric("Densidad H2O", f"{rho_w:.2f} kg/m³")
res2.metric("Aporte Arena", f"{aporte_a:.3f} vol.")
res3.metric("Aporte Grava", f"{aporte_g:.3f} vol.")
res4.metric("A/C Real", f"{ac_base_fija:.3f}")

# Tabla de dosificación
df_res = pd.DataFrame({
    "MATERIAL": ["AGUA (L)", "CEMENTO", "GRAVA", "ARENA"],
    "DOSIF. BASE": [f"{ac_base_fija:.3f}", "1.00", f"{p_gra_fija:.2f}", f"{p_are_fija:.2f}"],
    "DOSIF. OPERATIVA": [f"{agua_b:.3f}", "1.00", f"{p_gra_fija:.2f}", f"{are_b:.2f}"],
    "OBSERVACIONES": [f"Temp: {temp}°C", "Referencia", "Volumen seco", f"Esponj: {e}%"]
})

st.table(df_res)

st.markdown('<p style="text-align: center; color: gray; margin-top: 50px;">Facultad de Ingeniería - UMSA 2026</p>', unsafe_allow_html=True)
