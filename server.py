from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import sqlite3
import secrets
from typing import Optional

# Inicializamos el motor del servidor
app = FastAPI(title="⚡ NEXUS LIGHTNING BACKEND ⚡", description="Un backend completo en un solo archivo para programar a la velocidad de la luz.")

# --- MÓDULO 1: MOTOR DE BASE DE DATOS LOCAL INTERNA ---
def init_db():
    conn = sqlite3.connect("lightning_data.db")
    cursor = conn.cursor()
    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            token TEXT
        )
    """)
    # Tabla de datos general (Key-Value) para la app del programador
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kv_store (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- MODELOS DE DATOS ---
class UserAuth(BaseModel):
    username: str
    password: str

class DataPayload(BaseModel):
    key: str
    value: str

# --- MÓDULO 2: SISTEMA DE AUTENTICACIÓN (LOGIN/REGISTRO) ---
@app.post("/auth/register", tags=["Autenticación"])
def register(user: UserAuth):
    conn = sqlite3.connect("lightning_data.db")
    cursor = conn.cursor()
    try:
        # Registramos al usuario y le creamos un Token de acceso único
        token = secrets.token_hex(16)
        cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (user.username, user.password, token))
        conn.commit()
        return {"status": "success", "message": "Usuario creado", "token": token}
    except sqlite3.IntegrityError:
        throw HTTPException(status_code=400, detail="El usuario ya existe")
    finally:
        conn.close()

@app.post("/auth/login", tags=["Autenticación"])
def login(user: UserAuth):
    conn = sqlite3.connect("lightning_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT token FROM users WHERE username=? AND password=?", (user.username, user.password))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {"status": "success", "token": row[0]}
    throw HTTPException(status_code=401, detail="Credenciales incorrectas")

# --- MÓDULO 3: API DE DATOS (Para guardar lo que sea de la App) ---
@app.post("/data/save", tags=["Base de Datos"])
def save_data(payload: DataPayload, token: str):
    # Verificación rápida de seguridad por Token
    conn = sqlite3.connect("lightning_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE token=?", (token,))
    if not cursor.fetchone():
        conn.close()
        throw HTTPException(status_code=403, detail="Token inválido o expirado")
    
    # Guardar o actualizar el dato
    cursor.execute("INSERT OR REPLACE INTO kv_store VALUES (?, ?)", (payload.key, payload.value))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"Dato '{payload.key}' guardado correctamente"}

@app.get("/data/get/{key}", tags=["Base de Datos"])
def get_data(key: str, token: str):
    conn = sqlite3.connect("lightning_data.db")
    cursor = conn.cursor()
    # Validar seguridad
    cursor.execute("SELECT username FROM users WHERE token=?", (token,))
    if not cursor.fetchone():
        conn.close()
        throw HTTPException(status_code=403, detail="Token inválido")
    
    # Buscar el dato
    cursor.execute("SELECT value FROM kv_store WHERE key=?", (key,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {"key": key, "value": row[0]}
    throw HTTPException(status_code=404, detail="Llave no encontrada")
