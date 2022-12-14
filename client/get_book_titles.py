import inventory_client

DEFAULT_SERVER_URL = "localhost"
DEFAULT_SERVER_PORT = 50051
DEFAULT_ISBN_LIST = ["9780786838653", "9781476753164"]

def getBookTitles(inventoryClient, isbnList):
    # check inventoryClient is type InventoryClient
    if isinstance(inventoryClient, inventory_client.InventoryClient):
        bookTitles = []
        for isbn in isbnList:
            bookTitle = inventoryClient.getBookTitle(isbn)
            if (bookTitle):
                bookTitles.append(bookTitle)
        
        return bookTitles
    else:
        raise Exception("InventoryClient not provided")

if __name__ == "__main__":
    inventoryClient = inventory_client.InventoryClient(DEFAULT_SERVER_URL, DEFAULT_SERVER_PORT)
    bookTitles = getBookTitles(inventoryClient, DEFAULT_ISBN_LIST)
    print(", ".join(bookTitles))


    