from database.database_conection import sessao_local
from database.models.DisciplinaTurma import DisciplinaTurma
from sqlalchemy.orm import make_transient
from .Erros import ErroExcluir, ErroNaoEncontrado, ErroRegistrar, ErroAtualizar

def criar_disciplinaTurma(id_Turma, id_disciplina, id_professor, id_nota):
    
    sessao = sessao_local()
    try:
        novo = DisciplinaTurma(
            id_turma=id_Turma,
            id_disciplina = id_disciplina,
            id_professor = id_professor,
            id_nota = id_nota,
        )
        sessao.add(novo)
        sessao.commit()
        sessao.refresh(novo)
        sessao.expunge(novo)
        return novo
    except Exception as erro:
        sessao.rollback()
        raise ErroRegistrar(f"Erro ao registrar disciplinaTurma (id={DisciplinaTurma.id})") from erro
    finally:
        sessao.close()

def buscar_todos_disciplinaTurmas():
    sessao = sessao_local()
    try:
        resultados = sessao.query(DisciplinaTurma).all()
        for r in resultados:
            sessao.expunge(r)
        return resultados
    finally:
        sessao.close()

def contar_disciplinaTurmas():
    sessao = sessao_local()
    try:
        resultado = sessao.query(DisciplinaTurma).count()
        return resultado
    finally:
        sessao.close()


def buscar_disciplina_turma_por_turma(id_turma):
    sessao = sessao_local()

    try:
        resultados = (
            sessao.query(DisciplinaTurma)
            .filter(DisciplinaTurma.id_turma == id_turma)
            .all()
        )

        if not resultados:
            raise ErroNaoEncontrado(
                f"Nenhuma disciplina encontrada para a turma (id_turma={id_turma})"
            )

        return [
            {
                "Id": item.id,
                "Turma": item.turma.nome if item.turma else None,
                "Disciplina": item.disciplina.nome if item.disciplina else None,
                "Professor": item.professor.nome if item.professor else None,
                "Nota": item.nota.id if item.nota else None,
            }
            for item in resultados
        ]

    except ErroNaoEncontrado:
        raise
    finally:
        sessao.close()

def atualizar_disciplinaTurma(id_disciplinaTurma, nova_disciplinaTurma):
    sessao = sessao_local()
    try:
        disciplinaTurma = sessao.query(disciplinaTurma).filter(disciplinaTurma.id == id_disciplinaTurma).first()
        if disciplinaTurma is None:
            raise ErroNaoEncontrado(f"disciplinaTurma nao encontrado (id={id_disciplinaTurma})")
        if nova_disciplinaTurma is not None:
            disciplinaTurma.valor = nova_disciplinaTurma
        
        sessao.commit()
        sessao.refresh(disciplinaTurma)
        sessao.expunge(disciplinaTurma)
        return disciplinaTurma
    except ErroNaoEncontrado:
        raise
    except Exception as erro:
        sessao.rollback()
        raise ErroAtualizar(f"Erro ao atualizar disciplinaTurma (id={id_disciplinaTurma})") from erro
    finally:
        sessao.close()

def deletar_disciplinaTurma(id_disciplinaTurma):
    sessao = sessao_local()
    try:
        disciplinaTurma = sessao.query(disciplinaTurma).filter(disciplinaTurma.id == id_disciplinaTurma).first()
        if disciplinaTurma is None:
            raise ErroNaoEncontrado(f"disciplinaTurma nao encontrado (id={id_disciplinaTurma})")
        sessao.delete(disciplinaTurma)
        sessao.commit()
        return True
    except ErroNaoEncontrado:
        raise
    except Exception as erro:
        sessao.rollback()
        raise ErroExcluir(f"Erro ao excluir disciplinaTurma (id={id_disciplinaTurma})") from erro
    finally:
        sessao.close()