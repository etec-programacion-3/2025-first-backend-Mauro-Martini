from fastapi import FastAPI, HTTPException
from tortoise import fields, models
from tortoise.contrib.fastapi import register_tortoise
from pydantic import BaseModel, Field, constr
from typing import List

app = FastAPI(title="API Biblioteca", description="Gestión de libros - Fase 1", version="1.0.0")

# Modelo de Tortoise ORM (para la base de datos)
class Libro(models.Model):
    id = fields.IntField(pk=True)
    titulo = fields.CharField(max_length=255)
    autor = fields.CharField(max_length=255)
    isbn = fields.CharField(max_length=13)
    categoria = fields.CharField(max_length=100)
    estado = fields.CharField(max_length=50, default="disponible")
    fecha_creacion = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "libros"

# Modelos Pydantic
class LibroSchema(BaseModel):
    titulo: constr(min_length=1, max_length=255)
    autor: constr(min_length=1, max_length=255)
    isbn: constr(min_length=13, max_length=13)
    categoria: constr(min_length=1, max_length=100)

class LibroOut(BaseModel):
    titulo: str
    autor: str
    isbn: str
    categoria: str
    estado: str


    model_config = {
        "from_attributes": True
    }
class LibroUpdate(BaseModel):
    titulo: constr(min_length=1, max_length=255) | None = None
    autor: constr(min_length=1, max_length=255) | None = None
    isbn: constr(min_length=13, max_length=13) | None = None
    categoria: constr(min_length=1, max_length=100) | None = None
    estado: constr(min_length=1, max_length=50) | None = None

# Conexión con la base de datos
register_tortoise(
    app,
    db_url="sqlite://./db.sqlite3",
    modules={"models": ["biblioteca_backend.main"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

# Endpoints

@app.post("/libros/", response_model=LibroSchema, summary="Crear libro", description="Crea un nuevo libro con los datos enviados.")
async def crear_libro(libro: LibroSchema):
    """
    Crea un libro en la base de datos.

    - **titulo**: Título del libro.
    - **autor**: Nombre del autor.
    - **isbn**: Código ISBN (exactamente 13 caracteres).
    - **categoria**: Categoría o género del libro.
    """
    libro_obj = await Libro.create(**libro.dict())
    return libro_obj

from fastapi import Query

@app.get("/libros/", response_model=List[LibroSchema], summary="Listar libros", description="Lista libros con opciones de ordenamiento y paginación.")
async def listar_libros(
    ordenar_por: str = Query("titulo", description="Campo por el que se desea ordenar (ej: titulo, autor, fecha_creacion)"),
    orden: str = Query("asc", description="asc para ascendente o desc para descendente"),
    limit: int = Query(10, ge=1, le=25, description="Cantidad máxima de libros por página (1-25)"),
    offset: int = Query(0, ge=0, description="Cantidad de libros a omitir desde el inicio")
):
    """
    Lista libros con ordenamiento y paginación.

    - **ordenar_por**: Campo por el cual ordenar los resultados.
    - **orden**: Dirección del orden ('asc' o 'desc').
    - **limit**: Cuántos libros devolver por página.
    - **offset**: Cuántos libros saltar desde el inicio (para avanzar de página).
    """
    campos_validos = ["titulo", "autor", "isbn", "categoria", "estado", "fecha_creacion"]
    if ordenar_por not in campos_validos:
        raise HTTPException(status_code=400, detail=f"Campo de orden inválido: {ordenar_por}")

    orden_orm = f"-{ordenar_por}" if orden == "desc" else ordenar_por
    libros = await Libro.all().order_by(orden_orm).offset(offset).limit(limit)
    return libros


@app.get("/libros/{id}", response_model=LibroOut, summary="Obtener libro por ID", description="Devuelve los datos de un libro específico por su ID.")
async def obtener_libro(id: int):
    """
    Busca un libro por su ID.

    - **id**: Identificador del libro.
    """
    libro = await Libro.get_or_none(id=id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@app.put("/libros/{id}", response_model=LibroOut, summary="Actualizar libro", description="Actualiza los datos de un libro existente.")
async def actualizar_libro(id: int, datos: LibroUpdate):
    """
    Actualiza un libro existente.

    - **id**: ID del libro a actualizar.
    - Solo se deben enviar los campos que se desean modificar.
    """
    libro = await Libro.get_or_none(id=id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    datos_dict = datos.dict(exclude_unset=True)
    for campo, valor in datos_dict.items():
        setattr(libro, campo, valor)
    await libro.save()
    return libro

@app.delete("/libros/{id}", summary="Eliminar libro", description="Elimina un libro de la base de datos según su ID.")
async def eliminar_libro(id: int):
    """
    Elimina un libro por su ID.

    - **id**: ID del libro a eliminar.
    """
    libro = await Libro.get_or_none(id=id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    await libro.delete()
    return {"message": f"Libro con ID {id} eliminado correctamente"}

@app.get("/libros/buscar/", response_model=List[LibroOut], summary="Buscar libros por título", description="Busca libros que contengan la cadena proporcionada en su título.")
async def buscar_libros(titulo: str):
    """
    Busca libros cuyo título contenga la cadena proporcionada (búsqueda insensible a mayúsculas).

    - **titulo**: Cadena de texto que se buscará en los títulos de los libros.
    """
    libros = await Libro.filter(titulo__icontains=titulo)
    if not libros:
        raise HTTPException(status_code=404, detail="No se encontraron libros con ese título")
    return libros

@app.get("/libros/categoria/", response_model=List[LibroOut], summary="Buscar libros por categoría", description="Busca libros que pertenezcan a la categoría especificada.")
async def buscar_libros_por_categoria(categoria: str):
    """
    Busca libros que pertenezcan a una categoría específica.

    - **categoria**: Nombre de la categoría a la que los libros deben pertenecer.
    """
    libros = await Libro.filter(categoria__icontains=categoria)
    if not libros:
        raise HTTPException(status_code=404, detail="No se encontraron libros en esa categoría")
    return libros
