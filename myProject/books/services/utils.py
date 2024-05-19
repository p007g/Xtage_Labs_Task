import requests

class GoogleBooksClient:
    
    url = "https://www.googleapis.com/books/v1/volumes"
    API_KEY = "AIzaSyBvM_EvKXT5jaE3D5TNxc6rY9isWOqT-VY"

    @staticmethod
    def search_books(query):
        # query = "harry potter"
        params = {"q": query, "key": GoogleBooksClient.API_KEY}
        response = requests.get(GoogleBooksClient.url, params=params)
        return response.json()
    
    
    @staticmethod
    def get_book(book_id):
        params = {'key': GoogleBooksClient.API_KEY}
        response = requests.get(f"{GoogleBooksClient.url}/{book_id},", params=params)
        return response.json()