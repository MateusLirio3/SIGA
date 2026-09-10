from database.database_conection import sessao_local
from database.models.Professor import Professor
from database.models.Usuario import Usuario
from database.models.Disciplina import Disciplina
from database.models.DisciplinaTurma import DisciplinaTurma
from database.models.Nota import Nota
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
        linhas = (
            sessao.query(Professor, Disciplina.nome)
            .outerjoin(
                DisciplinaTurma,
                DisciplinaTurma.id_professor == Professor.id
            )
            .outerjoin(
                Disciplina,
                Disciplina.id == DisciplinaTurma.id_disciplina
            )
            .all()
        )

        professores = {}
        for professor, nome_disciplina in linhas:
            professor_id = str(professor.id)
            if professor_id not in professores:
                professores[professor_id] = {
                    "id": professor.id,
                    "nome": professor.nome,
                    "matricula": professor.matricula,
                    "cpf": professor.cpf,
                    "email": professor.email,
                    "disciplinas": [],
                }
            if nome_disciplina and nome_disciplina not in professores[professor_id]["disciplinas"]:
                professores[professor_id]["disciplinas"].append(nome_disciplina)

        return list(professores.values())
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

def buscar_Professor_por_nome(nome):
    sessao = sessao_local()

    try:
        resultado = sessao.query(Professor).filter(Professor.nome == nome).first()
        if resultado is None:
            raise ErroNaoEncontrado(f"Professor nao encontrado (nome = {nome})")
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

def atualizar_Professor(id_professor, novo_nome=None, nova_matricula=None, novo_cpf=None, novo_email=None):
    sessao = sessao_local()
    try:
        professor = sessao.query(Professor).filter(Professor.id == id_professor).first()
        if professor is None:
            raise ErroNaoEncontrado(f"Professor nao encontrado (id={id_professor})")
        if novo_nome is not None:
            professor.nome = novo_nome
        if nova_matricula is not None:
            professor.matricula = nova_matricula
        if novo_cpf is not None:
            professor.cpf = novo_cpf
        if novo_email is not None:
            professor.email = novo_email
            professor.email_hash = Usuario.hash_email(novo_email)
        
        sessao.commit()
        sessao.refresh(professor)
        sessao.expunge(professor)
        return professor
    except ErroNaoEncontrado:
        raise
    except Exception as erro:
        sessao.rollback()
        raise ErroAtualizar(f"Erro ao atualizar Professor (id={id_professor})") from erro
    finally:
        sessao.close()


def deletar_Professor(id_professor):
    sessao = sessao_local()
    try:
        professor = sessao.query(Professor).filter(Professor.id == id_professor).first()
        if professor is None:
            raise ErroNaoEncontrado(f"Professor nao encontrado (id={id_professor})")
        sessao.delete(professor)
        sessao.commit()
        return True
    except ErroNaoEncontrado:
        raise
    except Exception as erro:
        sessao.rollback()
        raise ErroExcluir(f"Erro ao excluir Professor (id={id_professor})") from erro
    finally:
        sessao.close()