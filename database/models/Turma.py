from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database.database_conection import classe_base
from .Curso import Curso
from .ulid_Generator import TipoULID, gerar_ulid


class Turma(classe_base):

    __tablename__ = "turmas"

    id         = Column(TipoULID, primary_key=True, default=gerar_ulid)
    id_curso   = Column(TipoULID, ForeignKey("cursos.id"), unique=True)
    nome       = Column(String(256), nullable=False)
    periodo    = Column(String(256), nullable=False)
    ano        = Column(Integer(), nullable=False )

    curso = relationship(
        "Curso",
        foreign_keys="[Turma.id_curso]",
        back_populates="turmas"
    )

    matriculas = relationship(
        "MatriculaTurma",
        back_populates="turma"
    )