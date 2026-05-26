from mcp.server.fastmcp import FastMCP
from docplex.mp.model import Model

# Crea el servidor MCP
mcp = FastMCP("CPLEX Simplex Solver")

@mcp.tool()
def resolver_simplex(
    variables: list[str],
    coeficientes_objetivo: list[float],
    restricciones: list[dict],
    maximizar: bool = True
) -> dict:
    """
    Resuelve un modelo de programación lineal usando CPLEX
    
    - variables: nombres de las variables ["x1", "x2"]
    - coeficientes_objetivo: coeficientes de la función objetivo [3, 5]
    - restricciones: lista de restricciones, cada una con:
        {"coeficientes": [1, 2], "operador": "<=", "rhs": 10}
    - maximizar: True para maximizar, False para minimizar
    """
    
    # Crea el modelo de CPLEX
    m = Model(name="Simplex")
    
    # Variables
    vars_lp = {v: m.continuous_var(name=v, lb=0) for v in variables}
    
    # Función objetivo
    objetivo = m.sum(coeficientes_objetivo[i] * vars_lp[variables[i]] 
                     for i in range(len(variables)))
    
    if maximizar:
        m.maximize(objetivo)
    else:
        m.minimize(objetivo)
    
    # Restricciones
    for i, r in enumerate(restricciones):
        expr = m.sum(r["coeficientes"][j] * vars_lp[variables[j]] 
                     for j in range(len(variables)))
        if r["operador"] == "<=":
            m.add_constraint(expr <= r["rhs"], f"R{i+1}")
        elif r["operador"] == ">=":
            m.add_constraint(expr >= r["rhs"], f"R{i+1}")
        elif r["operador"] == "==":
            m.add_constraint(expr == r["rhs"], f"R{i+1}")
    
    # Resuelve el modelo con CPLEX
    sol = m.solve(log_output=False)
    
    # Solución
    if sol:
        return {
            "estado": "Óptimo encontrado",
            "valor_objetivo": m.objective_value,
            "variables": {v: vars_lp[v].solution_value for v in variables}
        }
    else:
        return {"estado": "Sin solución", "valor_objetivo": None, "variables": {}}

# Ejecuta el servidor (Claude lo llama cuando necesita resolver un modelo)
if __name__ == "__main__":
    mcp.run(transport="stdio")