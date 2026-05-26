# Modelos y Optimización I - TP

Instalar `cplex_studio2211` de la página de IBM (utilizando el email FIUBA).

Instalar dependencias: `pip install cplex docplex mcp`

CPLEX es el software de IBM para optimización lineal.  
MCP (Model Context Protocol) es el sistema que usa Claude para conectarse con herramientas externas.

Servidor MCP local en Python que conecta CPLEX con Claude: `servidor.py`

Archivo de configuración JSON que le indica a Claude dónde está el servidor MCP (reemplazarlo en AppData\Local\Packages\Claude_\<hash>\LocalCache\Roaming\Claude): `claude_desktop_config.json`

En Claude Desktop -> Archivo, Configuración, Desarrollador, aparece cplex ahora como herramienta.

Pedirle a Claude directamente que resuelva un modelo lineal usando el método simplex cargado.