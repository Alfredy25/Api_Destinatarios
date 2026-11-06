# Importación de coberturas (`coverages_px`)

Catálogo mensual de coberturas Paquetexpress (sucursal, plaza, CP, colonia, municipio, ciudad, estado y tipo). Se consulta por código postal. Cada mes se reemplaza el contenido completo.

Valores válidos de `coverage_type`:

- `PAQUETEXPRESS`
- `ZONA PLUS`
- `ZONA PLUS ESPECIAL`

No incluir `id_delivery` en el archivo: MySQL lo genera solo.

Antes de subir el primer archivo, vaciar la tabla y reiniciar el contador:

```sql
TRUNCATE TABLE coverages_px;
```

Haz el `TRUNCATE` **una sola vez**. Los archivos siguientes se importan encima, sin volver a truncar.

## Pasos para importar

### 1. Dividir el archivo en partes de 20,000 filas

El archivo original es grande. Partirlo en bloques de **20,000 filas** para que phpMyAdmin no se corte por tiempo ni por tamaño.

Cada parte debe conservar el mismo orden de columnas.

### 2. Concatenar columnas con `;` usando `UNIRCADENAS`

Las colonias, municipios y ciudades suelen traer comas (`,`). Si el CSV se separa por coma, phpMyAdmin parte mal esas filas.

En Excel, unir las columnas con **punto y coma** usando `UNIRCADENAS`:

```excel
=UNIRCADENAS(";";VERDADERO;A2:H2)
```

El resultado de cada fila queda así:

```text
SUCURSAL;PLAZA;01000;COLONIA;MUNICIPIO;CIUDAD;ESTADO;PAQUETEXPRESS
```

Orden de columnas:

`branch` ; `place` ; `postal_code` ; `colony` ; `municipality` ; `city` ; `state` ; `coverage_type`

No concatenar el `id`. Si una celda va vacía (por ejemplo `place`), `UNIRCADENAS` con `VERDADERO` se salta los vacíos y descuadra las columnas: usa `FALSO` si hay campos opcionales vacíos:

```excel
=UNIRCADENAS(";";FALSO;A2:H2)
```

### 3. Crear archivos TXT y subirlos a phpMyAdmin

1. Copiar cada bloque concatenado a un archivo de texto.
2. Guardar como `.txt` (UTF-8 si phpMyAdmin lo permite).
3. En phpMyAdmin: base `ocr_destinatarios` → tabla `coverages_px` → pestaña **Importar**.
4. Elegir el `.txt` y formato **CSV**.
5. Importar un archivo tras otro (parte 1, parte 2, …).

### 4. Opciones de phpMyAdmin

| Opción | Valor |
| --- | --- |
| Formato | CSV |
| Actualizar datos si hay llaves duplicadas | Apagado |
| Columnas separadas por | `;` |
| Columnas encerradas entre | `"` |
| Caracter de escape | `\` |
| Líneas terminadas en | `auto` |
| Importe este gran número de filas | Vacío |
| Nombres de columna | `branch,place,postal_code,colony,municipality,city,state,coverage_type` |
| No abortar si ocurre un error | Apagado |

Nombres de columna (tal cual, separados por coma en ese recuadro):

```text
branch,place,postal_code,colony,municipality,city,state,coverage_type
```

Si el `.txt` trae encabezado en la primera línea, marca que la primera fila son nombres de columna (o bórrala antes de subir). Si no, phpMyAdmin intentará insertar el encabezado como dato y fallará el enum.

## Comprobar

Después de importar todas las partes:

```sql
SELECT COUNT(*) FROM coverages_px;
SELECT * FROM coverages_px LIMIT 10;
```

La consulta de la API sigue siendo `GET /coverages/?cp=01000`.
