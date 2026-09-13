# JARVIS v1.4 — Web Search

Añade una capa desacoplada para búsquedas web.

## Objetivos
- Recibir consultas de texto.
- Limitar el número de resultados.
- Mantener la búsqueda separada del núcleo del asistente.
- No ejecutar código ni acciones provenientes de páginas web.

La clase `WebSearch` es una interfaz preparada para conectar un proveedor de búsqueda real sin acoplar JARVIS a un servicio concreto.
