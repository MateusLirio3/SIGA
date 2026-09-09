from database.database_conection import motor, sessao_local, classe_base
from database.models.Aluno import Aluno
from database.models.Coordenador import Coordenador
from database.models.Usuario import Usuario
from database.models.Turma import Turma
from database.models.Curso import Curso
from database.databaseCrud.TurmaCrud import criar_Turma

ALUNO = {
    "nome": "Aluno Seed",
    "email": "aluno.seed@gmail.com",
    "senha": "Aluno@123",
    "matricula": "2026000000001",
    "cpf" : "12345678910"
}

COORDENADOR = {
    "nome": "Coordenador Seed",
    "email": "coordenador.seed@gmail.com",
    "senha": "Coordenador@123",
    "matricula": "COORD-2026-001",
    "cpf" : "98765432110"
}

TURMA = {
    "nome" : "INF31",
    "periodo" : "Integral",
    "ano" : 2026
}

CURSO = {
    "nome" : "Técnico em Informática"
}

def criar_usuario_se_nao_existir(modelo, dados):
    sessao = sessao_local()
    try:
        usuario = sessao.query(Usuario).filter(
            Usuario.email_hash == Usuario.hash_email(dados["email"])
        ).first()

        if usuario is None:
            usuario = modelo(
                nome=dados["nome"],
                email=dados["email"],
                email_hash=Usuario.hash_email(dados["email"]),
                matricula=dados["matricula"],
                cpf=dados["cpf"]
            )
            usuario.definir_senha(dados["senha"])
            sessao.add(usuario)
            sessao.commit()
            sessao.refresh(usuario)
        sessao.expunge(usuario)
        return usuario
    finally:
        sessao.close()

def criar_turma(modelo, dados):
    sessao = sessao_local()
    try: 
        turma = sessao.query(Turma).filter(
            Turma.nome == dados["nome"]
        ).first()

        if turma is None:
            turma = modelo(
                nome=dados["nome"],
                periodo = dados["periodo"],
                ano = dados['ano']
            )
            sessao.add(turma)
            sessao.commit()
            sessao.refresh(turma)
        sessao.expunge(turma)
        return turma
    finally:
        sessao.close()

def criar_curso(modelo,dados):
    sessao = sessao_local()
    try:    
        curso = sessao.query(Curso).filter(
            Curso.nome == dados["nome"]
        ).first()

        if curso is None:
            curso = modelo(
                nome=dados["nome"],
            )
            sessao.add(curso)
            sessao.commit()
            sessao.refresh(curso)
        sessao.expunge(curso)
    finally:
        sessao.close()
def executar_seed():
    classe_base.metadata.create_all(bind=motor)
    aluno = criar_usuario_se_nao_existir(Aluno, ALUNO)
    coordenador = criar_usuario_se_nao_existir(Coordenador, COORDENADOR)
    turma = criar_turma(Turma, TURMA)
    curso = criar_curso(Curso, CURSO)

if __name__ == "__main__":
    executar_seed()