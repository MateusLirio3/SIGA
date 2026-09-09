from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from backend.permissoes import tem_permissao

templates = Jinja2Templates(directory="Frontend/pages/Coordenador")

router = APIRouter()

@router.get("/Aluno/{aluno_id}", tags=["Aluno", "Detalhes"])
async def detalhesAluno(request: Request, aluno_id: str):
    tipo = request.cookies.get("tipo_usuario", "")
        
    # colocar pra redirecionar pra pagina de erro(tem que criar tbm)

    if not tem_permissao(tipo, "visualizar"):
        raise HTTPException(
            status_code=403,
            detail="Você não tem permissão para acessar esta página."
        )
    
    return templates.TemplateResponse(
        request=request,
        name="aluno_detalhes.html",
        context={"request": request, "aluno_id": aluno_id}
    )