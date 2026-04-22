# Api_Destinatarios

1. al inicia ejecutar `python -m pip install --upgrade pip` o  `pip install --upgrade pip`

1. instalar las siguientes librerias con pip install:
   * fastapi → Framework de la API
   * uvicorn → Servidor ASGI (ejecución)
   * sqlalchemy → ORM
   * alembic → Migraciones de base de datos
   * pymysql → Driver MySQL
   * python-dotenv → Variables de entorno (.env)
   * passlib[bcrypt] → Hash seguro de contraseñas
   * python-jose → JWT (access + refresh tokens)
   * pydantic → Validación de datos (v2, usado en schemas)
   * pytest → Tests (con SQLite en entorno de pruebas)
   
      al final utilizar `pip freeze`

1. crear la base de datos llamada ocr_destinatarios en mysql 
y crear el usuario dev con su respectivo password

1. crear archivo .env con los siguientes datos:
    <!-- agregar codigo -->
    ```
    DB_HOST=prod-db-host
    DB_PORT=3306
    DB_NAME=mi_db_prod
    DB_USER=usuario_prod
    DB_PASSWORD=secreto_fuerte
    ```
1. verificar la conexión a la base de datos ejecutando el archivo app/db/database.py
1. Ejecutar para generar las tablas `alembic upgrade head`
2. Levantar el servidor con `uvicorn app.main:app --reload`

