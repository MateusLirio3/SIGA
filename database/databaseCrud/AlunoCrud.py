from database.database_conection import sessao_local
from database.models.Aluno import Aluno
from database.models.Usuario import Usuario
from database.models.MatriculaTurma import MatriculaTurma
from database.models.Turma import Turma
from database.models.Status import Status
from sqlalchemy.orm import make_transient
from sqlalchemy import func
from .Erros import ErroExcluir, ErroNaoEncontrado, ErroRegistrar, ErroAtualizar

def criar_Aluno(nome, email, senha, matricula,cpf):
    
    sessao = sessao_local()
    try:
        novo = Aluno(
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
        raise ErroRegistrar(f"Erro ao registrar Aluno (matricula={matricula})") from erro
    finally:
        sessao.close()

def buscar_todos_Alunos():
    sessao = sessao_local()
    try:
        ultima_matricula = (
            sessao.query(
                MatriculaTurma.id_aluno,
                func.max(MatriculaTurma.data_Entrada).label("ultima_entrada"),
            )
            .group_by(MatriculaTurma.id_aluno)
            .subquery()
        )

        resultados = (
            sessao.query(Aluno, Turma, MatriculaTurma)
            .outerjoin(
                ultima_matricula,
                ultima_matricula.c.id_aluno == Aluno.id,
            )
            .outerjoin(
                MatriculaTurma,
                (MatriculaTurma.id_aluno == Aluno.id)
                & (
                    MatriculaTurma.data_Entrada
                    == ultima_matricula.c.ultima_entrada
                ),
            )
            .outerjoin(Turma, Turma.id == MatriculaTurma.id_turma)
            .all()
        )

        return [
            {
                "id": aluno.id,
                "nome": aluno.nome,
                "matricula": aluno.matricula,
                "cpf": aluno.cpf,
                "email": aluno.email,
                "turma": turma.nome if turma else None,
                "status": matricula.status.value if matricula else None,
            }
            for aluno, turma, matricula in resultados
        ]
    finally:
        sessao.close()

def contar_Alunos():
    sessao = sessao_local()
    try:
        resultado = sessao.query(Aluno).count()
        return resultado
    finally:
        sessao.close()


def autenticar_Aluno(matricula, senha):

    sessao = sessao_local()
    try:
        Aluno = sessao.query(Aluno).filter(
            Aluno.matricula == matricula
        ).first()

        if Aluno is None:
            raise ErroNaoEncontrado(f"Aluno nao encontrado (matricula={matricula})")
        if not Aluno.verificar_senha(senha):
            return None

        _ = Aluno.id, Aluno.matricula,

        sessao.expunge(Aluno)
        return Aluno
    except ErroNaoEncontrado:
        raise
    finally:
        sessao.close()

def buscar_Aluno_por_matricula(matricula):
    sessao = sessao_local()
    try:
        resultado = sessao.query(Aluno).filter(Aluno.matricula == matricula).first()
        if resultado is None:
            raise ErroNaoEncontrado(f"Aluno nao encontrado (matricula={matricula})")

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

def buscar_Aluno_por_cpf(cpf):
    sessao = sessao_local()
    try:
        resultado = sessao.query(Aluno).filter(Aluno.cpf == cpf).first()
        if resultado is None:
            raise ErroNaoEncontrado(f"Aluno nao encontrado (cpf={cpf})")

        sessao.refresh(resultado)
        resultado.id

        sessao.expunge(resultado)
        make_transient(resultado)
        return resultado
    except ErroNaoEncontrado:
        raise
    finally:
        sessao.close()

def atualizar_Aluno(matricula, nova_matricula):
    sessao = sessao_local()
    try:
        Aluno = sessao.query(Aluno).filter(Aluno.matricula == matricula).first()
        if Aluno is None:
            raise ErroNaoEncontrado(f"Aluno nao encontrado (matricula={matricula})")
        if nova_matricula is not None:
            Aluno.matricula = nova_matricula
        
        sessao.commit()
        sessao.refresh(Aluno)
        sessao.expunge(Aluno)
        return Aluno
    except ErroNaoEncontrado:
        raise
    except Exception as erro:
        sessao.rollback()
        raise ErroAtualizar(f"Erro ao atualizar Aluno (matricula={matricula})") from erro
    finally:
        sessao.close()


def atualizar_dados_Aluno(id_aluno, nome, matricula, cpf, email, turma, status):
    sessao = sessao_local()
    try:
        aluno = sessao.query(Aluno).filter(Aluno.id == id_aluno).first()
        if aluno is None:
            raise ErroNaoEncontrado(f"Aluno nao encontrado (id={id_aluno})")

        turma_obj = sessao.query(Turma).filter(Turma.nome == turma).first()
        if turma_obj is None:
            raise ErroNaoEncontrado(f"Turma nao encontrada (nome={turma})")

        matricula_obj = (
            sessao.query(MatriculaTurma)
            .filter(MatriculaTurma.id_aluno == aluno.id)
            .order_by(MatriculaTurma.data_Entrada.desc())
            .first()
        )
        if matricula_obj is None:
            raise ErroNaoEncontrado(
                f"Matricula nao encontrada (id_aluno={id_aluno})"
            )

        aluno.nome = nome
        aluno.matricula = matricula
        aluno.cpf = cpf
        aluno.email = email
        matricula_obj.id_turma = turma_obj.id
        matricula_obj.status = status

        sessao.commit()
        return {
            "id": aluno.id,
            "nome": aluno.nome,
            "matricula": aluno.matricula,
            "cpf": aluno.cpf,
            "email": aluno.email,
            "turma": turma_obj.nome,
            "status": matricula_obj.status.value,
        }
    except ErroNaoEncontrado:
        sessao.rollback()
        raise
    except Exception as erro:
        sessao.rollback()
        raise ErroAtualizar(f"Erro ao atualizar Aluno (id={id_aluno})") from erro
    finally:
        sessao.close()


def deletar_Aluno(id):
    sessao = sessao_local()
    try:
        aluno = sessao.query(Aluno).filter(Aluno.id == id).first()
        if aluno is None:
            raise ErroNaoEncontrado(f"Aluno nao encontrado (id={id})")

        sessao.query(MatriculaTurma).filter(
            MatriculaTurma.id_aluno == aluno.id
        ).delete(synchronize_session=False)
        sessao.delete(aluno)
        sessao.commit()
        return True
    except ErroNaoEncontrado:
        raise
    except Exception as erro:
        sessao.rollback()
        raise ErroExcluir(f"Erro ao excluir Aluno (id={id})") from erro
    finally:
        sessao.close()