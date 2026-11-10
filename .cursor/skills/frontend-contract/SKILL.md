---
name: frontend-contract
description: Genera documentación Markdown de contrato HTTP para un frontend PySide6 a partir de una entidad del backend. Use when the user names an entity (receiver, address, contact, job_role, organization, title, volante, sepomex, shipment, user, record) and asks for frontend docs, contrato frontend, documentación de endpoints, o un contrato para PySide6.
---

# Frontend Contract Generator

Objetivo:
Generar documentación para frontend a partir de una entidad existente.

Pasos:

1. Localiza los routers relacionados.
2. Localiza los schemas Pydantic.
3. Identifica validaciones.
4. Identifica respuestas.
5. Identifica errores.
6. Genera documentación Markdown.

Formato:
# Receiver

## POST /receivers

### Descripción
Crear destinatario.

### Request

{
 ...
}

### Campos
...

### Validaciones
...

### Respuesta
...

### Errores
...

## Cuándo usarla

El usuario nombra una entidad (o un módulo de `app/api/v1/<modulo>/`) y pide documentación para el escritorio PySide6. No inventes rutas ni campos. Lee el código y documenta solo lo que existe.

Salida: Markdown en el chat. Si pide archivo, escríbelo en `docs_md/contrato_<entidad>.md`. No generes widgets Qt salvo que lo pida.

## Dónde buscar

Por cada entidad, lee estos archivos (ajusta el nombre del módulo):

| Qué | Ruta |
|-----|------|
| Rutas | `app/api/v1/<modulo>/router.py` |
| Schemas | `app/api/v1/<modulo>/schemas.py` |
| Errores de negocio | `app/api/v1/<modulo>/service.py` (`HTTPException`) |
| Códigos Pydantic extra | `app/api/v1/<modulo>/error_codes.py` si existe |
| Montaje real | `app/main.py` (`include_router`) |
| Auth | `app/api/v1/security/service.py` (`get_current_user`) |
| 422 global | handler en `app/main.py` |

Módulos actuales: `address`, `contact`, `job_role` (prefijo `/job-roles`), `organization`, `receiver`, `title`, `volante` (prefijo `/volante`), `sepomex`, `shipment` (`/shipments-px`), `user` (`/users`), `record` (`/registros`), `coverage_px` (`/coverages`), `security` (`/auth`).

`position` no está montado en `main.py`. No documentes rutas de position. Documenta el nested `position` solo cuando otra entidad (receiver) lo manda en el body.

Si el alta anida otras entidades (receiver crea address/contact/title/volante/position), lee esos schemas Create y enlázalos; no dupliques el contrato completo de cada una salvo que el usuario pida varias entidades.

## Cómo extraer cada sección

**Ruta.** `APIRouter.prefix` + path del decorator. Método HTTP, `status_code`, `response_model`, `summary`/`docstring`. Query, Path y Body por separado. Si el endpoint tiene `Depends(get_current_user)`, el request lleva header `Authorization: Bearer <token>`. Token: `POST /auth/login` con `{ "email", "password" }` → `{ "access_token", "token_type": "bearer" }`.

**Request.** Un JSON de ejemplo con `examples=` de Field o valores reales del schema. GET no lleva body: documenta query/path. PATCH: solo campos enviados (`exclude_unset`); no pongas null para “borrar” si el validator lo rechaza.

**Campos.** Tabla: nombre, tipo JSON, requerido, default, origen (body / query / path). Incluye nested objects. Campos de auditoría `created_at`, `updated_at`, `created_by`, `updated_by` son de respuesta, no de alta ni de PATCH.

**Validaciones.** De `Field(...)`: `min_length`, `max_length`, `ge`, `le`, `pattern`, `examples`. De `@field_validator` / `@model_validator` / `AfterValidator`: normalización (strip, upper, title) y reglas condicionales (PERSONA vs GOBIERNO). De Query/Path en el router. Traduce a reglas de formulario PySide6, no copies el Python.

**Respuesta.** Status de éxito y JSON del `response_model` (Dto o Paginated*). Paginated típico: `page`, `page_size`, `total`, `total_pages`, `has_prev`, `has_next`, `order_by`, `direction`, `search`, `items`.

**Errores.** Lista `{status, cuando, cuerpo}`:

- 401: token ausente, inválido o usuario inactivo. `{"detail": "Token inválido o expirado"}` o `"Usuario no válido o inactivo"`.
- 422 validación FastAPI: `{"errors": [{"message", "field", "type"}]}`.
- 404 / 409 / 422 de servicio: `detail` string o `{"msg", "<id>"}` (duplicados de receiver/address/contact).
- Códigos `PydanticCustomError` (receiver): el `type` del 422 coincide con `error_codes.py`.

No listes CORS: PySide6 no lo usa.

## Mapeo rápido PySide6

Solo como pista en Campos o Validaciones, no como código:

| Tipo API | Widget típico |
|----------|----------------|
| `str` corto | `QLineEdit` + `setMaxLength` |
| `str` + pattern | `QRegularExpressionValidator` |
| enum / Literal | `QComboBox` |
| `bool` | `QCheckBox` |
| `int` | `QSpinBox` |
| email | `QLineEdit` + validación de correo |
| objeto nested | grupo / diálogo |
| lista | tabla o lista |

Auth: un `QNetworkAccessManager` (o equivalente) debe adjuntar el Bearer en cada llamada documentada como protegida.

## Plantilla por endpoint

Repite un bloque por cada método del router. Título del documento = nombre de la entidad (Receiver, JobRole, Title, …).

```markdown
# <Entidad>

Auth: Bearer token. Header `Authorization: Bearer <access_token>`.
(omite Auth si el endpoint no usa `get_current_user`)

## <METODO> <ruta>

### Descripción
<summary o docstring>

### Request

```json
{ }
```

Query (si aplica):
- `search`: string, opcional, ...

Path (si aplica):
- `id`: int >= 1

Header:
- `Authorization`: Bearer <token>

### Campos
| Campo | Tipo | Requerido | Default | Notas |
|-------|------|-----------|---------|-------|

### Validaciones
- ...

### Respuesta
Status: 201
```json
{ }
```

### Errores
| Status | Cuándo | Cuerpo |
|--------|--------|--------|
```

Si un GET no tiene body, deja Request con query/path y un JSON vacío o omite el JSON.

## Ejemplo mínimo (título)

Entrada del usuario: “documentación frontend de title”

Salida (recortada):

```markdown
# Title

Auth: Bearer token.

## GET /titles/

### Descripción
Listar títulos paginados.

### Request

Query:
- `search`: string, opcional, 2–60, pattern letras/números/punto/espacio
- `page`: int, default 1, >= 1
- `page_size`: int, default 50, 5–80
- `order_by`: `id` | `abbrev` | `meaning`, default `id`
- `direction`: `desc` | `asc`, default `asc`

### Campos
| Campo | Tipo | Requerido | Default | Notas |
|-------|------|-----------|---------|-------|
| search | string | no | null | query |

### Validaciones
- search se normaliza (trim) y exige al menos 3 caracteres útiles vía `normalize_search` si viene informado (revisar el router real).

### Respuesta
Status: 200 — `PaginatedTitles`

### Errores
| Status | Cuándo | Cuerpo |
|--------|--------|--------|
| 401 | sin token | `{"detail": "Token inválido o expirado"}` |
| 422 | query inválido | `{"errors":[{"message","field","type"}]}` |

## POST /titles/

### Descripción
Crear título.

### Request

```json
{ "abbreviation": "DR.", "meaning": "Doctor" }
```

### Campos
| Campo | Tipo | Requerido | Default | Notas |
|-------|------|-----------|---------|-------|
| abbreviation | string | sí | — | body |
| meaning | string | sí | — | body |

### Validaciones
- abbreviation: min 3, max 60
- meaning: min 3, max 150

### Respuesta
Status: 201 — TitleDto con `id`, `abbreviation`, `meaning`, `created_at`, `updated_at`, `created_by`, `updated_by`

### Errores
| Status | Cuándo | Cuerpo |
|--------|--------|--------|
| 409 | ya existe | `{"detail": "El titulo ya existe"}` |
```

Ajusta min/max/pattern al schema actual; el ejemplo no sustituye la lectura del archivo.
