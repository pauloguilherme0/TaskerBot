import sqlite3
import os

from dotenv import load_dotenv

class AtividadeManager:
    load_dotenv()
    def __init__(self, db_name = os.getenv("DB_NAME", "default.db")):
        self.conn = sqlite3.connect(db_name)
        self.conn.execute("CREATE TABLE IF NOT EXISTS atividades (id INTEGER PRIMARY KEY, nome TEXT, status TEXT, tag TEXT, user_id INTEGER, server_id INTEGER)")
        self.conn.commit()

    def __enter__(self):
        self.c = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()

    def inserir_atividade(self, nome, status, tag, user_id, server_id):
        self.c.execute("INSERT INTO atividades (nome, status, tag, user_id, server_id) VALUES (?, ?, ?, ?, ?)", (nome, status, tag, user_id, server_id))
        self.conn.commit()

    def listar_atividades(self, user_id, server_id):
        self.c.execute("SELECT * FROM atividades WHERE user_id = ? AND server_id = ?", (user_id, server_id,))
        atividades = self.c.fetchall()
        output = []
        for atividade in atividades:
            output.append({"id": atividade[0], "nome": atividade[1], "status": atividade[2], "tag": atividade[3]})
        return output

    def limpar_atividades(self):
        self.c.execute("DELETE FROM atividades")
        self.conn.commit()