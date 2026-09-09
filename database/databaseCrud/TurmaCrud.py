from database.database_conection import sessao_local
from database.models.Turma import Turma
from database.models.Curso import Curso
from sqlalchemy.exc import IntegrityError
from .Erros import ErroExcluir, ErroNaoEncontrado, ErroRegistrar, ErroAtualizar
from sqlalchemy.orm import make_transient

def criar_Turma(nome, periodo, id_curso, ano):
    
    sessao = sessao_local()
    try:
        novo = Turma(
            id_curso=id_curso,
            nome=nome,
            periodo=periodo,
            ano = ano

        )
        sessao.add(novo)
        sessao.commit()
        sessao.refresh(novo)
        sessao.expunge(novo)
        return novo
    except Exception as erro:
        sessao.rollback()
        raise ErroRegistrar(f"Erro ao registrar Turma (nome={nome})") from erro
    finally:
        sessao.close()


def buscar_Turma_por_id(id):
    sessao = sessao_local()
    try:
        resultado = sessao.query(Turma).filter(Turma.id == id).first()
        if resultado is None:
            raise ErroNaoEncontrado(f"Turma nao encontrado (id={id})")
        sessao.expunge(resultado)
        return resultado
    except ErroNaoEncontrado:
        raise
    finally:
        sessao.close()


def buscar_Turma_por_nome(nome):
    sessao = sessao_local()
    try:
        resultado = sessao.query(Turma).filter(Turma.nome == nome).first()
        if resultado is None:
            raise ErroNaoEncontrado(f"Turma nao encontrado (nome={nome})")

        sessao.refresh(resultado)
        resultado.id
        resultado.nome
        resultado.periodo

        sessao.expunge(resultado)
        make_transient(resultado)
        return resultado
    except ErroNaoEncontrado:
        raise
    finally:
        sessao.close()


def buscar_todos_Turmas():
    sessao = sessao_local()
    try:
        resultados = sessao.query(Turma).all()
        return [
            {
                "id": item.id,
                "nome": item.nome,
                "curso": item.curso.nome if item.curso else None,
                "periodo": item.periodo,
                "alunos": len(item.matriculas),
                "ano": item.ano
            }
            for item in resultados
        ]
    finally:
        sessao.close()

def atualizar_Turma(id, novo_nome=None, novo_periodo=None, novo_curso=None):
    sessao = sessao_local()
    try:
        turma = sessao.query(Turma).filter(Turma.id == id).first()
        if turma is None:
            raise ErroNaoEncontrado(f"Turma nao encontrado (id={id})")
        if novo_nome is not None:
            turma.nome = novo_nome
        if novo_periodo is not None:
            turma.periodo = novo_periodo
        if novo_curso is not None:
            turma.id_curso = sessao.query(Curso).filter(Curso.nome == novo_curso).first().id
        sessao.commit()
        sessao.refresh(turma)
        sessao.expunge(turma)
        return turma
    except ErroNaoEncontrado:
        raise
    except Exception as erro:
        sessao.rollback()
        raise ErroAtualizar(f"Erro ao atualizar Turma (id={id})") from erro
    finally:
        sessao.close()

def adicionar_Curso(id_Turma, curso):
    sessao = sessao_local()
    try:
        turma = sessao.query(Turma).filter(Turma.id == id_Turma).first()

        if turma is None:
            raise ErroNaoEncontrado(f"Erro ao buscar por turma (id={id_Turma})")

        turma.id_curso = curso
        sessao.commit()
        sessao.refresh(turma)
        sessao.expunge(turma)
        return turma
    except ErroNaoEncontrado:
        raise
    except Exception as erro:
        sessao.rollback()
        raise ErroAtualizar(
            f"Erro ao adicionar o curso (curso={curso}) a turma (id={id_Turma})"
        ) from erro
    finally:
        sessao.close()

def contar_Turmas():
    sessao = sessao_local()
    try:
        resultado = sessao.query(Turma).count()
        return resultado
    finally:
        sessao.close()

def deletar_turma(id):
    sessao = sessao_local()
    try:
        turma = sessao.query(Turma).filter(Turma.id == id).first()

        if turma is None:
            raise ErroNaoEncontrado(f"Turma nao encontrado (id={id})")

        if turma.matriculas:
            raise ErroExcluir(f"A turma possui alunos cadastrados nela.")

        sessao.delete(turma)
        sessao.commit()
        return True
    except ErroNaoEncontrado:
        raise        

    except IntegrityError as erro:
        sessao.rollback()
        raise ErroExcluir(
            f"A turma possui matriculas cadastradas e nao pode ser excluida (id={id})"
        ) from erro

    except Exception as erro:
        sessao.rollback()
        raise ErroExcluir(f"Erro ao excluir Turma (id={id})") from erro
    finally:
        sessao.close()