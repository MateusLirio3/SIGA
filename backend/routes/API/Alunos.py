from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.databaseCrud.AlunoCrud import (
    contar_Alunos,
    buscar_todos_Alunos,
    criar_Aluno,
    buscar_Aluno_por_cpf,
    atualizar_dados_Aluno,
    deletar_Aluno
)
from database.databaseCrud.MatriculaTurmaCrud import criar_MatriculaTurma
from database.databaseCrud.TurmaCrud import buscar_Turma_por_nome
from database.models.Status import Status
from datetime import date
router = APIRouter(prefix="/API")


class AlunoEntrada(BaseModel):
    nome: str
    matricula: str
    cpf: str
    turma: str
    status: str
    email: str


class AlunoEdicao(AlunoEntrada):
    id: str

@router.get("/GetAlunosCount", tags=["API", "GET"])
async def contagemAlunos():
    return contar_Alunos()

@router.get("/GetAlunos", tags=["API", "GET"])
async def listarAlunos():
    Alunos = [ aluno for aluno in buscar_todos_Alunos()]
    return Alunos

@router.post("/PostAluno", tags=["API","POST"])
async def adicionarAluno(dados: AlunoEntrada):
    status_por_nome = {
        "Ativo": Status.ATIVO,
        "Inativo": Status.INATIVO,
        "Pendente": Status.INDEFINIDO,
        "Concluído": Status.CONCLUIDO,
    }
    status = status_por_nome.get(dados.status)
    if status is None:
        raise HTTPException(status_code=422, detail="Status inválido")

    criar_Aluno(nome = dados.nome, email = dados.email, cpf = dados.cpf, matricula = dados.matricula, senha="Abc12345")
    aluno = buscar_Aluno_por_cpf(dados.cpf)

    turma = buscar_Turma_por_nome(dados.turma)
    criar_MatriculaTurma(
        turma.id,
        aluno.id,
        date.today(),
        status=status,
    )

    return aluno

    # ADICIONAR PARA ELE ENVIAR O EMAIL COM A SENHA TEMPORARIA DO ALUNO. OH MY FUCKING GOD :D

@router.post("/PostEditarAluno", tags=["API","POST"])
async def editarAluno(dados: AlunoEdicao):
    status_por_nome = {
        "Ativo": Status.ATIVO,
        "Inativo": Status.INATIVO,
        "Pendente": Status.INDEFINIDO,
        "Concluído": Status.CONCLUIDO,
        "ativo/a": Status.ATIVO,
        "inativo/a": Status.INATIVO,
        "indefinido/a": Status.INDEFINIDO,
        "concluido/a": Status.CONCLUIDO,
    }
    status = status_por_nome.get(dados.status)
    if status is None:
        raise HTTPException(status_code=422, detail="Status inválido")

    return atualizar_dados_Aluno(
        dados.id,
        dados.nome,
        dados.matricula,
        dados.cpf,
        dados.email,
        dados.turma,
        status,
    )


@router.delete("/DeleteAluno/{id}", tags=["API", "DELETE"])
async def removerAluno(id: str):
    return deletar_Aluno(id)

