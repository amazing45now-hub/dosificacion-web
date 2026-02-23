import tkinter as tk
from tkinter import ttk, messagebox

def calcular():
    try:
        # --- LÓGICA ADUVIRI ---
        t = float(ent_t.get())
        ha, absa, e = float(ent_ha.get()), float(ent_absa.get()), float(ent_e.get())
        hg, absg = float(ent_hg.get()), float(ent_absg.get())
        p_are, p_gra, ac_base = float(ent_p_are.get()), float(ent_p_gra.get()), float(ent_ac.get())

        # 1. Densidad del Agua (Interpolación Pág. 10)
        rho_w = 999.01 + (t - 15.6) * (998.54 - 999.01) / (18.3 - 15.6)
        # 2. Arena Corregida por Esponjamiento (Pág. 14)
        are_b = p_are * (1 + e/100)
        # 3. Agua corregida por aportes (Pág. 16)
        aporte_a = ((ha - absa) / 100) * p_are
        aporte_g = ((hg - absg) / 100) * p_gra
        agua_b = ac_base - aporte_a - aporte_g

        # --- LIMPIAR Y LLENAR TABLA ---
        for row in tabla.get_children(): tabla.delete(row)
        
        filas = [
            ("CEMENTO", "1.00", "1.00", "Referencia fija"),
            ("ARENA", f"{p_are:.2f}", f"{are_b:.2f}", f"Corr. Esp. {e}%"),
            ("GRAVA", f"{p_gra:.2f}", f"{p_gra:.2f}", "Sin cambios"),
            ("AGUA (L)", f"{ac_base:.3f}", f"{agua_b:.3f}", f"Dens: {rho_w:.2f} kg/m3")
        ]
        for f in filas: tabla.insert("", "end", values=f)
        lbl_info.config(text=f"✅ Cálculo exitoso. Densidad del agua: {rho_w:.2f} kg/m³", fg="#2ecc71")

    except:
        messagebox.showerror("Error", "Ingresa datos numéricos válidos.")

# --- INTERFAZ ESTILO WEB APP ---
root = tk.Tk()
root.title("Aduviri Mix Design Pro")
root.geometry("850x600")
root.configure(bg="#f8f9fa")

# Barra lateral (Sidebar)
sidebar = tk.Frame(root, bg="#2c3e50", width=250, padx=20, pady=20)
sidebar.pack(side="left", fill="y")

tk.Label(sidebar, text="DATOS DE\nLABORATORIO", font=("Arial", 12, "bold"), bg="#2c3e50", fg="white").pack(pady=10)

def crear_label_input(txt, val):
    tk.Label(sidebar, text=txt, bg="#2c3e50", fg="#bdc3c7").pack(anchor="w", pady=(10,0))
    ent = tk.Entry(sidebar, font=("Arial", 10))
    ent.insert(0, val)
    ent.pack(fill="x")
    return ent

ent_t = crear_label_input("Temp. Agua (°C):", "16.1")
ent_ha = crear_label_input("% Humedad Arena:", "4.5")
ent_absa = crear_label_input("% Abs. Arena:", "1.2")
ent_e = crear_label_input("% Esponjamiento:", "15.0")
ent_hg = crear_label_input("% Humedad Grava:", "1.5")
ent_absg = crear_label_input("% Abs. Grava:", "0.8")

# Panel Principal
main = tk.Frame(root, bg="#f8f9fa", padx=30, pady=20)
main.pack(side="right", fill="both", expand=True)

tk.Label(main, text="DOSIFICACIÓN VOLUMÉTRICA", font=("Arial", 18, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(pady=10)

# Inputs de Dosificación Base
f_base = tk.Frame(main, bg="#f8f9fa")
f_base.pack(pady=10)

tk.Label(f_base, text="Arena (A):", bg="#f8f9fa").grid(row=0, column=0)
ent_p_are = tk.Entry(f_base, width=8); ent_p_are.insert(0, "2.0"); ent_p_are.grid(row=0, column=1, padx=5)

tk.Label(f_base, text="Grava (A):", bg="#f8f9fa").grid(row=0, column=2)
ent_p_gra = tk.Entry(f_base, width=8); ent_p_gra.insert(0, "3.0"); ent_p_gra.grid(row=0, column=3, padx=5)

tk.Label(f_base, text="A/C Base:", bg="#f8f9fa").grid(row=0, column=4)
ent_ac = tk.Entry(f_base, width=8); ent_ac.insert(0, "0.52"); ent_ac.grid(row=0, column=5, padx=5)

# Botón
btn = tk.Button(main, text="GENERAR PLANILLA", bg="#3498db", fg="white", font=("Arial", 10, "bold"), 
                padx=20, pady=10, command=calcular, relief="flat")
btn.pack(pady=20)

# Tabla
style = ttk.Style()
style.configure("Treeview", font=("Arial", 10), rowheight=25)
cols = ("M", "A", "B", "O")
tabla = ttk.Treeview(main, columns=cols, show="headings", height=5)
for c, h in zip(cols, ["Material", "Base (Col. A)", "Operativa (Col. B)", "Notas"]):
    tabla.heading(c, text=h)
    tabla.column(c, width=120, anchor="center")
tabla.pack(fill="x")

lbl_info = tk.Label(main, text="Complete los datos para calcular", bg="#f8f9fa", fg="#7f8c8d", font=("Arial", 9, "italic"))
lbl_info.pack(pady=20)

root.mainloop()