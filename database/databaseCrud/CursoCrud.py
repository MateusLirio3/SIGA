from database.database_conection import sessao_local
from sqlalchemy.orm import make_transient
from database.models.Curso import Curso
from .Erros import ErroExcluir, ErroNaoEncontrado, ErroRegistrar, ErroAtualizar

def criar_Curso(nome):
    
    sessao = sessao_local()
    try:
        novo = Curso(
            nome=nome
        )
        sessao.add(novo)
        sessao.commit()
        sessao.refresh(novo)
        sessao.expunge(novo)
        return novo
    except Exception as erro:
        sessao.rollback()
        raise ErroRegistrar(f"Erro ao registrar Curso (nome={nome})") from erro
    finally:
        sessao.close()

def buscar_todos_Cursos():
    sessao = sessao_local()
    try:
        resultados = sessao.query(Curso).all()
        for r in resultados:
            sessao.expunge(r)
        return resultados
    finally:
        sessao.close()

def contar_Cursos():
    sessao = sessao_local()
    try:
        resultado = sessao.query(Curso).count()
        return resultado
    finally:
        sessao.close()


def buscar_Curso_por_nome(nome):
    sessao = sessao_local()
    try:
        resultado = sessao.query(Curso).filter(Curso.nome == nome).first()
        if resultado is None:
            raise ErroNaoEncontrado(f"Curso nao encontrado (nome={nome})")

        sessao.refresh(resultado)
        resultado.id
        resultado.nome

        sessao.expunge(resultado)
        make_transient(resultado)
        return resultado
    except ErroNaoEncontrado:
        raise
    finally:
        sessao.close()

def atualizar_Curso(nome, novo_nome, nova_descricao):
    sessao = sessao_local()
    try:
        Curso = sessao.query(Curso).filter(Curso.nome == nome).first()
        if Curso is None:
            raise ErroNaoEncontrado(f"Curso nao encontrado (nome={nome})")
        if (novo_nome is not None) and (nova_descricao is not None):
            Curso.nome = novo_nome
            Curso.descricao = nova_descricao
        
        sessao.commit()
        sessao.refresh(Curso)
        sessao.expunge(Curso)
        return Curso
    except ErroNaoEncontrado:
        raise
    except Exception as erro:
        sessao.rollback()
        raise ErroAtualizar(f"Erro ao atualizar Curso (nome={nome})") from erro
    finally:
        sessao.close()


def deletar_Curso(nome):
    sessao = sessao_local()
    try:
        Curso = sessao.query(Curso).filter(Curso.nome == nome).first()
        if Curso is None:
            raise ErroNaoEncontrado(f"Curso nao encontrado (nome={nome})")
        sessao.delete(Curso)
        sessao.commit()
        return True
    except ErroNaoEncontrado:
        raise
    except Exception as erro:
        sessao.rollback()
        raise ErroExcluir(f"Erro ao excluir Curso (nome={nome})") from erro
    finally:
        sessao.close()