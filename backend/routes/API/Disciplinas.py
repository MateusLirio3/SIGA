from fastapi import APIRouter, HTTPException, Request
from database.databaseCrud.DisciplinaCrud import contar_Disciplinas, buscar_todos_Disciplinas, criar_Disciplina, buscar_Disciplina_por_nome, atualizar_Disciplina, deletar_Disciplina
from database.databaseCrud.CursoCrud import buscar_Curso_por_nome
from pydantic import BaseModel

router = APIRouter(prefix="/API")

@router.get("/GetDisciplinasCount", tags=["API", "GET"])
async def contagemDisciplinas():
    return contar_Disciplinas()

@router.get("/GetDisciplinas", tags=["API", "GET"])
async def listarDisciplinas():
    Disciplinas = [ Disciplina for Disciplina in buscar_todos_Disciplinas()]
    return Disciplinas

class Disciplina(BaseModel):
    nome: str

# class DisciplinaEdicao(Disciplina):
#     id: str

# @router.post("/PostDisciplina", tags=["API","POST"])
# async def adicionarDisciplina(dados: Disciplina):

#     curso_id = buscar_Curso_por_nome(dados.curso)
#     criar_Disciplina(nome = dados.nome)

#     Disciplina = buscar_Disciplina_por_nome(dados.nome)

#     return Disciplina

# @router.post("/PostEditarDisciplina", tags=["API", "POST"])
# async def editarDisciplina(dados: DisciplinaEdicao):
#     return atualizar_Disciplina(
#         dados.id,
#         dados.nome,
#         dados.periodo,
#         dados.curso
#     )

@router.delete("/DeleteDisciplina/{id}", tags=["API", "DELETE"])
async def removerAluno(id: str):
    return deletar_Disciplina(id)
