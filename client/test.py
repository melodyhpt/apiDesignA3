import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
import inventory_client
import get_book_titles

SERVER_URL = "localhost"
SERVER_PORT = 50051
ISBN_LIST = ["9780786838653", "9781476753164"]
TITLE_LIST = ["The Lightning Thief (Percy Jackson and the Olympians, Book 1)", "Maybe Someday"]

def side_effect_func(isbn):
    index = ISBN_LIST.index(isbn)
    if index >= 0:
        return TITLE_LIST[index]

class TestGetBookTitles(unittest.TestCase):
    def test_get_book_titles_without_server(self):
        print("Testing get book titles without server")
        inventoryCient = inventory_client.InventoryClient(None,None)
        inventoryCient.getBookTitle = MagicMock(side_effect=side_effect_func)
        bookTitles = get_book_titles.getBookTitles(inventoryCient, ISBN_LIST)

        self.assertEqual(bookTitles, TITLE_LIST)
        print("Get book titles without server test passed")

    
    def test_get_book_titles_with_server(self):
        print("Testing get book titles with server")
        inventoryCient = inventory_client.InventoryClient(SERVER_URL,SERVER_PORT)
        bookTitles = get_book_titles.getBookTitles(inventoryCient, ISBN_LIST)
        self.assertEqual(bookTitles, TITLE_LIST)
        print("Get book titles with server test passed")

if __name__ == '__main__':
    unittest.main()