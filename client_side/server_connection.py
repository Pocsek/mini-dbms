from socket import *


class ServerConnection:
    """
    A class that represents a connection to a server.
    """
    __sock: socket

    def __init__(self, host: str, port: int):
        self.__sock: socket = socket(AF_INET, SOCK_STREAM)
        self.connect(host, port)

    def connect(self, host: str, port: int):
        self.__sock.connect((host, port))

    def send(self, data: str):
        """
        Send data to the server after sending the length of the data.
        """
        data_length: int = len(data)
        self.__sock.sendall(data_length.to_bytes(4, byteorder="big"))  # send the length of the data
        self.__sock.sendall(data.encode())  # send the data

    def receive(self) -> str:
        """
        Receive data from the server after receiving the length of the data.
        """
        response_length: int = int.from_bytes(self.__sock.recv(4), byteorder="big")  # receive the length of the data
        return self.__sock.recv(response_length).decode()  # receive the data

    def close(self):
        self.__sock.close()
