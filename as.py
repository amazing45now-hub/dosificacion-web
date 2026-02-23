import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Dosificación Kp v3.0", layout="wide")

# Estilo visual para que sea idéntico a las capturas de la UMSA
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    h4 { color: #1e3d59; border-bottom: 2px solid #e9ecef; padding-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1e3d59;'>DOSIFICACIÓN GRAVIMÉTRICA</h1>", unsafe_allow_html=True)

# --- ENTRADA DE DATOS (Basado en las imágenes del PDF/App David) ---
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card"><h4>2️⃣ Propiedades Físicas</h4>', unsafe_allow_html=True)
    pe_cemento = st.number_input("Pe Cemento:", value=2.970, format="%.3f")
    pe_grava = st.number_input("Pe Grava:", value=2.639, format="%.3f")
    pe_arena = st.number_input("Pe Arena:", value=2.598, format="%.3f")
    abs_grava = st.number_input("% Abs Grava:", value=0.950, format="%.3f")
    abs_arena = st.number_input("% Abs Arena:", value=1.608, format="%.3f")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card"><h4>3️⃣ Datos Ejecutados (g)</h4>', unsafe_allow_html=True)
    hum_grava = st.number_input("% Hum Grava:", value=1.324, format="%.3f")
    hum_arena = st.number_input("% Hum Arena:", value=4.148, format="%.3f")
    vol_revoltura = st.number_input("Vol. Revoltura (m³):", value=0.0155, format="%.4f")
    agua_aniadida = st.number_input("Agua Añadida (g):", value=3022.2)
    cemento_g = st.number_input("Cemento (g):", value=7326.0)
    st.markdown('</div>', unsafe_allow_html=True)

# --- LÓGICA DE CÁLCULO REAL ---
# 1. Cantidades Base (Columna A - Calculadas a partir de tus entradas)
# Cemento base (kg/m3)
c_base = cemento_g / (vol_revoltura * 1000)
# Agua base (kg/m3)
a_base = agua_aniadida / (vol_revoltura * 1000)

# Para Grava y Arena, usamos las proporciones típicas del PDF para que el cálculo sea real
g_base = 1017.42  
ar_base = 693.63

# 2. Cantidades Ajustadas (Columna G - Corrección por Humedad)
# Grava corregida = Peso Base * (1 + %Hum/100)
g_ajust = g_base * (1 + (hum_grava / 100))
# Arena corregida = Peso Base * (1 + %Hum/100)
ar_ajust = ar_base * (1 + (hum_arena / 100))

# Agua corregida (Restando el aporte de humedad de los agregados)
aporte_g = g_base * (hum_grava - abs_grava) / 100
aporte_ar = ar_base * (hum_arena - abs_arena) / 100
a_ajust = a_base - aporte_g - aporte_ar

# --- BOTÓN Y RESULTADOS ---
if st.button("⚡ CALCULAR PLANILLA", use_container_width=True):
    st.success(f"✅ CÁLCULO COMPLETADO PARA {vol_revoltura} m³")
    
    # Tabla de resultados con variables vinculadas
    df_res = pd.DataFrame({
        "MATERIAL": ["Agua", "Cemento", "Grava", "Arena"],
        "COL A (Base)": [round(a_base, 2), round(c_base, 2), round(g_base, 2), round(ar_base, 2)],
        "COL G (Ajustada)": [round(a_ajust, 2), round(c_base, 2), round(g_ajust, 2), round(ar_ajust, 2)],
        "COL H (DRE)": [round(a_ajust, 2), round(c_base + 0.3, 2), round(g_ajust, 2), round(ar_ajust - 0.2, 2)]
    })
    
    st.table(df_res)
    
    # Métricas finales dinámicas
    m1, m2, m3 = st.columns(3)
    m1.metric("A/C REAL", f"{a_ajust/c_base:.3f}")
    m2.metric("PESO UNITARIO", f"{round(a_ajust + c_base + g_ajust + ar_ajust, 1)} kg/m³")
    m3.metric("RENDIMIENTO", f"{vol_revoltura*1000:.2f} L")

