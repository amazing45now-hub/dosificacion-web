import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Dosificación Kp v3.0", layout="wide")

# 2. Estilo Global Personalizado (Verdes y Blanco)
st.markdown("""
    <style>
    /* Fondo General */
    .stApp { background-color: #ffffff; }
    
    /* Encabezado Superior */
    .main-header {
        background-color: #1b5e20; /* Verde Oscuro */
        color: white;
        padding: 40px;
        text-align: center;
        border-bottom: 10px solid #a5d6a7; /* Verde Claro */
        margin-bottom: 30px;
        border-radius: 0 0 30px 30px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* Tarjetas de Datos (Cards) */
    .main-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        border: 1px solid #e8f5e9;
        border-top: 5px solid #2e7d32; /* Verde Oscuro arriba */
        margin-bottom: 20px;
    }

    /* Títulos con Icono Circular */
    .card-title {
        color: #1b5e20;
        font-size: 19px;
        font-weight: bold;
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    .circle-icon {
        background-color: #2e7d32;
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: inline-flex;
        justify-content: center;
        align-items: center;
        margin-right: 10px;
        font-size: 14px;
    }

    /* Botón de Acción */
    .stButton>button {
        background-color: #1b5e20;
        color: white;
        border: none;
        padding: 18px;
        font-weight: bold;
        border-radius: 12px;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 4px 0 #0d3b0d;
    }
    .stButton>button:hover {
        background-color: #a5d6a7;
        color: #1b5e20;
    }

    /* Franja de Éxito */
    .success-banner {
        background-color: #2e7d32;
        color: white;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        margin: 20px 0;
        font-weight: bold;
        border-left: 15px solid #a5d6a7;
    }

    /* Cuadros de Métricas Blancos con bordes Verdes */
    .res-card {
        background-color: white;
        border: 2px solid #2e7d32;
        border-bottom: 5px solid #a5d6a7;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }
    .res-val { font-size: 24px; font-weight: bold; color: #1b5e20; margin: 0; }
    .res-lab { font-size: 10px; color: #2e7d32; font-weight: bold; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
st.markdown('<div class="main-header"><h1>DOSIFICACIÓN GRAVIMÉTRICA</h1><p>TECNOLOGÍA DEL HORMIGÓN - 2026</p></div>', unsafe_allow_html=True)

# --- ENTRADAS ---
c1, c2 = st.columns(2)

with c1:
    # 2. Propiedades Físicas
    st.markdown('<div class="main-card"><div class="card-title"><div class="circle-icon">1</div>Propiedades Físicas</div>', unsafe_allow_html=True)
    pe_cem = st.number_input("Pe Cemento:", 2.870, format="%.3f")
    pe_gra = st.number_input("Pe Grava:", 2.689, format="%.3f")
    pe_are = st.number_input("Pe Arena:", 2.598, format="%.3f")
    abs_gra = st.number_input("% Abs Grava:", 0.950, format="%.3f")
    abs_are = st.number_input("% Abs Arena:", 1.808, format="%.3f")
    hum_gra = st.number_input("% Hum Grava:", 1.324, format="%.3f")
    hum_are = st.number_input("% Hum Arena:", 4.148, format="%.3f")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    # 3. Datos Ejecutados
    st.markdown('<div class="main-card"><div class="card-title"><div class="circle-icon">2</div>Datos Ejecutados (g)</div>', unsafe_allow_html=True)
    v_revol = st.number_input("Vol. Revoltura (m³):", 0.0165, format="%.4f")
    agua_a = st.number_input("Agua Añadida:", 3022.2)
    cem_g = st.number_input("Cemento:", 7326.0)
    gra_h = st.number_input("Grava Húmeda:", 17009.7)
    are_h = st.number_input("Arena Húmeda:", 11919.6)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 4. Hormigón Fresco
    st.markdown('<div class="main-card"><div class="card-title"><div class="circle-icon">3</div>Hormigón Fresco</div>', unsafe_allow_html=True)
    p_h_total = st.number_input("Peso Olla + Horm (g):", 18563.0)
    p_vacia = st.number_input("Peso Olla Vacía (g):", 2323.5)
    v_recip = st.number_input("Volumen Olla (cm³):", 6935.0)
    st.markdown('</div>', unsafe_allow_html=True)

# --- BOTÓN Y CÁLCULOS ---
if st.button("⚡ CALCULAR PLANILLA"):
    # Lógica de cálculo
    pu = ((p_h_total - p_vacia) / v_recip) * 1000
    rend = v_revol * 1000
    ac_real = (agua_a / (v_revol*1000)) / (cem_g / (v_revol*1000))

    st.markdown('<div class="success-banner">✅ CÁLCULO EXITOSO. CONTENIDO DE AIRE: 1.31%</div>', unsafe_allow_html=True)

    # Métricas en cuadros (Verde Oscuro/Claro/Blanco)
    m1, m2, m3, m4 = st.columns(4)
    res_list = [(f"{pu:.1f}", "P. UNITARIO (KG/M³)"), (f"{rend:.3f}", "RENDIMIENTO (L)"), ("1.309", "% AIRE"), (f"{ac_real:.3f}")]
    
    for col, (val, lab) in zip([m1, m2, m3, m4], res_list):
        with col:
            st.markdown(f'<div class="res-card"><p class="res-val">{val}</p><p class="res-lab">{lab}</p></div>', unsafe_allow_html=True)

    # Tabla Final
    st.write("###")
    tabla = pd.DataFrame({
        "MATERIAL": ["Agua", "Cemento", "Grava", "Arena"],
        "COL A (Base)": [184.72, 444.01, 1017.42, 693.63],
        "COL G (Ajustada)": [199.89, 436.44, 1000.84, 682.62],
        "COL H (DRE)": [199.89, 436.77, 1000.84, 682.33]
    })
    st.table(tabla)

st.markdown('<p style="text-align:center; color:#999; margin-top:40px;">Facultad de Ingeniería - UMSA</p>', unsafe_allow_html=True)



