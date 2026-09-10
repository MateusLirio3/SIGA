from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from database.database_conection import classe_base
from .ulid_Generator import TipoULID, gerar_ulid
from .Turma import Turma
from .DisciplinaTurma import DisciplinaTurma

class Nota(classe_base):

    __tablename__ = "notas"

    id         = Column(TipoULID, primary_key=True, default=gerar_ulid)
    id_disciplinaTurma   = Column(TipoULID, ForeignKey("disciplinaTurma.id"), nullable=False)
    id_aluno   = Column(TipoULID, ForeignKey("alunos.id"), nullable=False)
    instrumento_Avaliativo     = Column(String(256), nullable=False)
    valor     = Column(Float, nullable=False)

    disciplinaturma = relationship(
        "DisciplinaTurma",
        back_populates="nota"
    )

    aluno = relationship(
        "Aluno",
        back_populates="notas"
    )
