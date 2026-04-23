"""
Script administrativo para crear usuarios del sistema.

Uso:
    python scripts/create_user.py

IMPORTANTE:
- Este script NO es una API
- Debe ejecutarse en un entorno confiable
- Usa el mismo hashing que el backend
"""

import getpass

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password


def create_user():
    print("=== Crear usuario del sistema ===")

    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    password_confirm = getpass.getpass("Confirmar password: ")

    if password != password_confirm:
        print("Las contraseñas no coinciden")
        return

    db: Session = SessionLocal()

    try:
        # Verificar si el usuario ya existe
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            print("El usuario ya existe")
            return

        user = User(
            username=username,
            password_hash=hash_password(password),
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        print(f"Usuario '{username}' creado correctamente (id={user.id})")

    finally:
        db.close()


if __name__ == "__main__":
    create_user()