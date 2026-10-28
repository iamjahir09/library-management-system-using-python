from django.contrib import admin
from .models import Book, BorrowRecord

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "isbn", "available_copies", "total_copies")
    list_filter = ("category",)
    search_fields = ("title", "author", "isbn")
    ordering = ("title",)

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ("book", "member", "issued_at", "due_date", "returned_at", "status")
    list_filter = ("status", "issued_at", "due_date")
    search_fields = ("book__title", "member__username", "member__email")
    readonly_fields = ("issued_at", "returned_at")
