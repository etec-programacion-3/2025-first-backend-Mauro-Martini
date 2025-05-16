# Proyecto Backend - Sistema de Gestión de Biblioteca

## Información del Alumno
- Nombre y Apellido: [Mauro-Martini]
- Curso: 5to Año
- Especialidad: Informática

## Configuración del Repositorio
- La rama `main` debe estar protegida
- No se permiten push directos a `main`
- Todos los cambios deben realizarse a través de Pull Requests
- Los Pull Requests deben ser aprobados antes de ser mergeados

## Descripción
Este proyecto consiste en desarrollar un sistema backend para la gestión de una biblioteca escolar. El desarrollo se realizará en tres fases incrementales:

### Fase 1: Gestión de Libros
Implementación de la API REST para gestionar libros, incluyendo:
- CRUD completo de libros
- Búsqueda y filtrado
- Documentación de endpoints

### Fase 2: Gestión de Usuarios
Implementación del sistema de usuarios, incluyendo:
- Registro y autenticación
- Roles y permisos
- Perfiles de usuario

### Fase 3: Gestión de Préstamos
Implementación del sistema de préstamos, incluyendo:
- Préstamos y devoluciones
- Historial de préstamos
- Notificaciones

## Objetivos de Aprendizaje
- Diseñar e implementar una API REST
- Trabajar con bases de datos SQL a través de ORM
- Manejar versionado de código con Git
- Trabajar con milestones e issues en GitHub
- Documentar la API

## Tecnologías
Los estudiantes pueden elegir entre las siguientes tecnologías:
- Node.js + Express + Sequelize + SQLite
- Python + Flask + SQLAlchemy + SQLite
- Python + FastAPI + Tortoise ORM + SQLite

Nota: Se debe utilizar un ORM (Object-Relational Mapping) para interactuar con la base de datos. No se permite el uso de SQL nativo.

## Pruebas de la API
- Se recomienda utilizar REST Client para probar los endpoints
- Crear un archivo `requests.http` en el proyecto con todas las peticiones necesarias
- Incluir ejemplos de todas las operaciones CRUD
- Documentar cada petición con comentarios explicativos

## Fase 1: Gestión de Libros

### Modelo de Datos
```python
# Ejemplo con Tortoise ORM
class Libro(Model):
    id = fields.IntField(pk=True)
    titulo = fields.CharField(max_length=255)
    autor = fields.CharField(max_length=255)
    isbn = fields.CharField(max_length=13, unique=True)
    categoria = fields.CharField(max_length=100)
    estado = fields.CharField(max_length=50)  # disponible, prestado, etc.
    fecha_creacion = fields.DatetimeField(auto_now_add=True)
```

### Endpoints
```
GET    /libros           # Listar todos los libros
GET    /libros/{id}      # Obtener un libro específico
POST   /libros           # Crear un nuevo libro
PUT    /libros/{id}      # Actualizar un libro
DELETE /libros/{id}      # Eliminar un libro
GET    /libros/buscar    # Buscar libros (parámetros: titulo, autor, categoria)
```

### Milestones Fase 1
1. Configuración Inicial
   - [ ] Configurar el proyecto base
   - [ ] Implementar la conexión a la base de datos
   - [ ] Crear el modelo de libros

2. CRUD Básico
   - [ ] Implementar endpoints para libros
   - [ ] Implementar validación de datos
   - [ ] Documentar los endpoints

3. Búsqueda y Filtrado
   - [ ] Implementar búsqueda por título
   - [ ] Implementar filtrado por categoría
   - [ ] Implementar ordenamiento
   - [ ] Implementar paginación

## Fase 2: Gestión de Usuarios

### Modelo de Datos
```python
# Ejemplo con Tortoise ORM
class Usuario(Model):
    id = fields.IntField(pk=True)
    nombre = fields.CharField(max_length=100)
    apellido = fields.CharField(max_length=100)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    rol = fields.CharField(max_length=50)  # admin, usuario
    activo = fields.BooleanField(default=True)
    fecha_creacion = fields.DatetimeField(auto_now_add=True)
```

### Endpoints
```
POST   /auth/registro    # Registrar nuevo usuario
POST   /auth/login       # Iniciar sesión
GET    /usuarios         # Listar usuarios (solo admin)
GET    /usuarios/{id}    # Obtener perfil de usuario
PUT    /usuarios/{id}    # Actualizar perfil
```

### Milestones Fase 2
1. Autenticación Básica
   - [ ] Implementar registro de usuarios
   - [ ] Implementar login/logout
   - [ ] Implementar tokens JWT

2. Gestión de Usuarios
   - [ ] Implementar roles y permisos
   - [ ] Implementar gestión de perfiles
   - [ ] Proteger endpoints según roles

## Fase 3: Gestión de Préstamos

### Modelo de Datos
```python
# Ejemplo con Tortoise ORM
class Prestamo(Model):
    id = fields.IntField(pk=True)
    libro = fields.ForeignKeyField('models.Libro')
    usuario = fields.ForeignKeyField('models.Usuario')
    fecha_prestamo = fields.DatetimeField(auto_now_add=True)
    fecha_devolucion = fields.DatetimeField(null=True)
    estado = fields.CharField(max_length=50)  # activo, devuelto, vencido
```

### Endpoints
```
POST   /prestamos           # Crear nuevo préstamo
PUT    /prestamos/{id}      # Registrar devolución
GET    /prestamos/activos   # Listar préstamos activos
GET    /prestamos/historial # Ver historial de préstamos
GET    /prestamos/vencidos  # Listar préstamos vencidos
```

### Milestones Fase 3
1. Sistema de Préstamos
   - [ ] Implementar préstamos de libros
   - [ ] Implementar devolución de libros
   - [ ] Implementar validaciones de préstamos

2. Gestión de Estado
   - [ ] Implementar historial de préstamos
   - [ ] Implementar notificaciones de vencimiento
   - [ ] Implementar reportes

## Criterios de Evaluación
- Correcta implementación de los endpoints
- Calidad del código
- Manejo de errores
- Documentación
- Uso correcto de Git
- Gestión de milestones e issues

## Entregables
1. Repositorio Git con el código fuente
2. Documentación de la API
3. Archivo requests.http con ejemplos de uso
4. Diagrama de la base de datos
5. Presentación del proyecto

