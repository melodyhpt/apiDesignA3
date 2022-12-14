from concurrent import futures
import logging

import grpc
import inventory_service_pb2
import inventory_service_pb2_grpc


inventory = {
    "9780786838653": {
        "isbn": "9780786838653",
        "title": "The Lightning Thief (Percy Jackson and the Olympians, Book 1)",
        "author": "Rick Riordan",
        "genre": "GENRE_THRILLER",
        "year": 2006
    },
    "9781476753164": {
        "isbn":  "9781476753164",
        "title": "Maybe Someday",
        "author": "Colleen Hoover",
        "genre": "GENRE_ROMANCE",
        "year": 2014
    },
}

def required_field_provided(book):
    missingField = []
    if book.isbn == "":
        missingField.append("isbn")
    if book.title == "":
        missingField.append("title")
    if book.author == "":
        missingField.append("author")
    if book.genre == 0:
        missingField.append("genre")

    if len(missingField) > 0:
        return "The following fields are required but not provided: " + ", ".join(missingField)
    

class BookService(inventory_service_pb2_grpc.BookServiceServicer):

    def CreateBook(self, request, context):
        print("request", request.book)
        # check all required fields are provided
        errMsg = required_field_provided(request.book)
        if errMsg:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(errMsg)
            return inventory_service_pb2.CreateBookResponse()

        # add book to inventory
        inventory[request.book.isbn] = request.book
        context.set_code(grpc.StatusCode.OK)
        context.set_details("Book created")
        return inventory_service_pb2.CreateBookResponse(statusCode=grpc.StatusCode.OK.value[0])

    def GetBook(self, request, context):
        # check isbn is provided
        if request.isbn == "":
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("ISBN not provided")
            return inventory_service_pb2.GetBookResponse()

        # check isbn exists in inventory
        if request.isbn not in inventory:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Book not found")
            return inventory_service_pb2.GetBookResponse()

        return inventory_service_pb2.GetBookResponse(book=inventory[request.isbn])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inventory_service_pb2_grpc.add_BookServiceServicer_to_server(BookService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()