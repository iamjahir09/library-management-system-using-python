from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Book, BorrowRecord

class LibraryFlowTests(TestCase):
    def setUp(self):
        self.member = User.objects.create_user(username="reader", password="StrongTestPass123!")
        self.book = Book.objects.create(title="Test Book", author="Test Author", isbn="TEST-001", category="Testing", total_copies=2, available_copies=2)

    def test_catalogue_is_public(self):
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")

    def test_member_can_borrow_available_book(self):
        self.client.login(username="reader", password="StrongTestPass123!")
        response = self.client.post(reverse("borrow_book", args=[self.book.pk]))
        self.book.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.book.available_copies, 1)
        self.assertTrue(BorrowRecord.objects.filter(member=self.member, book=self.book, status=BorrowRecord.Status.ISSUED).exists())

    def test_borrowing_requires_login(self):
        response = self.client.post(reverse("borrow_book", args=[self.book.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response.headers["Location"].startswith(reverse("login"))
        )

    def test_return_restores_available_copy(self):
        record = BorrowRecord.objects.create(member=self.member, book=self.book, due_date=timezone.localdate() + timedelta(days=14))
        self.book.available_copies = 1
        self.book.save()
        self.client.login(username="reader", password="StrongTestPass123!")
        self.client.post(reverse("return_book", args=[record.pk]))
        self.book.refresh_from_db()
        record.refresh_from_db()
        self.assertEqual(self.book.available_copies, 2)
        self.assertEqual(record.status, BorrowRecord.Status.RETURNED)
