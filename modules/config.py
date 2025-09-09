# sky-systems/crm/modules/config.py
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def __init__(self):
        self.host = "db_agent"
        self.port = "3306"
        self.user = "root"
        self.password = "sdfdsfs1110477"
        self.database = "agent"
        self.connection = None
        self.cursor = None

    def connect_bd(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=int(self.port),
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except Error as e:
            print("[ERROR_CONNECT_BD]: ", str(e))
            raise Exception(f"Error al conectar a la base de datos: {e}")

    def query(self, query, params=None):
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connect_bd()
            self.cursor.execute(query, params or ())
            if "SELECT" in query:
                return self.cursor.fetchall()
            else:
                self.connection.commit()
        except Error as e:
            if self.connection is not None:
                self.connection.rollback()
            raise Exception(f"Error al ejecutar la consulta: {e}")
        finally:
            self.close()

    def insert_query(self, query, params=None):
        """Ejecuta una consulta de inserción y devuelve el ID del registro insertado."""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connect_bd()
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            if self.connection is not None:
                self.connection.rollback()
            print("[ERROR_INSERT_QUERY]: ",str(e) )
            raise Exception(f"Error al ejecutar la consulta de inserción: {e}")
        finally:
            self.close()

    def bulk_query(self, query, params_list):
        """
        Ejecuta una consulta en lote (bulk insert/update) utilizando `executemany`.

        Parámetros:
        ----------
        query : str
            Consulta SQL con placeholders (%s).
        params_list : list
            Lista de tuplas con los parámetros para cada ejecución.

        Retorna:
        --------
        int : Cantidad de filas afectadas.

        Excepción:
        ----------
        Lanza una excepción si ocurre un error durante la ejecución.
        """
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connect_bd()
            self.cursor.executemany(query, params_list)
            self.connection.commit()
            return self.cursor.rowcount  # Devuelve la cantidad de filas afectadas
        except Error as e:
            if self.connection is not None:
                self.connection.rollback()
            raise Exception(f"Error al ejecutar la consulta en lote: {e}")
        finally:
            self.close()

    def start_transaction(self):
        """Inicia una transacción."""
        if self.connection is None or not self.connection.is_connected():
            self.connect_bd()
        self.connection.start_transaction()

    def commit(self):
        """Confirma la transacción actual."""
        if self.connection is not None:
            self.connection.commit()

    def rollback(self):
        """Revierte la transacción actual."""
        if self.connection is not None:
            self.connection.rollback()

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.connection is not None:
            self.connection.close()
            self.connection = None