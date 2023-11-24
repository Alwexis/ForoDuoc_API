from pydantic import BaseModel, Field
from db import DB

class Usuario(BaseModel):
    correo: str = Field(description="Correo institucional del Alumno.")
    contrasena: str = Field(description="Contraseña de la Cuenta.")
    nombre: str = Field(description="Nombre del Usuario o Alumno.")
    rut: int = Field(description="RUT del Alumno.")
    dv: str = Field(description="Dígito Verificador.")
    activo: bool = Field(description="Estado de la cuenta del Alumno.")
    relevancia: int = Field(description="Puntos de relevancia del Alumno.")
    salud: list = Field(description="Lista de información sobre la salud de un Alumno.", examples=["Movilidad Reducida", "Espectro Autista"])
    carrera: int = Field(description="ID de la carrera a la cual pertenece el Alumno.")
    horario: int = Field(description="ID del horario al cual pertenece el Alumno.")

class Carrera(BaseModel):
    id: int =  Field(description="Base de datos de duoc.")
    nombre: str = Field(description="Nombre de la carrera.")
    duracion: int = Field(description="Cuanto dura la carrera.")
    modalidad: str = Field(description="Si es diurno o vespertino.")

class Escuela(BaseModel):
    id: int = Field(description="ID de la escuela.")
    nombre: str = Field(description="Nombre de la escuela.")
    sede: str = Field(description="Nombre de la sede.")

class Horario(BaseModel):
    id: int = Field(description="Id del horario.")
    ramos: list = Field(description="Nombre de los ramos.")

class Publicacion(BaseModel):
    id: int = Field(description="ID de la Publicación.")
    usuario: str = Field(description="Usuario autor de la publicación.")
    contenido: str = Field(description="Contenido escrito de la publicación.")
    adjuntos: list = Field(description="Lista de archivos adjuntos. Pueden ser imágenes o archivos.")
    reacciones: object = Field(description="Lista y métricas de las reacciones al foro. Incluídos 'Me Gustas', 'Comentarios', 'Compartidos'")
    foro: int = Field(description="ID del Foro al cual se subió la publicación. Puede ser nulo", default=None)

class Comentario(BaseModel):
    id: int = Field(description="ID del Comentario.")
    usuario: str = Field(description="Usuario autor del comentario.")
    contenido: str = Field(description="Contenido escrito de la publicación.")
    adjuntos: list = Field(description="Lista de archivos adjuntos. Pueden ser imágenes o archivos.")
    reacciones: object = Field(description="Lista y métricas de las reacciones al foro. Incluídos 'Me Gustas', 'Comentarios', 'Compartidos'")
    foro: int = Field(description="ID del Foro al cual se subió la publicación. Puede ser nulo", default=None)
    comentario_raiz = int = Field(description="ID del comentario Raíz, este campo se aplica únicamente cuando el comentario en cuestión es respondiendo a otro comentario.", default=None)

class Foro(BaseModel):
    id: int = Field(description="ID del Foro")
    nombre: str = Field(description="Nombre del Foro")
    descripcion: str = Field(description="Descripción del Foro.")
    carrera: list = Field(description="IDs de las Carreras ligadas al Foro. Se necesita al menos una.")
    moderadores: list = Field(description="Moderadores o Creadores del Foro. Además de estos moderadores estarán los globales y los moderadores automatizados")
    imagen: str = Field(description="URL de la Imagen del Foro")


#* Auto Incremento *#
_db = DB()

class AutoIncrementoModel(BaseModel):
    sequence_name: str = Field(description='Nombre del AutoIncremento')
    seq: int = Field(description='Secuencia del AutoIncremento')
    by: int = Field(description='Incremento del AutoIncremento')

class AutoIncremento:
    def __init__(self, sequence_name, seq=0, by=1):
        self.sequence_name = sequence_name
        self.seq = seq
        self.by = by

    async def next(self):
        secuencia = await _db.get('AutoIncremento', {'sequence_name': self.sequence_name})
        if len(secuencia) < 1:
            auto_incremento_model = AutoIncrementoModel(sequence_name=self.sequence_name, seq=self.seq, by=self.by)
            await _db.insert('AutoIncremento', auto_incremento_model.model_dump())  # Convierte a diccionario antes de insertar
        else:
            auto_incremento_model = AutoIncrementoModel(**secuencia[0])

        auto_incremento_model.seq += auto_incremento_model.by
        await _db.update('AutoIncremento', {'sequence_name': self.sequence_name}, {'seq': auto_incremento_model.seq})
        return auto_incremento_model.seq