import hashlib
from sqlalchemy import Column, String
from database.database_conection import classe_base
from .ulid_Generator import TipoULID, gerar_ulid
import bcrypt


class Usuario(classe_base):

    __tablename__ = "usuarios"

    id         = Column(TipoULID, primary_key=True, default=gerar_ulid)
    nome       = Column(String(256), nullable=False)
    email      = Column(String(256), nullable=False)
    email_hash = Column(String(64), nullable=False, unique=True)
    senha      = Column(String(60), nullable=False)
    tipo       = Column(String(60), nullable = False)
    cpf        = Column(String(11), nullable=False)

    __mapper_args__ = {
        "polymorphic_on" : tipo
    }

    def definir_senha(self, senha_pura: str):
        self.senha = bcrypt.hashpw(senha_pura.encode(), bcrypt.gensalt()).decode()

    def verificar_senha(self, senha_pura: str) -> bool:
        return bcrypt.checkpw(senha_pura.encode(), self.senha.encode())

    @staticmethod
    def hash_email(email: str) -> str:
        """Gera o SHA-256 do email para uso como índice de busca."""
        return hashlib.sha256(email.strip().lower().encode()).hexdigest()