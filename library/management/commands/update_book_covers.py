
from django.core.management.base import BaseCommand
from library.models import Book


class Command(BaseCommand):
    help = "Update cover image URLs for library books"

    def handle(self, *args, **options):
        updated = 0

        for book in Book.objects.all():
            if book.isbn:
                book.cover_url = (
                    f"https://covers.openlibrary.org/b/isbn/"
                    f"{book.isbn}-L.jpg?default=false"
                )
                book.save(update_fields=["cover_url"])
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Cover URLs updated for {updated} books."
            )
        )
