from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database_conection import classe_base
from .ulid_Generator import TipoULID, gerar_ulid


class Curso(classe_base):

    __tablename__ = "cursos"

    id         = Column(TipoULID, primary_key=True, default=gerar_ulid)
    nome       = Column(String(256), nullable=False, unique=True)

    turmas = relationship(
        "Turma",
        foreign_keys="[Turma.id_curso]",
        back_populates="curso"
    )
