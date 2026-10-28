from datetime import timedelta
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

def default_due_date():
    return timezone.localdate() + timedelta(days=14)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    isbn = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=100, default="General", db_index=True)
    description = models.TextField(blank=True)
    publisher = models.CharField(max_length=150, blank=True)
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    total_copies = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    available_copies = models.PositiveIntegerField(default=1)
    cover_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} — {self.author}"

    @property
    def is_available(self):
        return self.available_copies > 0

class BorrowRecord(models.Model):
    class Status(models.TextChoices):
        ISSUED = "ISSUED", "Issued"
        RETURNED = "RETURNED", "Returned"

    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="borrow_records")
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrow_records")
    issued_at = models.DateField(default=timezone.localdate)
    due_date = models.DateField(default=default_due_date)
    returned_at = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ISSUED, db_index=True)

    class Meta:
        ordering = ["-issued_at", "-id"]
        constraints = [
            models.CheckConstraint(condition=models.Q(due_date__gte=models.F("issued_at")), name="due_date_not_before_issue_date"),
        ]

    def __str__(self):
        return f"{self.book.title} → {self.member.username} ({self.status})"

    @property
    def is_overdue(self):
        return self.status == self.Status.ISSUED and self.due_date < timezone.localdate()
