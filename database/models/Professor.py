from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from database.models.Usuario import Usuario
from .ulid_Generator import TipoULID, gerar_ulid

class Professor(Usuario):

    __tablename__ = "professores"

    id         = Column(TipoULID, ForeignKey("usuarios.id"), primary_key=True, default=gerar_ulid)
    matricula       = Column(String(13), nullable=False, unique = True)

    __mapper_args__ = {
        "polymorphic_identity" : "Professor"
    }

    disciplinas_turma = relationship(
        "DisciplinaTurma",
        back_populates="professor"
    )
