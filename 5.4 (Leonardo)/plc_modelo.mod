/*
 =====================================================================
  MODELO OPL – IBM ILOG CPLEX Optimization Studio
  Problema de Programación Lineal (PLC)

  Maximizar  Z = 5·X1 + 2·X2
  Sujeto a:
    Recurso1:  6·X1 + 4·X2 <= 240
    Recurso2:  2·X1 +   X2 <=  70
    Demanda:          X2  >=  40
    X1, X2 >= 0
 =====================================================================
  Para obtener los rangos de sensibilidad en CPLEX IDE:
    Run > Run Configuration > solveType = Continuous (LP relax)
    Luego acceder a: Engine > Solution > Sensitivity Analysis
    O usar cplex.writeSensitivity("sensitivity.txt") en el script
 =====================================================================
*/

// ─── VARIABLES DE DECISIÓN ───────────────────────────────────────
dvar float+ X1;   // Unidades producidas del Producto 1
dvar float+ X2;   // Unidades producidas del Producto 2

// ─── FUNCIÓN OBJETIVO ────────────────────────────────────────────
maximize
  5 * X1 + 2 * X2;

// ─── RESTRICCIONES ───────────────────────────────────────────────
subject to {

  ct_Recurso1:
    6 * X1 + 4 * X2 <= 240;   // Disponibilidad Recurso 1

  ct_Recurso2:
    2 * X1 + X2 <= 70;        // Disponibilidad Recurso 2

  ct_Demanda:
    X2 >= 40;                  // Demanda mínima del Producto 2
}

// ─── SCRIPT DE POST-PROCESAMIENTO ────────────────────────────────
execute POST_ANALYSIS {
  writeln("==========================================================");
  writeln("  SOLUCIÓN ÓPTIMA");
  writeln("==========================================================");
  writeln("  X1 = " + X1);
  writeln("  X2 = " + X2);
  writeln("  Z  = " + (5*X1 + 2*X2));
  writeln();

  writeln("==========================================================");
  writeln("  HOLGURAS / EXCEDENTES");
  writeln("==========================================================");
  var hR1 = 240 - (6*X1 + 4*X2);
  var hR2 = 70  - (2*X1 +   X2);
  var eD  = X2  - 40;
  writeln("  Recurso1 holgura  = " + hR1 + (hR1 < 0.0001 ? "  (ACTIVA)" : "  (no activa)"));
  writeln("  Recurso2 holgura  = " + hR2 + (hR2 < 0.0001 ? "  (ACTIVA)" : "  (no activa)"));
  writeln("  Demanda  excedent = " + eD  + (eD  < 0.0001 ? "  (ACTIVA)" : "  (no activa)"));
  writeln();

  writeln("==========================================================");
  writeln("  PRECIOS SOMBRA (de la tabla óptima Simplex)");
  writeln("==========================================================");
  writeln("  u_Recurso1 =  0.8333  (5/6)");
  writeln("  u_Recurso2 =  0.0000  (restricción inactiva)");
  writeln("  u_Demanda  = -1.3333  (-4/3)");
  writeln();

  writeln("==========================================================");
  writeln("  RANGOS DE COEF. OBJETIVO (base sin cambio)");
  writeln("==========================================================");
  writeln("  X1: C1 actual = 5.00  |  Puede AUMENTAR: INFINITY  |  Puede DISMINUIR: 2.00  → Rango: [3, +inf)");
  writeln("  X2: C2 actual = 2.00  |  Puede AUMENTAR: 1.3333    |  Puede DISMINUIR: INFINITY → Rango: (-inf, 3.333]");
  writeln();

  writeln("==========================================================");
  writeln("  RANGOS DEL LADO DERECHO – RHS (base sin cambio)");
  writeln("==========================================================");
  writeln("  Recurso1: RHS=240  Aumento perm=10    Dismin perm=80     → Rango: [160, 250]");
  writeln("  Recurso2: RHS= 70  Aumento perm=INF   Dismin perm=3.333  → Rango: [66.67, +inf)");
  writeln("  Demanda:  RHS= 40  Aumento perm=20    Dismin perm=10     → Rango: [30, 60]");
  writeln();

  writeln("==========================================================");
  writeln("  ANÁLISIS PREGUNTA b – Subsidio $30 para C1: $5 → $2");
  writeln("==========================================================");
  writeln("  El cálculo del enunciado (13.33 x $3 = $40 de pérdida) ES INCORRECTO.");
  writeln("  La reducción de $3 EXCEDE el rango permitido ($2), cambia la base.");
  writeln("  Con C1=2 la nueva óptima es: X1=0, X2=60, Z=120.");
  writeln("  Pérdida real = 146.67 - 120 = $26.67 < $30 subsidio → CONVIENE ACEPTAR.");
  writeln();

  writeln("==========================================================");
  writeln("  ANÁLISIS PREGUNTA c – Tres alternativas sobre R1");
  writeln("==========================================================");
  writeln("  Alt 1 – No modificar:            Z neto = $146.67");
  writeln("  Alt 2 – Comprar 120u R1 por $90: Z neto =  $65.00  (RHS=360, re-optimizado)");
  writeln("  Alt 3 – Vender 120u R1 por $90:  INFACTIBLE (quedan 120u < demanda mínima 160u)");
  writeln();
  writeln("  ► MEJOR ALTERNATIVA: No modificar  (Z = $146.67)");
  writeln("==========================================================");
}
