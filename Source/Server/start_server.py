import sys

# from DataBase.class_DB import DB
from class_server import Server
from db.class_dbconnect import DBConnector

if __name__ == '__main__':
    db_conn = DBConnector(test_option=True)
    server = Server(db_conn)
    server.start()