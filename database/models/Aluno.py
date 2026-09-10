from sqlalchemy import Column, String, ForeignKey
from database.models.Usuario import Usuario
from .ulid_Generator import TipoULID, gerar_ulid
from sqlalchemy.orm import relationship

class Aluno(Usuario):

    __tablename__ = "alunos"

    id         = Column(TipoULID, ForeignKey("usuarios.id"), primary_key=True, default=gerar_ulid)
    matricula       = Column(String(13), nullable=False, unique = True)

    __mapper_args__ = {
        "polymorphic_identity" : "Aluno"
    }

    matriculas = relationship(
        "MatriculaTurma",
        back_populates="aluno"
    )

    notas = relationship(
        "Nota",
        back_populates="aluno"
    )
