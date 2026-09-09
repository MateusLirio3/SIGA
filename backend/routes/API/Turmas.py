from fastapi import APIRouter, HTTPException, Request
from database.databaseCrud.TurmaCrud import contar_Turmas, buscar_todos_Turmas, criar_Turma, buscar_Turma_por_nome, atualizar_Turma, deletar_turma
from database.databaseCrud.CursoCrud import buscar_Curso_por_nome
from pydantic import BaseModel

router = APIRouter(prefix="/API")

@router.get("/GetTurmasCount", tags=["API", "GET"])
async def contagemTurmas():
    return contar_Turmas()

@router.get("/GetTurmas", tags=["API", "GET"])
async def listarTurmas():
    Turmas = [ Turma for Turma in buscar_todos_Turmas()]
    return Turmas

class Turma(BaseModel):
    nome: str
    curso: str
    periodo: str
    ano: int

class TurmaEdicao(Turma):
    id: str

@router.post("/PostTurma", tags=["API","POST"])
async def adicionarTurma(dados: Turma):

    curso_id = buscar_Curso_por_nome(dados.curso)
    criar_Turma(nome = dados.nome, id_curso = curso_id.id, periodo= dados.periodo, ano = dados.ano)

    turma = buscar_Turma_por_nome(dados.nome)

    return turma

@router.post("/PostEditarTurma", tags=["API", "POST"])
async def editarTurma(dados: TurmaEdicao):
    return atualizar_Turma(
        dados.id,
        dados.nome,
        dados.periodo,
        dados.curso
    )

@router.delete("/DeleteTurma/{id}", tags=["API", "DELETE"])
async def removerAluno(id: str):
    return deletar_turma(id)
