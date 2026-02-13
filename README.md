# Prueba Técnica Python

## Descripción

Este proyecto pretende cumplir con los requerimientos del documento de **prueba técnica Python**.

- La carpeta **data** contiene el archivo CSV original proporcionado, así como los archivos resultantes del proceso de extracción y transformación.
- La carpeta **db_ETL** se corresponde con las secciones **1.1 a 1.3** del documento de requerimientos.
- La carpeta **db_normalized** se corresponde con las secciones **1.4 y 1.5**.
- En las carpetas **db_ETL** y **db_normalized** se incluyen _Jupyter Notebooks_ utilizados durante el desarrollo:
  - `.ipynb`: proceso de desarrollo
  - `.html`: documentación y visualización sin dependencias
  - El archivo que debe ejecutarse es el de extensión `.py`
- La carpeta **api** se corresponde con la **sección 2** del documento.

---

## Estructura del proyecto

```
prueba-t-cnica/
├── api/
│   ├── main.py
│   └── missing_number.py
├── data/
│   ├── data_prueba_tecnica_extracted.csv
│   ├── data_prueba_técnica.csv
│   └── data_prueba_tecnica_transformed.csv
├── db_ETL/
│   ├── ETL-process.py
│   ├── docker-compose.yml
│   └── init.sql
├── db_normalized/
│   ├── Normalización.pdf
│   ├── docker-compose.yml
│   ├── init.sql
│   ├── normalization-process.py
│   └── vw_total_amount.sql
└── requirements.txt
```

---

## Creación del ambiente

Este proyecto utiliza **Python** y **Docker**.

1. Crear un ambiente virtual:

   ```bash
   python -m venv venv
   ```

2. Activar el ambiente:

   ```bash
   source venv/bin/activate
   ```

3. Verificar que el ambiente esté activo:

   ```bash
   which python
   ```

4. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

## Carpeta `db_ETL`

- Es posible abrir en el navegador el archivo **ETL-process.html** para conocer detalles del proceso de desarrollo.
- Ejecutar el contenedor de la base de datos:

  ```bash
  docker compose up --build
  ```

- Ejecutar el programa ETL:

  ```bash
  python ETL-process.py
  ```

- Comprobar los cambios en la base de datos:

  ```bash
  docker exec -it mysql-transacciones mysql -u appuser -p transacciones_db
  ```

  **Credenciales MySQL**
  - Usuario: `appuser`
  - Contraseña: `apppass`
  - Puerto: `3306`

---

## Carpeta `db_normalized`

- Es posible abrir en el navegador el archivo **normalization-process.html** para conocer detalles del proceso de desarrollo.
- Ejecutar el contenedor de la base de datos:

  ```bash
  docker compose up --build
  ```

- Ejecutar el programa de normalización:

  ```bash
  python normalization-process.py
  ```

- Comprobar los cambios en la base de datos:

  ```bash
  docker exec -it mysql-transacciones-n mysql -u appuser -p transacciones_db
  ```

  **Credenciales MySQL**
  - Usuario: `appuser`
  - Contraseña: `apppass`
  - Puerto: `3307`

- Desde la CLI de MySQL se puede probar la **vista** definida en `vw_total_amount.sql`.

---

## Carpeta `api`

- Ejecutar la API:

  ```bash
  uvicorn main:app --host 0.0.0.0 --port 8000
  ```

- Verificar que la API esté corriendo desde el navegador:

  ```
  http://localhost:8000/
  ```

- Interactuar con la API usando Swagger:

  ```
  http://localhost:8000/docs
  ```

---

## Notas finales

- El proyecto está diseñado para ser reproducible usando Docker.
- La lógica de negocio está desacoplada de la capa de API.
- Los notebooks se incluyen como evidencia del proceso de desarrollo y documentación técnica.
