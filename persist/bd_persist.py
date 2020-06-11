import sqlite3
from datetime import datetime as dt


class Conexao:

    def __init__(self, caminho_bd):
        try:
            self.conn = sqlite3.connect(caminho_bd)
            self.cursor = self.conn.cursor()
        except sqlite3.Error:
            return False

    def desconectar_bd(self):
        if self.conn:
            self.conn.close()

    def inserir_bd(self, produto, valor, link, item_alvo, valor_alvo):
        try:
            self.cursor.execute("""
            INSERT INTO tb_dados_buscape (produto, valor, link, item_alvo, valor_alvo, data_consulta)
            VALUES (?,?,?,?,?,?)
            """, (produto, valor, link, item_alvo, valor_alvo, dt.now().strftime('%Y-%m-%d %H:%M')))
            self.conn.commit()
            return True
        except sqlite3.Error as err:
            return False

    def consultar_bd(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except sqlite3.Error as err:
            print(err)
            return False

    def atualizar_bd(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            return cursor.fetchall()
        except sqlite3.Error as err:
            print(err)
            return False

    def apagar_bd(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            return cursor.fetchall()
        except sqlite3.Error as err:
            print(err)
            return False
