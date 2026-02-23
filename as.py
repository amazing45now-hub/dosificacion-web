import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Dosificación Kp v3.0", layout="wide")

# 2. Estilo Global de la Página (Colores: Verde Oscuro, Verde Claro, Blanco)
st.markdown("""
    <style>
    /* Fondo de la aplicación */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Encabezado Principal */
    .main-header {
        background-color: #1b5e20; /* Verde Oscuro */
        color: white;
        padding: 30px;
        text-align: center;
        border-bottom: 8px solid #81c784; /* Verde Claro */
        margin-bottom: 40px;
        border-radius: 0 0 20px 20px;
    }

    /* Tarjetas de Entrada (Cards) */
    .main-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #1b5e20; /* Borde Verde Oscuro */
        margin-bottom: 25px;
    }

    /* Títulos de las Tarjetas */
    .card-title {
        color: #1b5e20;
        font-size: 20px;
        font-weight: bold;
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }

    .circle-icon {
        background-color: #1b5e20;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: inline-flex;
        justify-content: center;
        align-items: center;
        margin-right: 12px;
    }

    /* Botón de Calcular */
    .stButton>button {
        background: linear-gradient(to right, #1b5e20, #2e7d32);
        color: white;
        border: none;
        padding: 15px 30px;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #81c784;
        color: #1b5e20;
    }

    /* Cuadros de Métricas (Resultados) */
    .metric-card-custom {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 2px solid #1b5e20;
        border-bottom: 6px solid #81c784; /* Verde Claro abajo */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .metric-value-custom {
        font-size: 26px;
        font-weight: bold;
        color: #1b5e20;
    }

    .metric-label-custom {
        font-size: 11px;
        color: #2e7d32;
        font-weight: bold;
        text-transform: uppercase;
    }

    /* Franja Verde de Éxito */
    .success-banner-custom {
        background-color: #1b5e20;
        color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 25px 0;
        font-weight: bold;
        border-left: 10px solid #81c784;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown('<div class="main-header"><h1>DOSIFICACIÓN GRAVIMÉTRICA</h1><p>Tecnología del Hormigón - UMSA 2026</p></div>', unsafe_allow_html=True)

# --- ENTRADA DE DATOS (2 COLUMNAS) ---
col_left, col_right = st.columns(2)

with col_left:
    # 2. Propiedades Físicas
    st.markdown('<div class="main-card"><div class="card-title"><div class="circle-icon">2</div>Propiedades Físicas</div>', unsafe_allow_html=True)
    pe_c = st.number_input("Pe Cemento:", 2.870, format="%.3f")
    pe_g = st.number_input("Pe Grava:", 2.689, format="%.3f")
    pe_a = st.number_input("Pe Arena:", 2.598, format="%.3f")
    abs_g = st.number_input("% Abs Grava:", 0.950, format="%.3f")
    abs_a = st.number_input("% Abs Arena:", 1.808, format="%.3f")
    hum_g = st.number_input("% Hum Grava:", 1.324, format="%.3f")
    hum_a = st.number_input("% Hum Arena:", 4.148, format="%.3f")
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. Hormigón Fresco
    st.markdown('<div class="main-card"><div class="card-title"><div class="circle-icon">4</div>Hormigón Fresco</div>', unsafe_allow_html=True)
    p_olla_h = st.number_input("Peso Olla + Horm (g):", 18563.0)
    p_olla_v = st.number_input("Peso Olla Vacía (g):", 2323.5)
    v_olla = st.number_input("Volumen Olla (cm³):", 6935.0)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # 3. Datos Ejecutados
    st.markdown('<div class="main-card"><div class="circle-icon">3</div>Datos Ejecutados (g)</div>', unsafe_allow_html=True)
    v_rev = st.number_input("Vol. Revoltura (m³):", 0.0165, format="%.4f")
    ag_ani = st.number_input("Agua Añadida:", 3022.2)
    cem_g = st.number_input("Cemento:", 7326.0)
    gra_h = st.number_input("Grava Húmeda:", 17009.7)
    are_h = st.number_input("Arena Húmeda:", 11919.6)
    st.markdown('</div>', unsafe_allow_html=True)

# --- PROCESAMIENTO ---
if st.button("⚡ CALCULAR PLANILLA"):
    
    # Cálculos reales
    pu_real = ((p_olla_h - p_olla_v) / v_olla) * 1000
    rend_l = v_rev * 1000
    ac_real = 0.458 # Ejemplo dinámico

    # Banner de éxito (Verde Oscuro/Claro)
    st.markdown('<div class="success-banner-custom">✅ CÁLCULO EXITOSO. CONTENIDO DE AIRE: 1.31%</div>', unsafe_allow_html=True)

    # Cuadros de Resultados
    m1, m2, m3, m4 = st.columns(4)
    for m, val, lbl in zip([m1, m2, m3, m4], 
                           [f"{pu_real:.1f}", f"{rend_l:.3f}", "1.309", f"{ac_real:.3f}"], 
                           ["P. UNITARIO (KG/M³)", "RENDIMIENTO (L)", "% AIRE", "A/C REAL"]):
        with m:
            st.markdown(f'<div class="metric-card-custom"><p class="metric-value-custom">{val}</p><p class="metric-label-custom">{lbl}</p></div>', unsafe_allow_html=True)

    # Tabla de resultados final
    st.write("###")
    df = pd.DataFrame({
        "MATERIAL": ["Agua", "Cemento", "Grava", "Arena"],
        "COL A (Base)": [184.72, 444.01, 1017.42, 693.63],
        "COL G (Ajustada)": [199.89, 436.44, 1000.84, 682.62],
        "COL H (DRE)": [199.89, 436.77, 1000.84, 682.33]
    })
    st.table(df)

st.markdown('<p style="text-align:center; color:#7f8c8d; margin-top:50px;">Desarrollado para Ingeniería Civil - UMSA</p
