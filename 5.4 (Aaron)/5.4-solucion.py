"""
Ejercicio 5.4 - Programación Lineal Continua
Modelos y Optimización I

Problema:
    Z (Máx) = 5*X1 + 2*X2
    Sujeto a:
        Recurso1:  6*X1 + 4*X2 <= 240
        Recurso2:  2*X1 +   X2 <= 70
        Demanda:          X2   >= 40
        X1, X2 >= 0
"""

from scipy.optimize import linprog
import numpy as np

SEP = "=" * 60

# ─────────────────────────────────────────────
# 1. SOLUCIÓN ÓPTIMA con scipy.optimize.linprog
# ─────────────────────────────────────────────
c_obj = [-5, -2]   # Maximizar → Minimizar negativo

A_ub = [[ 6,  4],
        [ 2,  1],
        [ 0, -1]]   # -X2 <= -40  ≡  X2 >= 40
b_ub = [240, 70, -40]
x_bounds = [(0, None), (0, None)]

res = linprog(c_obj, A_ub=A_ub, b_ub=b_ub, bounds=x_bounds, method='highs')

X1_opt = res.x[0]
X2_opt = res.x[1]
Z_opt  = -res.fun

print(SEP)
print("  EJERCICIO 5.4 — Programación Lineal (PLC)")
print("  Z(Máx) = 5·X1 + 2·X2")
print(SEP)

print("\n[1] SOLUCIÓN ÓPTIMA")
print(f"   X1 = {X1_opt:.6f}  (= 40/3)")
print(f"   X2 = {X2_opt:.6f}")
print(f"   Z  = {Z_opt:.6f}  (= 440/3)")

s1 = 240 - (6*X1_opt + 4*X2_opt)
s2 =  70 - (2*X1_opt +   X2_opt)
s3 = X2_opt - 40

print("\n[2] HOLGURAS / EXCEDENTES")
print(f"   Recurso1 (<=): holgura   = {s1:.6f}  → restricción ACTIVA")
print(f"   Recurso2 (<=): holgura   = {s2:.6f}  → restricción inactiva")
print(f"   Demanda  (>=): excedente = {s3:.6f}  → restricción ACTIVA")

duals = -res.ineqlin.marginals
print("\n[3] PRECIOS SOMBRA (Dual Prices / Valores Marginales)")
print(f"   Recurso1: {duals[0]:.6f}  → cada unidad adicional de R1 agrega $0.8333 a Z")
print(f"   Recurso2: {duals[1]:.6f}  → recurso no limitante (holgura > 0)")
print(f"   Demanda:  {duals[2]:.6f}  → el mínimo de X2 penaliza Z en $1.3333/u")

# ─────────────────────────────────────────────
# 2. RANGOS DE VARIACIÓN
# ─────────────────────────────────────────────
print("\n" + SEP)
print("  RANGOS DE VARIACIÓN — Base sin cambios")
print(SEP)

print("""
  OBJ COEFFICIENT RANGES
  ┌────────────┬──────────────┬───────────────┬──────────────────┐
  │  Variable  │ Coef actual  │  Aumento máx  │  Disminución máx │
  ├────────────┼──────────────┼───────────────┼──────────────────┤
  │     X1     │   5.000000   │    INFINITO   │     2.000000     │
  │     X2     │   2.000000   │    1.333333   │     INFINITO     │
  └────────────┴──────────────┴───────────────┴──────────────────┘
  Rango de c1: [3.0, +∞)    Rango de c2: (-∞, 3.333]

  RIGHT-HAND SIDE RANGES
  ┌─────────────┬─────────────┬───────────────┬──────────────────┐
  │ Restricción │  RHS actual │  Aumento máx  │  Disminución máx │
  ├─────────────┼─────────────┼───────────────┼──────────────────┤
  │  RECURSO1   │   240.000   │    10.000     │     80.000       │
  │  RECURSO2   │    70.000   │   INFINITO    │      3.333       │
  │  DEMANDA    │    40.000   │    20.000     │     10.000       │
  └─────────────┴─────────────┴───────────────┴──────────────────┘
  Rango b1 ∈ [160, 250]   b2 ∈ [66.67, +∞)   b3 ∈ [30, 60]
""")

# ─────────────────────────────────────────────
# 3. INCISO b — Subsidio
# ─────────────────────────────────────────────
print(SEP)
print("  INCISO b — Subsidio $30 para bajar c1 de 5 a 2")
print(SEP)
print("""
  El cálculo propuesto es INCORRECTO.

  Razonamiento del enunciado: "pierdo 13.33 × 3 = $40 > $30 → no conviene."
  Esto supone que X1 sigue siendo 13.33, pero ESO NO ES VÁLIDO.

  Del análisis de sensibilidad:
    • La base actual es óptima solo si c1 ∈ [3.0, +∞).
    • Bajar c1 a 2 viola ese rango → la BASE CAMBIA.
    • Con c1 = 2 el nuevo óptimo es diferente (X1 ya no vale lo mismo).
""")

c_b = [-2, -2]
res_b = linprog(c_b, A_ub=A_ub, b_ub=b_ub, bounds=x_bounds, method='highs')
X1_b, X2_b = res_b.x
Z_b = -res_b.fun
perdida_real = Z_opt - Z_b

print(f"  Nuevo óptimo con c1=2:")
print(f"    X1 = {X1_b:.4f},  X2 = {X2_b:.4f},  Z = {Z_b:.4f}")
print(f"  Z original = {Z_opt:.4f}")
print(f"  Pérdida real en Z = {perdida_real:.4f}")
if perdida_real > 30:
    print(f"  Pérdida ({perdida_real:.2f}) > subsidio (30) → NO conviene aceptar.")
    print("  La CONCLUSIÓN final coincide, pero el RAZONAMIENTO es incorrecto.")
else:
    print(f"  Pérdida ({perdida_real:.2f}) < subsidio (30) → Convendría aceptar.")

# ─────────────────────────────────────────────
# 4. INCISO c — Tres alternativas sobre R1
# ─────────────────────────────────────────────
print("\n" + SEP)
print("  INCISO c — Alternativas sobre Recurso1 (120 unidades a $90)")
print(SEP)
print(f"\n  Precio sombra de R1 = 5/6 ≈ 0.8333  |  Rango b1: [160, 250]")

# Alt 1: No modificar
print(f"\n  Alt. 1 — No modificar plan actual")
print(f"    X1={X1_opt:.4f}, X2={X2_opt:.4f}, Z={Z_opt:.4f}")

# Alt 2: Comprar 120 u de R1 por $90  → b1 = 240+120 = 360 (fuera de rango → recalcular)
res_c2 = linprog([-5,-2],
                 A_ub=[[6,4],[2,1],[0,-1]], b_ub=[360,70,-40],
                 bounds=x_bounds, method='highs')
Z_c2_bruto = -res_c2.fun
Z_c2_neto  = Z_c2_bruto - 90

print(f"\n  Alt. 2 — Comprar 120u R1 por $90  (b1 sube de 240 a 360)")
print(f"    Nuevo plan: X1={res_c2.x[0]:.4f}, X2={res_c2.x[1]:.4f}")
print(f"    Z bruto = {Z_c2_bruto:.4f}  |  Costo R1 = $90  |  Z neto = {Z_c2_neto:.4f}")

# Alt 3: Vender 120 u de R1 por $90  → b1 = 240-120 = 120
# Con b1=120 la región factible se reduce; verificamos factibilidad
res_c3 = linprog([-5,-2],
                 A_ub=[[6,4],[2,1],[0,-1]], b_ub=[120,70,-40],
                 bounds=x_bounds, method='highs')

print(f"\n  Alt. 3 — Vender 120u R1 por $90  (b1 bajaría de 240 a 120)")
if not res_c3.success:
    print(f"    ⚠️  INFACTIBLE: con b1=120 no es posible cumplir X2≥40")
    print(f"       (requiere al menos 6·0 + 4·40 = 160 unidades de R1)")
    print(f"       Esta alternativa no es viable.")
    Z_c3_neto = float('-inf')
else:
    Z_c3_bruto = -res_c3.fun
    Z_c3_neto  = Z_c3_bruto + 90
    print(f"    Nuevo plan: X1={res_c3.x[0]:.4f}, X2={res_c3.x[1]:.4f}")
    print(f"    Z bruto = {Z_c3_bruto:.4f}  |  Ingreso R1 = $90  |  Z neto = {Z_c3_neto:.4f}")

# Conclusión
print("\n  ── COMPARATIVO ──────────────────────────────")
print(f"  Alt.1 No modificar   → Z neto = {Z_opt:.4f}")
print(f"  Alt.2 Comprar R1     → Z neto = {Z_c2_neto:.4f}")
print(f"  Alt.3 Vender R1      → INFACTIBLE")
print()
if Z_opt >= Z_c2_neto:
    print("  ✅ Mejor: No modificar el plan actual.")
else:
    print("  ✅ Mejor: Comprar las 120 unidades de R1.")

print("\n" + SEP)
print("  FIN DEL ANÁLISIS")
print(SEP)