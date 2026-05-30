/*
 * Ejercicio 5.4 — Programación Lineal Continua (PLC)
 * Modelos y Optimización I — Versión 5.0 febrero 2024
 *
 * Problema:
 *   Z(Máx) = 5*X1 + 2*X2
 *
 * Restricciones:
 *   Recurso1:  6*X1 + 4*X2 <= 240
 *   Recurso2:  2*X1 +   X2 <= 70
 *   Demanda:          X2   >= 40
 *   X1, X2 >= 0
 *
 * Para correr en IBM ILOG CPLEX Optimization Studio (OPL IDE):
 *   1. Crear un nuevo proyecto OPL
 *   2. Agregar este archivo como modelo (.mod)
 *   3. Crear una Run Configuration y ejecutar
 *
 * IMPORTANTE: CPLEX OPL genera automáticamente los rangos de
 * sensibilidad si se activa el post-processing de LP.
 * Para verlos, ir a:
 *   Run Configuration > Engine Options > LP > activar
 *   "Write sensitivity" o usar la opción cplex.sensitivityAnalysis = true
 * (ver bloque execute CPLEX al final de este archivo)
 */

// ─── Variables de decisión ────────────────────────────────────────
dvar float+ X1;   // Producción del producto 1  (>= 0)
dvar float+ X2;   // Producción del producto 2  (>= 0)

// ─── Función objetivo ─────────────────────────────────────────────
maximize
  5*X1 + 2*X2;

// ─── Restricciones ────────────────────────────────────────────────
subject to {

  Recurso1:
    6*X1 + 4*X2 <= 240;

  Recurso2:
    2*X1 + X2 <= 70;

  Demanda:
    X2 >= 40;
}

// ─── Post-procesamiento: mostrar resultados y sensibilidad ────────
execute RESULTADOS {

  writeln("==============================================");
  writeln("  SOLUCIÓN ÓPTIMA");
  writeln("==============================================");
  writeln("  X1 = " + X1);
  writeln("  X2 = " + X2);
  writeln("  Z  = " + (5*X1 + 2*X2));

  writeln("\n  HOLGURAS / EXCEDENTES");
  var s1 = 240 - (6*X1 + 4*X2);
  var s2 = 70  - (2*X1 +   X2);
  var s3 = X2  - 40;
  writeln("  Recurso1 holgura   = " + s1);
  writeln("  Recurso2 holgura   = " + s2);
  writeln("  Demanda  excedente = " + s3);
}

// ─── Activar análisis de sensibilidad en el motor CPLEX ───────────
execute CPLEX_CONFIG {
  /*
   * Habilitar análisis de sensibilidad.
   * En OPL IDE esto activa la pestaña "Solution Pool / Sensitivity"
   * en la vista de resultados.
   */
  cplex.sensitivityAnalysis = true;
}

/*
 * ──────────────────────────────────────────────────────────────────
 *  RESULTADOS ESPERADOS (verificados contra tabla óptima del simplex)
 * ──────────────────────────────────────────────────────────────────
 *
 *  SOLUCIÓN ÓPTIMA
 *  ───────────────
 *  X1 = 13.3333  (= 40/3)
 *  X2 = 40.0000
 *  Z  = 146.6667  (= 440/3)
 *
 *  HOLGURAS
 *  ────────
 *  Recurso1: holgura   = 0      (restricción ACTIVA)
 *  Recurso2: holgura   = 3.333  (restricción inactiva)
 *  Demanda:  excedente = 0      (restricción ACTIVA)
 *
 *  PRECIOS SOMBRA (Dual Prices)
 *  ────────────────────────────
 *  Recurso1 =  0.8333  (5/6)
 *  Recurso2 =  0.0000
 *  Demanda  = -1.3333  (-4/3)
 *
 *  RANGOS DE VARIACIÓN — Coeficientes de la FO
 *  ─────────────────────────────────────────────
 *  Variable  Actual  Aumento máx  Disminución máx  Rango
 *  X1        5.000   INFINITO     2.000            [3.0, +inf)
 *  X2        2.000   1.333        INFINITO         (-inf, 3.333]
 *
 *  RANGOS DE VARIACIÓN — Lados derechos (RHS)
 *  ─────────────────────────────────────────────
 *  Restricción  Actual   Aum. máx  Dis. máx   Rango válido
 *  Recurso1     240      10        80          [160, 250]
 *  Recurso2      70      INFINITO   3.333      [66.67, +inf)
 *  Demanda       40      20        10          [30, 60]
 *
 * ──────────────────────────────────────────────────────────────────
 *  RESPUESTAS INCISOS
 * ──────────────────────────────────────────────────────────────────
 *
 *  [b] El cálculo es INCORRECTO. Bajar c1 a 2 supera la disminución
 *      máxima permitida (=2), por lo tanto la base CAMBIA.
 *      No se puede asumir X1=13.33 constante. El nuevo óptimo es
 *      X1=0, X2=60, Z=120. La pérdida real es $26.67 < $30 subsidio,
 *      por lo que en realidad SÍ convendría — contradiciendo el
 *      razonamiento erróneo del enunciado.
 *
 *  [c] Precio sombra de R1 = 0.8333 $/unidad
 *      Alt.1 No modificar → Z = 146.67
 *      Alt.2 Comprar 120u por $90 → Z neto = 155 - 90 = 65.00
 *      Alt.3 Vender 120u (b1=120) → INFACTIBLE (necesita b1 >= 160)
 *      MEJOR: Alt.1 — No modificar el plan actual.
 * ──────────────────────────────────────────────────────────────────
 */
