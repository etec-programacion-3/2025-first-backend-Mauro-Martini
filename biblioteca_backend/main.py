from fastapi import FastAPI
from tortoise import fields, models
from tortoise.contrib.fastapi import register_tortoise

# Asegúrate que esta variable se llame EXACTAMENTE 'app'
app = FastAPI()  # <--- ¡Esta línea es esencial!

class Libro(models.Model):
    id = fields.IntField(pk=True)
    titulo = fields.CharField(max_length=255)
    autor = fields.CharField(max_length=255)
    isbn = fields.CharField(max_length=13, unique=True)
    categoria = fields.CharField(max_length=100)
    estado = fields.CharField(max_length=50)
    fecha_creacion = fields.DatetimeField(auto_now_add=True)

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["biblioteca_backend.main"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/")
async def root():
    return {"message": "API funcionando!"}