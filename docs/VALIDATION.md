# Verificación · EquineLead

Fecha: 7 de octubre de 2026 (Ecuador). Entorno local Python 3.12.14. Las dependencias de QA se registran aparte; esta comprobación no certifica todas las combinaciones de versiones del proyecto.

## Ejecutado

Arranque sin credenciales comprobado: presenta las instrucciones de configuración, sin excepción. Tres pruebas de rutas y lectura Parquet aprobadas: reconoce la salida DVC, prioriza una carpeta completa y respeta una ruta explícita.

## Dependencias externas y límites

Necesita los cinco Parquet originales en data/clean o app/data/clean, o acceso DVC/GCP (EQUINE_DATA_DIR permite otra ruta). Sin ellos muestra instrucciones; no sustituye los datos por un conjunto ficticio.

No se reentrenaron los modelos ni se validó la API remota, GCP, DagsHub o la descarga DVC. Las sesiones se limitan a 10.000 filas por tabla en la vista inicial.

## Presentación Power BI

Las definiciones se revisaron para límites y superposiciones, y el diseño móvil sigue el esquema oficial PBIR. La prueba nativa completa en teléfono permanece pendiente. Las fuentes externas deben exportarse antes de actualizar las páginas sin datos.
