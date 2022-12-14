import grpc
import os
import sys

sys.path.append(os.path.dirname(__file__) + '/..')
sys.path.append(os.path.dirname(__file__) + '/../service')
from service import inventory_service_pb2 
from service import inventory_service_pb2_grpc

class InventoryClient:
    def __init__(self, serverUrl, serverPort):
        self.serverUrl = serverUrl
        self.serverPort = serverPort

    def getBookTitle(self, isbn):
        with grpc.insecure_channel(self.serverUrl + ":" + str(self.serverPort)) as channel:
            stub = inventory_service_pb2_grpc.BookServiceStub(channel)
            try:
                getBookResponse = stub.GetBook(inventory_service_pb2.GetBookRequest(isbn=isbn))
                return getBookResponse.book.title
            except grpc.RpcError as e:
                print(e.code())
