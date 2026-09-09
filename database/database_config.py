import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('USUARIO_BD')}:{os.getenv('SENHA_BD')}"
    f"@{os.getenv('HOST_BD', 'localhost')}/{os.getenv('NOME_BD', 'siga')}"
)