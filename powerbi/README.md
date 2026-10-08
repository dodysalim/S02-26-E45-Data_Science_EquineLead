# EquineLead Analytics — Power BI

PENDIENTE DE DATOS · archivos Parquet de DVC/GCP ausentes · ninguna métrica usa mock data

## Abrir

1. Descarga el repositorio completo.
2. Ejecuta `python powerbi/configure_data.py`. Alternativamente, en Transformar datos → Administrar parámetros cambia `DataFolder` a la carpeta `powerbi/data/` con separador final.
3. Abre `powerbi/Analytics.pbip` en Power BI Desktop y pulsa Actualizar.

## Estructura y correspondencia

Secciones equivalentes: resumen, audiencia, conversión, caballos, retail e IA. Las visualizaciones están preparadas y vacías hasta obtener Parquet. IA permanece en la API/Streamlit. No se usa `generate_mock_data`.

Ejecuta `dvc pull` según la configuración del proyecto, luego `python powerbi/export_data.py`. Se busca `app/data/clean`, igual que el cargador del dashboard; también admite `data/clean` para repositorios con la carpeta en la raíz.

Las páginas conservan el análisis del proyecto original. Los controles de entrenamiento, conexión, escritura SQL e inferencia en vivo siguen en Python/Streamlit. El informe consume resultados exportados; no reemplaza esos servicios. Los CSV conservan su grano, y las medidas evitan sumar porcentajes o promedios.

## Verificación de esta entrega

El serializador TMDL nativo instalado con Power BI Desktop aceptó el modelo. Se comprobaron las referencias de los campos y los límites de cada visual. Esto valida la estructura; la apertura, actualización y representación de los gráficos se comprueban por separado. Los proyectos sin datos siguen pendientes.
