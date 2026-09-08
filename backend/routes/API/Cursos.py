from fastapi import APIRouter, HTTPException, Request
from database.databaseCrud.CursoCrud import contar_Cursos, buscar_todos_Cursos

router = APIRouter(prefix="/API")

@router.get("/GetCursosCount", tags=["API", "GET"])
async def contagemCursos():
    return contar_Cursos()

@router.get("/GetCursos", tags=["API", "GET"])
async def listarCursos():
    Cursos = [ curso for curso  in buscar_todos_Cursos()]
    return Cursos