from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from backend.permissoes import tem_permissao

templates = Jinja2Templates(directory="Frontend/pages/Coordenador")

router = APIRouter()

@router.get("/Alunos", tags=["Coordenador", "Alunos"])
async def listarAlunos(request: Request):
    tipo = request.cookies.get("tipo_usuario", "")
        
    # colocar pra redirecionar pra pagina de erro(tem que criar tbm)

    if not tem_permissao(tipo, "listar"):
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para acessar esta página."
        )
    
    return templates.TemplateResponse(
        request=request,
        name="alunos.html",
        context={"request": request}
    )