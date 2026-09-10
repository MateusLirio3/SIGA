from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database_conection import classe_base
from .ulid_Generator import TipoULID, gerar_ulid

class DisciplinaTurma(classe_base):

    __tablename__ = "disciplinaTurma"

    id         = Column(TipoULID, primary_key=True, default=gerar_ulid)
    id_turma   = Column(TipoULID, ForeignKey("turmas.id"), nullable=False)
    id_disciplina = Column (TipoULID, ForeignKey("disciplinas.id"), nullable=False)
    id_professor  = Column(TipoULID, ForeignKey("professores.id"), nullable=False)

    turma = relationship(
        "Turma",
        back_populates="disciplinas_turma"
    )

    disciplina = relationship(
        "Disciplina",
        back_populates="disciplinas_turma"
    )

    professor = relationship(
        "Professor",
        back_populates="disciplinas_turma"
    )

    nota = relationship(
        "Nota",
        back_populates="disciplinaturma"
    )