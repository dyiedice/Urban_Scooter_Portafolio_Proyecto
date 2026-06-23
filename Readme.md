# Urban Scooter - Pruebas Automatizadas

138 tests automatizados para una aplicación web de renta de scooters, 
cubriendo pruebas de API REST, flujos end-to-end y validación de 
formularios con clases de equivalencia y valores límite.

Si quieres ver lo mas relevante, decisiones técnicas y videos 
del funcionamiento, lo documenté aquí: [Notion](https://app.notion.com/p/Urban-Scooter-138-Test-automatizados-382c7da000378052aeb0ef3b5cd074df)

Numero:+52 55 1404 1866
## Tecnologías
- Python, Selenium, Pytest
- Patrón POM
- API REST (POST, PUT, GET)

## Cómo ejecutarlo
El proyecto corre sobre un servidor de TripleTen. Si quieres probarlo, 
escríbeme y te paso los links activos.

1. Actualiza las URLs en `data.py`
2. Instala dependencias: `pip install pytest selenium`
3. Ejecuta el test que necesites: `pytest main.py::nombre_del_test`

## Estructura del proyecto
- `main.py` — casos de prueba
- `data.py` — datos de prueba centralizados
- `searchers.py` — localizadores y funciones de búsqueda en la UI
- `ApiRequests.py` — construcción de solicitudes API
- `helpers.py` — lógica reutilizable que simplifica los tests

