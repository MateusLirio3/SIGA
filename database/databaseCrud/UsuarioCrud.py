from database.database_conection import sessao_local
from database.models.Usuario import Usuario
from .Erros import ErroExcluir, ErroNaoEncontrado, ErroRegistrar, ErroAtualizar
from sqlalchemy.orm import make_transient
from database.models.Aluno import Aluno

def criar_usuario(nome, email, senha,cpf):
    
    sessao = sessao_local()
    try:
        novo = Usuario(
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
        raise ErroRegistrar(f"Erro ao registrar Usuario (email={email})") from erro
    finally:
        sessao.close()


def buscar_usuario_por_id(id):
    sessao = sessao_local()
    try:
        resultado = sessao.query(Usuario).filter(Usuario.id == id).first()
        if resultado is None:
            raise ErroNaoEncontrado(f"Usuario nao encontrado (id={id})")
        sessao.expunge(resultado)
        return resultado
    except ErroNaoEncontrado:
        raise
    finally:
        sessao.close()


def buscar_usuario_por_email(email):
    sessao = sessao_local()
    try:
        h = Usuario.hash_email(email)
        resultado = sessao.query(Usuario).filter(Usuario.email_hash == h).first()
        if resultado is None:
            raise ErroNaoEncontrado(f"Usuario nao encontrado (email={email})")

        sessao.refresh(resultado)
        resultado.id
        resultado.nome
        resultado.email
        if isinstance(resultado, Aluno):
            resultado.matricula

        sessao.expunge(resultado)
        make_transient(resultado)
        return resultado
    except ErroNaoEncontrado:
        raise
    finally:
        sessao.close()


def buscar_todos_usuarios():
    sessao = sessao_local()
    try:
        resultados = sessao.query(Usuario).all()
        for r in resultados:
            sessao.expunge(r)
        return resultados
    finally:
        sessao.close()


def autenticar_usuario(identificador, senha, sessao):

    import re

    id_limpo     = identificador.strip()
    eh_matricula = bool(re.match(r'^\d{13}$', id_limpo))

    try:
        if eh_matricula:
            h       = Aluno.matricula
            usuario = sessao.query(Aluno).filter(
                Aluno.matricula == h
            ).first()

        else:
            h       = Usuario.hash_email(id_limpo)
            usuario = sessao.query(Usuario).filter(Usuario.email_hash == h).first()

        if usuario is None:
            raise ErroNaoEncontrado(f"Usuario nao encontrado (identificador={identificador})")
        if not usuario.verificar_senha(senha):
            return None

        _ = usuario.id, usuario.nome, usuario.email, usuario.tipo

        sessao.expunge(usuario)
        return usuario
    except ErroNaoEncontrado:
        raise
    finally:
        sessao.close()

def atualizar_usuario(email, novo_nome=None, novo_email=None, nova_senha=None):
    sessao = sessao_local()
    try:
        h = Usuario.hash_email(email)
        usuario = sessao.query(Usuario).filter(Usuario.email_hash == h).first()
        if usuario is None:
            raise ErroNaoEncontrado(f"Usuario nao encontrado (email={email})")
        if novo_nome is not None:
            usuario.nome = novo_nome
        if novo_email is not None:
            usuario.email = novo_email
            usuario.email_hash = Usuario.hash_email(novo_email)  # atualiza o índice
        if nova_senha is not None:
            usuario.definir_senha(nova_senha)
        sessao.commit()
        sessao.refresh(usuario)
        sessao.expunge(usuario)
        return usuario
    except ErroNaoEncontrado:
        raise
    except Exception as erro:
        sessao.rollback()
        raise ErroAtualizar(f"Erro ao atualizar Usuario (email={email})") from erro
    finally:
        sessao.close()


def deletar_usuario(email):
    sessao = sessao_local()
    try:
        h = Usuario.hash_email(email)
        usuario = sessao.query(Usuario).filter(Usuario.email_hash == h).first()
        if usuario is None:
            raise ErroNaoEncontrado(f"Usuario nao encontrado (email={email})")
        sessao.delete(usuario)
        sessao.commit()
        return True
    except ErroNaoEncontrado:
        raise
    except Exception as erro:
        sessao.rollback()
        raise ErroExcluir(f"Erro ao excluir Usuario (email={email})") from erro
    finally:
        sessao.close()