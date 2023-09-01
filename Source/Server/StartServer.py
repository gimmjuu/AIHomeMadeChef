from Server import Server
from Source.Common.DBConnector import DBConnector


if __name__ == '__main__':
    print("***서버 가동중****")
    db_conn = DBConnector()
    server = Server(db_conn)
    server.start()
