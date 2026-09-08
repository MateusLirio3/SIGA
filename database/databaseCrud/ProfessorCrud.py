from database.database_conection import sessao_local
from database.models.Professor import Professor
from database.models.Usuario import Usuario
from sqlalchemy.orm import make_transient
from .Erros import ErroExcluir, ErroNaoEncontrado, ErroRegistrar, ErroAtualizar

def criar_Professor(nome, email, senha, matricula, cpf):
    
    sessao = sessao_local()
    try:
        novo = Professor(
            matricula=matricula,
            nome=nome,
            email=email,
            email_hash=Usuario.hash_email(email),
            cpf=cpf
        )
        novo.definir_senha(senha)
        sessao.add(novo)
        sessao.commit()
        sessao.refresh(novo)
        sessao.expunge(novo)
        return novo
    except Exception as erro:
        sessao.rollback()
        raise ErroRegistrar(f"Erro ao registrar Professor (matricula={matricula})") from erro
    finally:
        sessao.close()

def buscar_todos_Professores():
    sessao = sessao_local()
    try:
        resultados = sessao.query(Professor).all()
        for r in resultados:
            sessao.expunge(r)
        return resultados
    finally:
        sessao.close()

def contar_Professores():
    sessao = sessao_local()
    try:
        resultado = sessao.query(Professor).count()
        return resultado
    finally:
        sessao.close()


def autenticar_Professor(matricula, senha):

    sessao = sessao_local()
    try:
        Professor = sessao.query(Professor).filter(
            Professor.matricula == matricula
        ).first()

        if Professor is None:
            raise ErroNaoEncontrado(f"Professor nao encontrado (matricula={matricula})")
        if not Professor.verificar_senha(senha):
            return None

        _ = Professor.id, Professor.matricula,

        sessao.expunge(Professor)
        return Professor
    except ErroNaoEncontrado:
        raise
    finally:
        sessao.close()

def buscar_Professor_por_matricula(matricula):
    sessao = sessao_local()
    try:
        resultado = sessao.query(Professor).filter(Professor.matricula == matricula).first()
        if resultado is None:
            raise ErroNaoEncontrado(f"Professor nao encontrado (matricula={matricula})")

        sessao.refresh(resultado)
        resultado.id
        resultado.matricula


        sessao.expunge(resultado)
        make_transient(resultado)
        return resultado
    except ErroNaoEncontrado:
        raise
    finally:
        sessao.close()

def atualizar_Professor(matricula, nova_matricula):
    sessao = sessao_local()
    try:
        Professor = sessao.query(Professor).filter(Professor.matricula == matricula).first()
        if Professor is None:
            raise ErroNaoEncontrado(f"Professor nao encontrado (matricula={matricula})")
        if nova_matricula is not None:
            Professor.matricula = nova_matricula
        
        sessao.commit()
        sessao.refresh(Professor)
        sessao.expunge(Professor)
        return Professor
    except ErroNaoEncontrado:
        raise
    except Exception as erro:
        sessao.rollback()
        raise ErroAtualizar(f"Erro ao atualizar Professor (matricula={matricula})") from erro
    finally:
        sessao.close()


def deletar_Professor(matricula):
    sessao = sessao_local()
    try:
        Professor = sessao.query(Professor).filter(Professor.matricula == matricula).first()
        if Professor is None:
            raise ErroNaoEncontrado(f"Professor nao encontrado (matricula={matricula})")
        sessao.delete(Professor)
        sessao.commit()
        return True
    except ErroNaoEncontrado:
        raise
    except Exception as erro:
        sessao.rollback()
        raise ErroExcluir(f"Erro ao excluir Professor (matricula={matricula})") from erro
    finally:
        sessao.close()