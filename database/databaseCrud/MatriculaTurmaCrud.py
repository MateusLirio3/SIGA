from database.database_conection import sessao_local
from database.models.MatriculaTurma import MatriculaTurma
from database.models.Aluno import Aluno
from sqlalchemy.orm import make_transient
from .Erros import ErroExcluir, ErroNaoEncontrado, ErroRegistrar, ErroAtualizar

def criar_MatriculaTurma(id_Turma, id_aluno, data_Entrada, status):
    
    sessao = sessao_local()
    try:
        novo = MatriculaTurma(
            id_turma=id_Turma,
            id_aluno=id_aluno,
            data_Entrada=data_Entrada,
            status=status
        )
        sessao.add(novo)
        sessao.commit()
        sessao.refresh(novo)
        sessao.expunge(novo)
        return novo
    except Exception as erro:
        sessao.rollback()
        raise ErroRegistrar("Erro ao registrar MatriculaTurma") from erro
    finally:
        sessao.close()

def buscar_todos_MatriculaTurmas():
    sessao = sessao_local()
    try:
        resultados = sessao.query(MatriculaTurma).all()
        for r in resultados:
            sessao.expunge(r)
        return resultados
    finally:
        sessao.close()

def contar_MatriculaTurmas():
    sessao = sessao_local()
    try:
        resultado = sessao.query(MatriculaTurma).count()
        return resultado
    finally:
        sessao.close()


def buscar_HistoricoAluno_por_nome(nome_aluno):
    sessao = sessao_local()

    try:
        resultados = (
            sessao.query(MatriculaTurma)
            .join(MatriculaTurma.aluno)
            .filter(Aluno.nome == nome_aluno)
            .all()
        )

        if not resultados:
            raise ErroNaoEncontrado(
                f"Historico não encontrado (Nome Aluno={nome_aluno})"
            )

        return [
            {
                "Id": item.id,
                "Turma": item.turma.nome if item.turma else None,
                "Aluno": item.aluno.nome if item.aluno else None,
                "Data Entrada": item.data_Entrada,
                "Data Saida": item.data_Saida,
                "status": item.status
            }
            for item in resultados
        ]

    except ErroNaoEncontrado:
        raise
    finally:
        sessao.close()

def atualizar_MatriculaTurma(id_MatriculaTurma, nova_MatriculaTurma):
    sessao = sessao_local()
    try:
        MatriculaTurma = sessao.query(MatriculaTurma).filter(MatriculaTurma.id == id_MatriculaTurma).first()
        if MatriculaTurma is None:
            raise ErroNaoEncontrado(f"MatriculaTurma nao encontrado (id={id_MatriculaTurma})")
        if nova_MatriculaTurma is not None:
            MatriculaTurma.valor = nova_MatriculaTurma
        
        sessao.commit()
        sessao.refresh(MatriculaTurma)
        sessao.expunge(MatriculaTurma)
        return MatriculaTurma
    except ErroNaoEncontrado:
        raise
    except Exception as erro:
        sessao.rollback()
        raise ErroAtualizar(f"Erro ao atualizar MatriculaTurma (id={id_MatriculaTurma})") from erro
    finally:
        sessao.close()

def deletar_MatriculaTurma(id_MatriculaTurma):
    sessao = sessao_local()
    try:
        MatriculaTurma = sessao.query(MatriculaTurma).filter(MatriculaTurma.id == id_MatriculaTurma).first()
        if MatriculaTurma is None:
            raise ErroNaoEncontrado(f"MatriculaTurma nao encontrado (id={id_MatriculaTurma})")
        sessao.delete(MatriculaTurma)
        sessao.commit()
        return True
    except ErroNaoEncontrado:
        raise
    except Exception as erro:
        sessao.rollback()
        raise ErroExcluir(f"Erro ao excluir MatriculaTurma (id={id_MatriculaTurma})") from erro
    finally:
        sessao.close()