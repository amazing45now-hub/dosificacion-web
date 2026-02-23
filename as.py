import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Dosificación Aduviri Pro", layout="centered")

st.title("🏗️ Dosificación de Hormigón (Guía Aduviri)")
st.markdown("---")

# --- ENTRADAS EN BARRA LATERAL ---
st.sidebar.header("Datos de Laboratorio")
temp = st.sidebar.number_input("Temp. Agua (°C)", value=16.1)
ha = st.sidebar.number_input("% Humedad Arena", value=4.5)
absa = st.sidebar.number_input("% Abs. Arena", value=1.2)
e = st.sidebar.number_input("% Esponjamiento", value=15.0)
hg = st.sidebar.number_input("% Humedad Grava", value=1.5)
absg = st.sidebar.number_input("% Abs. Grava", value=0.8)

# --- ENTRADAS PRINCIPALES ---
col1, col2, col3 = st.columns(3)
with col1: p_are = st.number_input("Partes Arena", value=2.0)
with col2: p_gra = st.number_input("Partes Grava", value=3.0)
with col3: ac_base = st.number_input("A/C Base", value=0.52)

# --- CÁLCULOS (Lógica Aduviri) ---
# Densidad del agua
rho_w = 999.01 + (temp - 15.6) * (998.54 - 999.01) / (18.3 - 15.6)
# Arena corregida
are_b = p_are * (1 + e/100)
# Agua corregida
aporte_a = ((ha - absa) / 100) * p_are
aporte_g = ((hg - absg) / 100) * p_gra
agua_b = ac_base - aporte_a - aporte_g

# --- TABLA DE RESULTADOS ---
st.subheader("Planilla de Dosificación Operativa")
datos = {
    "Material": ["CEMENTO", "ARENA", "GRAVA", "AGUA (L)"],
    "Base (A)": ["1.00", f"{p_are:.2f}", f"{p_gra:.2f}", f"{ac_base:.3f}"],
    "Operativa (B)": ["1.00", f"{are_b:.2f}", f"{p_gra:.2f}", f"{agua_b:.3f}"],
    "Observaciones": ["Referencia", f"Corr. E={e}%", "Sin cambios", f"Dens. H2O: {rho_w:.2f}"]
}
st.table(pd.DataFrame(datos))

st.info(f"💡 El aporte de humedad de los agregados es de {aporte_a + aporte_g:.3f} volúmenes.")
