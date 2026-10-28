from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import BookForm, SignUpForm
from .models import Book, BorrowRecord


def home(request):
    featured_books = Book.objects.all()[:6]
    return render(request, "library/home.html", {"featured_books": featured_books, "book_count": Book.objects.count()})


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("dashboard")
    return render(request, "library/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get("next") or "dashboard")
        error = "Invalid username or password. Please try again."
    return render(request, "library/login.html", {"error": error})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "You have been logged out.")
    return redirect("home")


@login_required
def dashboard(request):
    if request.user.is_staff:
        context = {
            "is_admin": True,
            "book_count": Book.objects.count(),
            "member_count": User.objects.filter(is_staff=False, is_superuser=False).count(),
            "active_loans": BorrowRecord.objects.filter(status=BorrowRecord.Status.ISSUED).count(),
            "overdue_count": BorrowRecord.objects.filter(status=BorrowRecord.Status.ISSUED, due_date__lt=timezone.localdate()).count(),
            "recent_records": BorrowRecord.objects.select_related("book", "member")[:8],
        }
    else:
        records = BorrowRecord.objects.filter(member=request.user).select_related("book")
        context = {
            "is_admin": False,
            "active_loans": records.filter(status=BorrowRecord.Status.ISSUED).count(),
            "returned_count": records.filter(status=BorrowRecord.Status.RETURNED).count(),
            "overdue_count": records.filter(status=BorrowRecord.Status.ISSUED, due_date__lt=timezone.localdate()).count(),
            "recent_records": records[:8],
        }
    return render(request, "library/dashboard.html", context)


def book_list(request):
    books = Book.objects.all()
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query) | Q(isbn__icontains=query) | Q(category__icontains=query))
    if category:
        books = books.filter(category__iexact=category)
    categories = Book.objects.order_by("category").values_list("category", flat=True).distinct()
    paginator = Paginator(books, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "library/book_list.html", {"page_obj": page_obj, "books": page_obj.object_list, "query": query, "category": category, "categories": categories})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    active_loans = BorrowRecord.objects.filter(book=book, status=BorrowRecord.Status.ISSUED).count()
    return render(request, "library/book_detail.html", {"book": book, "active_loans": active_loans})


def staff_required(view_func):
    return login_required(user_passes_test(lambda user: user.is_staff)(view_func))


@staff_required
def book_create(request):
    form = BookForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Book added successfully.")
        return redirect("book_list")
    return render(request, "library/book_form.html", {"form": form, "heading": "Add a book"})


@staff_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Book details updated.")
        return redirect("book_detail", pk=book.pk)
    return render(request, "library/book_form.html", {"form": form, "heading": "Edit book"})


@staff_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        if BorrowRecord.objects.filter(book=book, status=BorrowRecord.Status.ISSUED).exists():
            messages.error(request, "This book has active loans and cannot be deleted.")
        else:
            book.delete()
            messages.success(request, "Book deleted.")
        return redirect("book_list")
    return render(request, "library/book_confirm_delete.html", {"book": book})


@login_required
@transaction.atomic
def borrow_book(request, pk):
    if request.method != "POST":
        return redirect("book_detail", pk=pk)
    book = get_object_or_404(Book.objects.select_for_update(), pk=pk)
    already_borrowed = BorrowRecord.objects.filter(member=request.user, book=book, status=BorrowRecord.Status.ISSUED).exists()
    active_count = BorrowRecord.objects.filter(member=request.user, status=BorrowRecord.Status.ISSUED).count()
    if already_borrowed:
        messages.warning(request, "You already have an active loan for this book.")
    elif active_count >= 5 and not request.user.is_staff:
        messages.error(request, "Members can borrow up to five books at a time.")
    elif book.available_copies < 1:
        messages.error(request, "This book is currently unavailable.")
    else:
        BorrowRecord.objects.create(book=book, member=request.user, due_date=timezone.localdate() + timedelta(days=14))
        book.available_copies -= 1
        book.save(update_fields=["available_copies", "updated_at"])
        messages.success(request, "Book issued successfully. Please return it within 14 days.")
    return redirect("book_detail", pk=pk)


@login_required
def borrowing_list(request):
    if request.user.is_staff:
        records = BorrowRecord.objects.select_related("book", "member")
    else:
        records = BorrowRecord.objects.filter(member=request.user).select_related("book", "member")
    status = request.GET.get("status", "")
    if status in (BorrowRecord.Status.ISSUED, BorrowRecord.Status.RETURNED):
        records = records.filter(status=status)
    return render(request, "library/borrowing_list.html", {"records": records, "selected_status": status})


@login_required
@transaction.atomic
def return_book(request, pk):
    if request.method != "POST":
        return redirect("borrowing_list")

    record = get_object_or_404(
        BorrowRecord.objects.select_for_update().select_related("book"),
        pk=pk
    )

    if not request.user.is_staff and record.member.id != request.user.id:
        messages.error(request, "You are not allowed to return another member's book.")
        return redirect("borrowing_list")

    if record.status == BorrowRecord.Status.RETURNED:
        messages.info(request, "This book has already been returned.")
    else:
        record.status = BorrowRecord.Status.RETURNED
        record.returned_at = timezone.localdate()
        record.save(update_fields=["status", "returned_at"])

        book = record.book
        book.available_copies = min(
            book.total_copies,
            book.available_copies + 1
        )
        book.save(update_fields=["available_copies", "updated_at"])

        messages.success(request, "Book returned successfully.")

    return redirect("borrowing_list")
