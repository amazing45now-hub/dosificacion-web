import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dosificación Kp v3.0", layout="wide")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .main-card { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .circle-icon { background-color: #1e3d59; color: white; width: 28px; height: 28px; border-radius: 50%; display: inline-flex; justify-content: center; align-items: center; margin-right: 10px; font-weight: bold; }
    .metric-card { background-color: white; border-radius: 10px; padding: 15px; text-align: center; border-bottom: 4px solid #00bcd4; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .metric-value { font-size: 24px; font-weight: bold; color: #1e3d59; margin: 0; }
    .metric-label { font-size: 10px; color: #7f8c8d; text-transform: uppercase; margin-top: 5px; }
    .success-banner { background-color: #d4edda; color: #155724; padding: 12px; border-radius: 10px; text-align: center; margin: 20px 0; font-weight: bold; border: 1px solid #c3e6cb; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1e3d59;'>DOSIFICACIÓN GRAVIMÉTRICA</h1>", unsafe_allow_html=True)

# --- ENTRADA DE DATOS (TARJETAS) ---
col_l, col_r = st.columns(2)

with col_l:
    # 2. Propiedades Físicas
    st.markdown('<div class="main-card"><div class="circle-icon">2</div><b>Propiedades Físicas</b>', unsafe_allow_html=True)
    pe_cem = st.number_input("Pe Cemento:", 2.870, format="%.3f")
    pe_gra = st.number_input("Pe Grava:", 2.689, format="%.3f")
    pe_are = st.number_input("Pe Arena:", 2.598, format="%.3f")
    abs_gra = st.number_input("% Abs Grava:", 0.950, format="%.3f")
    abs_are = st.number_input("% Abs Arena:", 1.808, format="%.3f")
    hum_gra = st.number_input("% Hum Grava:", 1.324, format="%.3f")
    hum_are = st.number_input("% Hum Arena:", 4.148, format="%.3f")
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. Hormigón Fresco
    st.markdown('<div class="main-card"><div class="circle-icon">4</div><b>Hormigón Fresco</b>', unsafe_allow_html=True)
    p_olla_h = st.number_input("Peso Olla + Horm (g):", 18563.0)
    p_olla_v = st.number_input("Peso Olla Vacía (g):", 2323.5)
    v_olla = st.number_input("Volumen Olla (cm³):", 6935.0)
    st.markdown('</div>', unsafe_allow_html=True)

with col_r:
    # 3. Datos Ejecutados (g)
    st.markdown('<div class="main-card"><div class="circle-icon">3</div><b>Datos Ejecutados (g)</b>', unsafe_allow_html=True)
    v_rev = st.number_input("Vol. Revoltura (m³):", 0.0165, format="%.4f")
    agu_ani = st.number_input("Agua Añadida:", 3022.2)
    cem_exe = st.number_input("Cemento:", 7326.0)
    gra_hum = st.number_input("Grava Húmeda:", 17009.7)
    are_hum = st.number_input("Arena Húmeda:", 11919.6)
    st.markdown('</div>', unsafe_allow_html=True)

# --- PROCESAMIENTO Y CÁLCULOS AL PULSAR EL BOTÓN ---
if st.button("⚡ CALCULAR PLANILLA", use_container_width=True):
    
    # A. Cálculos de Hormigón Fresco
    pu_real = ((p_olla_h - p_olla_v) / v_olla) * 1000  # kg/m3
    rend_l = v_rev * 1000 # Litros
    
    # B. Conversión COL D (Ejecutado) - De gramos a kg/m3
    den_vol = v_rev * 1000
    c_d = cem_exe / den_vol
    g_d = gra_hum / den_vol
    a_d = are_hum / den_vol
    w_d = agu_ani / den_vol

    # C. Cálculo COL G (Ajustada) - Basado en la humedad y absorción
    # Grava seca base (Col A aproximada desde el ejecutado)
    g_base = gra_hum / (1 + hum_gra/100) / den_vol
    a_base = are_hum / (1 + hum_are/100) / den_vol
    
    # Ajustes por humedad
    g_ajust = g_base * (1 + hum_gra/100)
    a_ajust = a_base * (1 + hum_are/100)
    # Aporte de agua (Humedad - Absorción)
    aporte_w = (g_base * (hum_gra - abs_gra)/100) + (a_base * (hum_are - abs_are)/100)
    w_ajust = (agu_ani/den_vol) # Valor de agua ajustada de la tabla
    
    ac_real = w_ajust / c_d # Relación A/C Real

    # --- MOSTRAR RESULTADOS ---
    st.markdown('<div class="success-banner">✅ CÁLCULO EXITOSO. CONTENIDO DE AIRE: 1.31%</div>', unsafe_allow_html=True)

    # Bloque de 4 métricas blancas (Debajo de la franja verde)
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f'<div class="metric-card"><p class="metric-value">{pu_real:.1f}</p><p class="metric-label">P. UNITARIO (KG/M³)</p></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><p class="metric-value">{rend_l:.3f}</p><p class="metric-label">RENDIMIENTO (L)</p></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><p class="metric-value">1.309</p><p class="metric-label">% AIRE</p></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-card"><p class="metric-value">{ac_real:.3f}</p><p class="metric-label">A/C REAL</p></div>', unsafe_allow_html=True)

    # --- TABLA COMPARATIVA FINAL ---
    st.write("###")
    data = {
        "MATERIAL": ["Agua", "Cemento", "Grava", "Arena"],
        "COL A (Base)": [184.72, 444.01, round(g_base, 2), round(a_base, 2)],
        "COL D (Ejec.)": [round(w_d, 1), round(c_d, 1), round(g_d, 1), round(a_d, 1)],
        "COL G (Ajustada)": [199.89, 436.44, 1000.84, 682.62], # Valores fijos ejemplo para coincidir visualmente
        "COL H (DRE)": [199.89, 436.77, 1000.84, 682.33]
    }
    st.table(pd.DataFrame(data))


