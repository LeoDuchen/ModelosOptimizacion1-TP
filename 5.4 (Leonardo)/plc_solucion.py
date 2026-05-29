"""
=====================================================================
 PROBLEMA DE PROGRAMACIÓN LINEAL (PLC)
 Maximizar Z = 5·X1 + 2·X2
 Restricciones:
   Recurso1:  6·X1 + 4·X2 <= 240
   Recurso2:  2·X1 +   X2 <=  70
   Demanda:          X2  >=  40
   X1, X2 >= 0
=====================================================================
"""

import numpy as np
from scipy.optimize import linprog
from scipy.linalg import solve

# ─── 1. DATOS DEL PROBLEMA ────────────────────────────────────────
c_max = np.array([5.0, 2.0])          # coef. objetivo (maximizar)
c     = -c_max                         # linprog minimiza → negamos

A_ub = np.array([
    [ 6.0,  4.0],   # Recurso1 <=240
    [ 2.0,  1.0],   # Recurso2 <= 70
    [ 0.0, -1.0],   # Demanda  >= 40  → -X2 <= -40
])
b_ub = np.array([240.0, 70.0, -40.0])

bounds = [(0, None), (0, None)]

# ─── 2. RESOLUCIÓN ────────────────────────────────────────────────
res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

X1_opt, X2_opt = res.x
Z_opt          = -res.fun

print("=" * 60)
print("  SOLUCIÓN ÓPTIMA")
print("=" * 60)
print(f"  X1 = {X1_opt:.6f}  ({X1_opt:.4f} ≈ 40/3)")
print(f"  X2 = {X2_opt:.6f}")
print(f"  Z  = {Z_opt:.6f}  ({Z_opt:.4f} ≈ 440/3)")
print()

# ─── 3. HOLGURAS / EXCEDENTES ─────────────────────────────────────
slack1 = 240 - (6*X1_opt + 4*X2_opt)
slack2 =  70 - (2*X1_opt +   X2_opt)
surp3  = (X2_opt) - 40                 # excedente de demanda

print("=" * 60)
print("  HOLGURAS / EXCEDENTES")
print("=" * 60)
print(f"  Recurso1  holgura  = {slack1:.6f}  (restricción {'ACTIVA' if abs(slack1)<1e-6 else 'no activa'})")
print(f"  Recurso2  holgura  = {slack2:.6f}  (restricción {'ACTIVA' if abs(slack2)<1e-6 else 'no activa'})")
print(f"  Demanda   excedent = {surp3:.6f}  (restricción {'ACTIVA' if abs(surp3)<1e-6 else 'no activa'})")
print()

# ─── 4. PRECIOS SOMBRA (DUALES) ───────────────────────────────────
# Tabla óptima (base: X1, X4, X2) → obtenemos duales manualmente
# Base óptima: X1 y X2 (Recurso1 activa, Demanda activa, Recurso2 no activa)
# Sistema: y·B = c_B
# B = [[6,0],[0,1]]  con c_B = [5, 2]  para Rec1 y Demanda
# Recurso2 no activa → dual = 0
# Planteamos: 6·u1 + 0·u3 = 5   y   0·u1 - 1·u3 = 2  → u3=-2 ... usamos
# el método correcto: valores extraídos de la tabla óptima del enunciado
y_R1  =  5/6        # precio sombra Recurso1
y_R2  =  0.0        # precio sombra Recurso2 (holgura > 0)
y_DEM = -4/3        # precio sombra Demanda   (restricción >= activa)

print("=" * 60)
print("  PRECIOS SOMBRA (DUALES)")
print("=" * 60)
print(f"  u_Recurso1  = {y_R1:.6f}")
print(f"  u_Recurso2  = {y_R2:.6f}")
print(f"  u_Demanda   = {y_DEM:.6f}")
print()

# ─── 5. ANÁLISIS DE RANGOS ────────────────────────────────────────
print("=" * 60)
print("  ANÁLISIS DE SENSIBILIDAD")
print("=" * 60)

# --- 5a. Rangos de coeficientes de la función objetivo ---
# Extraídos de la tabla óptima y fórmulas estándar del Simplex
# cj - zj para no básicas debe permanecer <= 0 (max)
# X3 (holgura R1): cj-zj = 0 - (-5/6) = -5/6  → coef reducido de A1 en tabla
# Según tabla óptima: fila Zj-Cj: A1=0, A2=0, A3=5/6, A4=0, A5=4/3

print("\n  OBJ COEFFICIENT RANGES (base sin cambio)")
print(f"  {'Variable':<10} {'Valor actual':>14} {'Incr. permitido':>16} {'Decr. permitida':>16}")
print(f"  {'-'*58}")
# C1 (X1=5): rango [5-2, 5+inf] = [3, inf]
print(f"  {'X1':<10} {'5.000000':>14} {'INFINITY':>16} {'2.000000':>16}")
# C2 (X2=2): rango [2-inf, 2+4/3] = [-inf, 10/3]
print(f"  {'X2':<10} {'2.000000':>14} {'1.333333':>16} {'INFINITY':>16}")

# --- 5b. Rangos del lado derecho (RHS) ---
print("\n  RIGHTHAND SIDE RANGES (base sin cambio)")
print(f"  {'Restricción':<12} {'RHS actual':>12} {'Incr. permitido':>16} {'Decr. permitida':>16}")
print(f"  {'-'*62}")
# R1=240: [240-80, 240+10] = [160, 250]
print(f"  {'RECURSO1':<12} {'240.000000':>12} {'10.000000':>16} {'80.000000':>16}")
# R2=70:  [70-10/3, +inf] = [66.67, inf]
print(f"  {'RECURSO2':<12} {'70.000000':>12} {'INFINITY':>16} {'3.333333':>16}")
# DEM=40: [40-10, 40+20] = [30, 60]
print(f"  {'DEMANDA':<12} {'40.000000':>12} {'20.000000':>16} {'10.000000':>16}")
print()

# ─── 6. ANÁLISIS PREGUNTA b ───────────────────────────────────────
print("=" * 60)
print("  ANÁLISIS PREGUNTA b")
print("  Subsidio $30 por bajar precio X1 de $5 a $2")
print("=" * 60)
print()
print("  El cálculo del enunciado ES INCORRECTO.")
print("  Razón: usa el valor de X1 (13,33 unidades) multiplicado")
print("  por el cambio de precio ($3), lo cual sería válido SOLO")
print("  si la base óptima no cambiara. Pero el rango permitido")
print("  de DISMINUCIÓN del coef. C1 es $2.00, es decir C1 puede")
print("  bajar hasta 5-2 = $3 antes de cambiar de base.")
print()
print("  Bajar C1 de $5 a $2 implica una reducción de $3,")
print("  que EXCEDE el rango permitido ($2). Por lo tanto la base")
print("  CAMBIA y el análisis marginal ya no es válido.")
print()
print("  Se debe resolver el problema con C1=2 para encontrar")
print("  la nueva solución óptima:")

c_b = np.array([-2.0, -2.0])   # nuevo C1=2
res_b = linprog(c_b, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
Z_b = -res_b.fun
print(f"\n  Nueva solución con C1=2: X1={res_b.x[0]:.4f}, X2={res_b.x[1]:.4f}, Z={Z_b:.4f}")
perdida = Z_opt - Z_b
print(f"  Pérdida real en Z: {Z_opt:.4f} - {Z_b:.4f} = ${perdida:.4f}")
print(f"  Subsidio ofrecido: $30")
print(f"  ¿Conviene? {'SÍ' if perdida < 30 else 'NO'} (pérdida ${perdida:.2f} {'<' if perdida<30 else '>'} $30)")
print()

# ─── 7. ANÁLISIS PREGUNTA c ───────────────────────────────────────
print("=" * 60)
print("  ANÁLISIS PREGUNTA c – Tres alternativas (Recurso R1)")
print("=" * 60)
print()
print("  Precio sombra de R1 = $5/6 por unidad")
print()

# Alternativa 1: no modificar
print("  Alt 1 – No modificar")
print(f"    Z = $440/3 = ${440/3:.4f}")
print()

# Alternativa 2: Comprar 120 unidades R1 por $90
# RHS pasa de 240 a 360. Rango permitido aumento = 10 → 240+10=250
# 360 > 250 → fuera del rango, debemos re-resolver
rhs_alt2 = 240 + 120
b_alt2 = np.array([rhs_alt2, 70.0, -40.0])
res_alt2 = linprog(-c_max, A_ub=A_ub, b_ub=b_alt2, bounds=bounds, method='highs')
Z_alt2_bruto = -res_alt2.fun
Z_alt2_neto  = Z_alt2_bruto - 90
print(f"  Alt 2 – Comprar 120 u. R1 por $90")
print(f"    RHS R1 = {rhs_alt2}  (fuera del rango de sensibilidad → re-optimizado)")
print(f"    X1={res_alt2.x[0]:.4f}, X2={res_alt2.x[1]:.4f}")
print(f"    Z bruto = ${Z_alt2_bruto:.4f}  |  Costo compra = $90")
print(f"    Z neto  = ${Z_alt2_neto:.4f}")
print()

# Alternativa 3: Vender 120 unidades R1 por $90
# RHS pasa de 240 a 120. Rango permitido disminución = 80 → 240-80=160
# 120 < 160 → fuera del rango, re-resolver
rhs_alt3 = 240 - 120
b_alt3 = np.array([rhs_alt3, 70.0, -40.0])
res_alt3 = linprog(-c_max, A_ub=A_ub, b_ub=b_alt3, bounds=bounds, method='highs')
print(f"  Alt 3 – Vender 120 u. R1 por $90")
print(f"    RHS R1 = {rhs_alt3}")
if res_alt3.success:
    Z_alt3_bruto = -res_alt3.fun
    Z_alt3_neto  = Z_alt3_bruto + 90
    print(f"    X1={res_alt3.x[0]:.4f}, X2={res_alt3.x[1]:.4f}")
    print(f"    Z bruto = ${Z_alt3_bruto:.4f}  |  Ingreso venta = $90")
    print(f"    Z neto  = ${Z_alt3_neto:.4f}")
else:
    # RHS=120 con demanda X2>=40 y 4*40=160>120 → infactible
    # Recalcular: Demanda activa X2=40, entonces 6X1<=120-160<0 → infactible
    # Nota: con RHS R1=120 y X2>=40: 6X1+4*40<=120 → 6X1<=-40 → infactible
    Z_alt3_bruto = None
    Z_alt3_neto  = None
    print(f"    INFACTIBLE: con X2>=40 se necesita al menos 4*40=160 de R1,")
    print(f"    pero solo quedarían 120 unidades. El problema no tiene solución.")
    print(f"    Z neto  = N/A (infactible)")
print()

alternativas = {
    "No modificar":  440/3,
    "Comprar 120u":  Z_alt2_neto,
}
if Z_alt3_neto is not None:
    alternativas["Vender 120u"] = Z_alt3_neto
else:
    print("  (Alternativa 3 excluida por infactibilidad)")
mejor = max(alternativas, key=alternativas.get)
print(f"\n  ► MEJOR ALTERNATIVA: {mejor}  (Z neto = ${alternativas[mejor]:.4f})")
print()
print("=" * 60)
print("  FIN DEL ANÁLISIS")
print("=" * 60)
