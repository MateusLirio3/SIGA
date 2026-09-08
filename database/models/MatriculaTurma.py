from sqlalchemy import Column, ForeignKey, DATE, Enum
from sqlalchemy.orm import relationship, mapped_column, Mapped
from database.database_conection import classe_base
from .ulid_Generator import TipoULID, gerar_ulid
from .Turma import Turma
from .Aluno import Aluno
from .Status import Status

class MatriculaTurma(classe_base):

    __tablename__ = "matriculaturma"

    id         = Column(TipoULID, primary_key=True, default=gerar_ulid)
    id_turma   = Column(TipoULID, ForeignKey("turmas.id"), nullable=False)
    id_aluno   = Column(TipoULID, ForeignKey("alunos.id"), nullable=False)
    data_Entrada = Column(DATE, nullable=False)
    data_Saida = Column(DATE, nullable=True)
    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False)

    turma = relationship(
        "Turma",
        back_populates="matriculas"
    )

    aluno = relationship(
        "Aluno",
        back_populates="matriculas"
    )
