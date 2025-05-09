from fastapi import FastAPI, HTTPException
from tortoise import fields, models
from tortoise.contrib.fastapi import register_tortoise
from pydantic.v1 import BaseModel  # ¡Usa pydantic.v1 explícitamente!
from typing import List

app = FastAPI()

# Modelo de Tortoise ORM (para la base de datos)
class Libro(models.Model):
    id = fields.IntField(pk=True)
    titulo = fields.CharField(max_length=255)
    autor = fields.CharField(max_length=255)
    isbn = fields.CharField(max_length=13)
    categoria = fields.CharField(max_length=100)
    estado = fields.CharField(max_length=50, default="disponible")  # Nuevo campo "default"
    fecha_creacion = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "libros"  # Opcional: nombre personalizado para la tabla

# Modelo Pydantic (para validación de entradas/salidas)
class LibroSchema(BaseModel):
    titulo: str
    autor: str
    isbn: str
    categoria: str
    # No incluyas campos como 'id' o 'fecha_creacion' (son automáticos) 

# Configuración de la base de datos (¡Ajusta el módulo!)
register_tortoise(
    app,
    db_url="sqlite://./db.sqlite3",  # "../" porque main.py está en biblioteca_backend/
    modules={"models": ["biblioteca_backend.main"]},  # Ruta al módulo
    generate_schemas=True,  # Crea tablas automáticamente
    add_exception_handlers=True,
)

# Endpoint de prueba
@app.get("/")
async def root():
    return {"message": "¡API de Biblioteca con DB activa!"}

# Endpoint para crear un libro
@app.post("/libros/", response_model=LibroSchema)
async def crear_libro(libro: LibroSchema):
    libro_obj = await Libro.create(**libro.dict())
    return libro_obj

# Endpoint para listar libros
@app.get("/libros/", response_model=List[LibroSchema])
async def listar_libros():
    return await Libro.all()