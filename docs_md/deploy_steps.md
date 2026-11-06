# Actualizar la API en el VPS Hostinger

Guía para subir código nuevo a producción **sin redesplegar todo**. DNS, SSL, LiteSpeed, NGINX, MariaDB, el venv y el servicio systemd `fastapi-backend` ya existen.

Dominio: `tools.feuh.com.mx`

Arquitectura:

```text
Internet
    ↓
tools.feuh.com.mx
    ↓
LiteSpeed (443 SSL)
    ↓
NGINX (127.0.0.1:8080)
    ↓
FastAPI / Uvicorn (127.0.0.1:8000)
    ↓
MariaDB
```

Rutas en el VPS:

| Qué | Ruta |
| --- | --- |
| Proyecto | `/home/freido/apps/fastapi-backend/Api_Destinatarios` |
| Entorno virtual | `/home/freido/apps/venvs/fastapi-backend` |
| Servicio systemd | `/etc/systemd/system/fastapi-backend.service` |
| `.env` de producción | `/home/freido/apps/fastapi-backend/Api_Destinatarios/.env` |

## Qué no hay que repetir

No hace falta: `apt update`, crear el venv, clonar de cero, instalar NGINX, configurar OpenLiteSpeed, emitir SSL, tocar DNS ni rehacer el archivo `.service`.

## Diferencias de este código respecto al despliegue original

1. El código lee `DATABASE_URI`, no `DB_HOST` / `DB_USER` / `DB_PASSWORD`.
2. Hay migraciones nuevas (`coverages_px`, `shipments_px`, `email` en `users`, etc.).
3. El login es por `email`, no por `username`.
4. **No subir el `.env` local a GitHub** (credenciales de desarrollo).

---

## Paso 1 — Subir el código a GitHub (`main`)

**Por qué:** el VPS solo puede `git pull` lo que esté en el remoto. Hasta que no esté en `main`, producción sigue con el código viejo.

En la PC, en la carpeta del proyecto:

```powershell
git status
git branch
git remote -v
```

Confirma que estás en `main` (o la rama que use el VPS) y que el remoto es el repo correcto.

```powershell
git add .
git status
```

Revisa que **no** aparezca `.env`. Si aparece:

```powershell
git restore --staged .env
```

```powershell
git commit -m "Actualiza API: nueva estructura, coverages y shipments PX"
git push origin main
```

No copies el `.env` local al VPS. El de producción ya existe y se ajusta en el paso 4.

---

## Paso 2 — SSH al VPS y detener el servicio

**Por qué:** si la API sigue corriendo durante `git pull` y migraciones, puede servir código a medias o chocar con cambios en las tablas.

Desde PowerShell:

```powershell
ssh freido@195.35.14.26
```

Usa la IP/usuario de Hostinger si cambian. Comprueba e inicia la detención:

```bash
sudo systemctl status fastapi-backend
sudo systemctl stop fastapi-backend
sudo systemctl status fastapi-backend
```

Lo esperado al final: `inactive (dead)`.

```bash
curl http://127.0.0.1:8000
```

Lo esperado: `Connection refused` (la API está apagada a propósito).

Usa `stop`, no `restart`. El arranque es el paso 8.

---

## Paso 3 — Actualizar el código (`git pull`)

**Por qué:** trae el código de `main` sin tocar DNS, SSL ni systemd.

```bash
cd ~/apps/fastapi-backend/Api_Destinatarios
pwd
git status
git branch
```

`pwd` debe ser `/home/freido/apps/fastapi-backend/Api_Destinatarios`. Si hay archivos modificados que git no ignora, no hagas pull hasta resolverlos.

```bash
git pull origin main
```

Si la rama es `master`: `git pull origin master`.

Confirma archivos nuevos y que el `.env` **sigue ahí**:

```bash
ls app/routers/
ls alembic/versions/
ls -la .env
```

---

## Paso 4 — Actualizar el `.env` del VPS

**Por qué:** el código nuevo no lee `DB_HOST`, `DB_USER`, etc. Lee `DATABASE_URI`. Sin eso, FastAPI y Alembic no conectan a MariaDB. El `.env` no se actualiza con `git pull` (está ignorado).

```bash
cd ~/apps/fastapi-backend/Api_Destinatarios
nano .env
```

**No cambies** `JWT_SECRET_KEY` (invalidaría sesiones).

Agrega `DATABASE_URI` con los mismos usuario, password, host, puerto y base que ya tenía el archivo:

```env
ENV=production

DATABASE_URI=mysql+pymysql://USUARIO:PASSWORD@127.0.0.1:3306/tools_OCR

JWT_SECRET_KEY=el_mismo_que_ya_tenias
JWT_ALGORITHM=HS256
JWT_EXP_MINUTES=30
```

Usa `mysql+pymysql://` (driver ya instalado en el VPS). Las variables `DB_*` viejas se pueden dejar; el código las ignora. `ACCESS_TOKEN_EXPIRE_MINUTES` ya no se usa; el código lee `JWT_EXP_MINUTES`.

Si la contraseña tiene `#`, `$`, `@`, `%` o espacios, pon la URI entre comillas. `@` en el password hay que codificarlo como `%40`.

Guarda en nano: `Ctrl+O`, Enter, `Ctrl+X`.

```bash
chmod 600 .env
ls -l .env
```

Debe verse `-rw-------` y dueño `freido`.

Comprueba sin mostrar la password:

```bash
grep -E '^(ENV|DATABASE_URI|JWT_)' .env | sed 's/:.*@/:***@/'
```

---

## Paso 5 — Activar el venv e instalar dependencias

**Por qué:** el código nuevo puede traer paquetes que el venv aún no tiene. Sin ellos la API falla al arrancar.

```bash
cd ~/apps/fastapi-backend/Api_Destinatarios
source ~/apps/venvs/fastapi-backend/bin/activate
which python
which pip
```

Deben apuntar a `/home/freido/apps/venvs/fastapi-backend/bin/...`.

```bash
pip install -r requirements.txt
which uvicorn
```

`uvicorn` debe ser el del venv (el mismo de `ExecStart` en systemd).

---

## Paso 6 — Aplicar migraciones (Alembic)

**Por qué:** el código espera tablas/columnas nuevas. Sin `upgrade`, esas rutas fallan.

Con el venv activado:

```bash
cd ~/apps/fastapi-backend/Api_Destinatarios
alembic current
alembic upgrade head
alembic current
alembic heads
```

`current` y `heads` deben coincidir. Head esperado de esta versión: `d4efccb680d6`.

Si hay error de conexión, revisa `DATABASE_URI` y no arranques la API.

### Si falla `Data truncated` (caso `contacto`)

La migración `9f04f5143a93` recorta `contacto` de `VARCHAR(255)` a `VARCHAR(150)`. MariaDB no corta textos más largos.

MariaDB **no deshace** los `ALTER` anteriores. Alembic puede quedarse en `8acedd05a0d4` aunque ya existan `nombre_titulo` y `numero_volante`. **No vuelvas a correr `alembic upgrade head`** hasta completar lo de abajo: reintentaría renombrar columnas que ya no existen.

Diagnóstico:

```bash
mysql -u TU_USUARIO -p tools_OCR
```

```sql
SELECT version_num FROM alembic_version;
SHOW COLUMNS FROM registros_destinatarios;

SELECT id, CHAR_LENGTH(contacto) AS len, contacto
FROM registros_destinatarios
WHERE CHAR_LENGTH(contacto) > 150;

SELECT COUNT(*) AS indicaciones_largas
FROM registros_destinatarios
WHERE CHAR_LENGTH(indicaciones) > 200;

SELECT COUNT(*) AS observaciones_largas
FROM registros_destinatarios
WHERE CHAR_LENGTH(observaciones_ia) > 100;

SELECT COUNT(*) AS crops_null
FROM registros_destinatarios
WHERE crop_x IS NULL OR crop_y IS NULL OR crop_w IS NULL OR crop_h IS NULL;
```

Ajustar el `contacto` largo (sustituye `EL_ID`):

```sql
UPDATE registros_destinatarios
SET contacto = LEFT(contacto, 150)
WHERE id = EL_ID;
```

Si hace falta recortar otros campos:

```sql
UPDATE registros_destinatarios
SET indicaciones = LEFT(indicaciones, 200)
WHERE CHAR_LENGTH(indicaciones) > 200;

UPDATE registros_destinatarios
SET observaciones_ia = LEFT(observaciones_ia, 100)
WHERE CHAR_LENGTH(observaciones_ia) > 100;
```

Si `nombre_titulo` y `numero_volante` **ya existen**, termina a mano lo que Alembic no llegó a hacer. Si `users.email` ya existe, salta el `ADD COLUMN` y el `CREATE INDEX`:

```sql
ALTER TABLE registros_destinatarios MODIFY contacto VARCHAR(150) NULL;
ALTER TABLE registros_destinatarios MODIFY indicaciones VARCHAR(200) NULL;
ALTER TABLE registros_destinatarios MODIFY observaciones_ia VARCHAR(100) NULL;
ALTER TABLE registros_destinatarios MODIFY crop_x INTEGER NOT NULL;
ALTER TABLE registros_destinatarios MODIFY crop_y INTEGER NOT NULL;
ALTER TABLE registros_destinatarios MODIFY crop_w INTEGER NOT NULL;
ALTER TABLE registros_destinatarios MODIFY crop_h INTEGER NOT NULL;

ALTER TABLE users ADD COLUMN email VARCHAR(150) NULL;
CREATE UNIQUE INDEX ix_users_email ON users (email);
```

Sal de mysql y marca esa revisión (sin reejecutarla):

```bash
alembic stamp 9f04f5143a93
alembic current
alembic upgrade head
alembic current
```

`stamp` le dice a Alembic que esa revisión ya está aplicada. Después `upgrade head` aplica las siguientes hasta `d4efccb680d6`.

---

## Paso 7 — Poner `email` a los usuarios existentes

**Por qué:** `/auth/login` busca por `email`. Los usuarios viejos pueden tener `email` en `NULL` y el login responderá 401.

```sql
SELECT id, username, email, is_active FROM users;

UPDATE users
SET email = 'el_correo@tudominio.com'
WHERE id = EL_ID;

SELECT id, username, email, is_active FROM users;
```

El email debe ser único y con formato válido (`algo@dominio.com`).

Si hace falta un usuario nuevo, desde la raíz del proyecto con el venv activado:

```bash
python -m scripts.create_user
```

Usa el mismo hash que la API. El cliente debe enviar `email` + `password`, no el `username` viejo.

---

## Paso 8 — Arrancar la API y validar

**Por qué:** código, `.env`, migraciones y emails ya están. Hay que levantar Uvicorn y comprobar LiteSpeed → NGINX → FastAPI.

```bash
sudo systemctl start fastapi-backend
sudo systemctl status fastapi-backend
```

Lo esperado: `active (running)`.

Si falla:

```bash
journalctl -u fastapi-backend --since "5 minutes ago" --no-pager
```

Prueba local y por dominio:

```bash
curl http://127.0.0.1:8000
curl https://tools.feuh.com.mx
```

Ambos deben devolver:

```json
{"message":"OCR Destinatarios API está funcionando correctamente"}
```

Login (opcional):

```bash
curl -X POST https://tools.feuh.com.mx/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"el_correo@tudominio.com","password":"tu_password"}'
```

Lo esperado: `access_token`. `401` = credenciales. `422` = el cliente aún manda `username` en vez de `email`.

---

## Despliegues siguientes (cuando no cambie el `.env` ni el login)

Si solo hay código/dependencias/migraciones nuevas:

```bash
cd ~/apps/fastapi-backend/Api_Destinatarios
sudo systemctl stop fastapi-backend
git pull
source ~/apps/venvs/fastapi-backend/bin/activate
pip install -r requirements.txt
alembic upgrade head
sudo systemctl start fastapi-backend
sudo systemctl status fastapi-backend
```

Detén el servicio antes de migrar. Si `upgrade` falla a medias (DDL de MySQL no es transaccional), no reintentes a ciegas: revisa columnas y `alembic current` como en el paso 6.

## Logs

```bash
journalctl -u fastapi-backend -f
journalctl -u fastapi-backend --since "10 minutes ago"
tail -f /var/log/nginx/error.log
tail -f /usr/local/lsws/logs/access.log
```

Tiempos de petición de la API: `logs/requests.log` dentro del proyecto.

## Tras reiniciar el VPS

No hace falta acción manual si los servicios están `enabled`. Verificar:

```bash
systemctl status fastapi-backend
systemctl status nginx
```

Ambos deben estar `active (running)`.
