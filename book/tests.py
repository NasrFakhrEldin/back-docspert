from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from book.models import Book, Page

User = get_user_model()


class BookAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.authorized_client = APIClient()
        self.book = Book.objects.create(
            title="Test Book",
            author=self.user,
            publication_date=timezone.now(),
            price="9.99",
        )
        self.page = Page.objects.create(
            book=self.book, number=1, content="Test page content"
        )
        self.authorized_client.force_authenticate(user=self.user)

    def test_create_book(self):
        data = {
            "title": "New Book",
            "publication_date": "2023-07-01",
            "price": "19.99",
        }
        response = self.authorized_client.post("/api/v1/books/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_get_book_list(self):
        response = self.client.get("/api/v1/books/?pages=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_get_book_detail(self):
        pn = 1
        response = self.client.get(f"/api/v1/books/{self.book.id}/?pn={pn}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Book")
        self.assertEqual(
            response.data["pages"]["results"][0]["content"], "Test page content"
        )

    def test_update_book(self):
        data = {
            "title": "Updated Book",
            "publication_date": "2023-07-01",
            "price": "20.99",
        }
        response = self.authorized_client.put(f"/api/v1/books/{self.book.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Book")

    def test_delete_book(self):
        response = self.authorized_client.delete(f"/api/v1/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_get_page_detail(self):
        response = self.client.get(f"/api/v1/pages/{self.page.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["number"], 1)

    def test_create_page(self):
        data = {"book": self.book.id, "number": 2, "content": "New page content"}
        response = self.authorized_client.post("/api/v1/pages/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Page.objects.count(), 2)
        self.assertEqual(response.data["number"], 2)

    def test_update_page(self):
        data = {"book": self.book.id, "number": 1, "content": "Updated page content"}
        response = self.authorized_client.put(f"/api/v1/pages/{self.page.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Updated page content")

    def test_delete_page(self):
        response = self.authorized_client.delete(f"/api/v1/pages/{self.page.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Page.objects.count(), 0)
