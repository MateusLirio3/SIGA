from fastapi import APIRouter
from database.databaseCrud.ProfessorCrud import contar_Professores, buscar_todos_Professores, criar_Professor, buscar_Professor_por_nome, atualizar_Professor, deletar_Professor
from pydantic import BaseModel, Field

router = APIRouter(prefix="/API")

@router.get("/GetProfessoresCount", tags=["API", "GET"])
async def contagemProfessors():
    return contar_Professores()

@router.get("/GetProfessors", tags=["API", "GET"])
async def listarProfessores():
    Professors = [ Professor for Professor in buscar_todos_Professores()]
    return Professors

class Professor(BaseModel):
    nome: str
    matricula: str
    cpf: str
    email: str
    disciplinas: list[str] = Field(default_factory=list)

class ProfessorEdicao(Professor):
    id: str

@router.post("/PostProfessor", tags=["API","POST"])
async def adicionarProfessor(dados: Professor):
    return criar_Professor(
        nome=dados.nome, email=dados.email, senha="Abc123",
        matricula=dados.matricula, cpf=dados.cpf
    )

@router.post("/PostEditarProfessor", tags=["API", "POST"])
async def editarProfessor(dados: ProfessorEdicao):
    return atualizar_Professor(
        dados.id,
        dados.nome,
        dados.matricula,
        dados.cpf,
        dados.email,
    )

@router.delete("/DeleteProfessor/{id}", tags=["API", "DELETE"])
async def removerProfessor(id: str):
    return deletar_Professor(id)
