from database.database_conection import sessao_local
from database.models.Coordenador import Coordenador
from database.models.Usuario import Usuario
from .Erros import ErroExcluir, ErroNaoEncontrado, ErroRegistrar, ErroAtualizar
from sqlalchemy.orm import make_transient

def criar_Coordenador(nome, email, senha, matricula, cpf):
    
    sessao = sessao_local()
    try:
        novo = Coordenador(
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
        raise ErroRegistrar(f"Erro ao registrar Coordenador (matricula={matricula})") from erro
    finally:
        sessao.close()

def buscar_todos_Coordenadors():
    sessao = sessao_local()
    try:
        resultados = sessao.query(Coordenador).all()
        for r in resultados:
            sessao.expunge(r)
        return resultados
    finally:
        sessao.close()

def buscar_Coordenador_por_matricula(matricula):
    sessao = sessao_local()
    try:
        resultado = sessao.query(Coordenador).filter(Coordenador.matricula == matricula).first()
        if resultado is None:
            raise ErroNaoEncontrado(f"Coordenador nao encontrado (matricula={matricula})")

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

def contar_Coordenador():
    sessao = sessao_local()
    try:
        resultado = sessao.query(Coordenador).count()
        return resultado
    finally:
        sessao.close()

def autenticar_Coordenador(matricula, senha):

    sessao = sessao_local()
    try:
        Coordenador = sessao.query(Coordenador).filter(
            Coordenador.matricula == matricula
        ).first()

        if Coordenador is None:
            raise ErroNaoEncontrado(f"Coordenador nao encontrado (matricula={matricula})")
        if not Coordenador.verificar_senha(senha):
            return None

        _ = Coordenador.id, Coordenador.matricula,

        sessao.expunge(Coordenador)
        return Coordenador
    except ErroNaoEncontrado:
        raise
    finally:
        sessao.close()

def atualizar_Coordenador(matricula, nova_matricula):
    sessao = sessao_local()
    try:
        Coordenador = sessao.query(Coordenador).filter(Coordenador.matricula == matricula).first()
        if Coordenador is None:
            raise ErroNaoEncontrado(f"Coordenador nao encontrado (matricula={matricula})")
        if nova_matricula is not None:
            Coordenador.matricula = nova_matricula
        
        sessao.commit()
        sessao.refresh(Coordenador)
        sessao.expunge(Coordenador)
        return Coordenador
    except ErroNaoEncontrado:
        raise
    except Exception as erro:
        sessao.rollback()
        raise ErroAtualizar(f"Erro ao atualizar Coordenador (matricula={matricula})") from erro
    finally:
        sessao.close()


def deletar_Coordenador(matricula):
    sessao = sessao_local()
    try:
        Coordenador = sessao.query(Coordenador).filter(Coordenador.matricula == matricula).first()
        if Coordenador is None:
            raise ErroNaoEncontrado(f"Coordenador nao encontrado (matricula={matricula})")
        sessao.delete(Coordenador)
        sessao.commit()
        return True
    except ErroNaoEncontrado:
        raise
    except Exception as erro:
        sessao.rollback()
        raise ErroExcluir(f"Erro ao excluir Coordenador (matricula={matricula})") from erro
    finally:
        sessao.close()