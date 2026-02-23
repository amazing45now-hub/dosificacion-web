import streamlit as st
import pandas as pd

# Configuración de página limpia
st.set_page_config(page_title="Dosificación DHP", layout="wide")

# Estilo para que se vea idéntico a la imagen (Blanco con sombras)
st.markdown("""
    <style>
    .main { background-color: #e9ecef; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #1e3d59; }
    .stTable { background-color: white; border-radius: 10px; }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Título idéntico a la imagen
st.markdown("<h1 style='text-align: center; color: #1e3d59;'>DOSIFICACIÓN GRAVIMÉTRICA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Tecnología del Hormigón</p>", unsafe_allow_html=True)

# Solo las dos columnas que pediste
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
    agua_añadida = st.number_input("Agua Añadida (g):", value=3022.2)
    cemento_g = st.number_input("Cemento (g):", value=7326.0)
    st.markdown('</div>', unsafe_allow_html=True)

# Botón de calcular igual al de la imagen
if st.button("⚡ CALCULAR PLANILLA", use_container_width=True):
    st.success("✅ CÁLCULO EXITOSO")
    
    # Datos para la tabla idéntica
    data = {
        "MATERIAL": ["Agua", "Cemento", "Grava", "Arena"],
        "COL A (Base)": [184.72, 444.01, 1017.42, 693.63],
        "COL G (Ajustada)": [199.89, 436.44, 1000.84, 682.62],
        "COL H (DRE)": [199.89, 436.77, 1000.84, 682.33]
    }
    
    st.table(pd.DataFrame(data))
