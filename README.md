# Api Destinatarios

Backend REST (FastAPI) para el sistema extractor OCR de destinatarios. Expone autenticación JWT, registros, usuarios, envíos Paquetexpress y consulta de coberturas por código postal. El cliente principal es una app de escritorio (PySide6).

## Requisitos

- Python 3.11+
- MySQL 8
- Git

## 1. Entorno virtual

```bash
python -m venv .venv
```

En Cursor: `Ctrl+Shift+P` → **Python: Select Interpreter** → elige:

```text
...\Api_Destinatarios\.venv\Scripts\python.exe
```

Activa el entorno e instala dependencias:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
instalar las siguientes librerias con pip install:
 * fastapi → Framework de la API
 * uvicorn → Servidor ASGI (ejecución)
 * sqlalchemy → ORM
 * alembic → Migraciones de base de datos
 * mysql-connector-python → Driver MySQL
 * python-dotenv → Variables de entorno (.env)
 * passlib[bcrypt] → Hash seguro de contraseñas
 * python-jose → JWT (access + refresh tokens)
 * pydantic → Validación de datos (v2, usado en schemas)
 * pytest → Tests (con SQLite en entorno de pruebas)


## 2. Base de datos

Crea la base `ocr_destinatarios` y un usuario (por ejemplo `dev`) con su password.

## 3. Variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
ENV=development
DATABASE_URI=mysql+mysqlconnector://usuario:password@localhost:3306/ocr_destinatarios
JWT_SECRET_KEY=cambia-esta-clave
JWT_ALGORITHM=HS256
JWT_EXP_MINUTES=60
```

`DATABASE_URI` es la cadena que usa SQLAlchemy. No uses `DB_HOST` / `DB_USER` por separado.

Verifica la conexión ejecutando `app/db/database.py`.

## 4. Migraciones

Genera las tablas:

```bash
alembic upgrade head
```

Para una nueva migración:

```bash
alembic revision --autogenerate -m "descripcion del cambio"
alembic upgrade head
```

## 5. Crear usuario

Desde la raíz del proyecto, con el venv activado:

```bash
python scripts/create_user.py
```

## 6. Levantar el servidor

```bash
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs

Los tiempos de cada petición se registran en `logs/requests.log`.

## Endpoints

Todas las rutas (salvo login y `/`) requieren `Authorization: Bearer <token>`.

| Método | Ruta | Descripción |
| --- | --- | --- |
| POST | `/auth/login` | Login (email + password) → access token |
| GET | `/users/` | Listar usuarios |
| GET | `/users/{user_id}` | Consultar usuario (solo el propio) |
| POST | `/users/` | Crear usuario (restringido) |
| GET | `/registros/` | Listar registros (filtros: sede, fechas) |
| POST | `/registros/` | Crear registro |
| PUT | `/registros/{registro_id}` | Actualizar registro |
| GET | `/shipments-px/` | Listar envíos (filtro por fechas) |
| POST | `/shipments-px/` | Crear envío |
| GET | `/shipments-px/{folio}` | Consultar envío por folio |
| PUT | `/shipments-px/{id_shipping}` | Actualizar envío |
| GET | `/coverages/?cp=01000` | Coberturas Paquetexpress por código postal |

La app de escritorio no está sujeta a CORS.

## Renovación mensual de `coverages_px`

`coverages_px` es un catálogo de coberturas (sucursal, plaza, CP, colonia, municipio, ciudad, estado y tipo). Se consulta por código postal y **no** tiene claves foráneas. Cada mes se reemplaza el contenido completo.

Para vaciar la tabla y reiniciar el `id_delivery` desde 1:

```sql
TRUNCATE TABLE coverages_px;
```

`TRUNCATE` no borra fila por fila: libera los datos de golpe y reinicia el `AUTO_INCREMENT`. Con cientos de miles de registros suele tardar segundos. `DELETE FROM` sí recorre cada fila y **no** reinicia el contador.

Después del `TRUNCATE`, carga el archivo nuevo (ejemplo CSV):

```sql
LOAD DATA LOCAL INFILE 'coverages_mes.csv'
INTO TABLE coverages_px
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(branch, place, postal_code, colony, municipality, city, state, coverage_type);
```

Valores válidos de `coverage_type`:

- `PAQUETEXPRESS`
- `ZONA PLUS`
- `ZONA PLUS ESPECIAL`

Si hace falta que `/coverages` no se quede vacío durante la carga, usa una tabla temporal y un rename atómico:

```sql
CREATE TABLE coverages_px_new LIKE coverages_px;
-- cargar el archivo en coverages_px_new
RENAME TABLE coverages_px TO coverages_px_old,
             coverages_px_new TO coverages_px;
DROP TABLE coverages_px_old;
```

### Próximo paso: importar desde la app de escritorio

`LOAD DATA` sirve para una carga manual en MySQL. El flujo objetivo es un endpoint (`POST /coverages/import`) que reciba el archivo por multipart, lo normalice/valide en la API y recargue la tabla, para que el cliente PySide6 lo envíe con el token JWT. Aún no está implementado.
