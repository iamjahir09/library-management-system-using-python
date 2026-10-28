
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("books/", views.book_list, name="book_list"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("books/add/", views.book_create, name="book_create"),  # type: ignore[arg-type]
    path("books/<int:pk>/edit/", views.book_update, name="book_update"),  # type: ignore[arg-type]
    path("books/<int:pk>/delete/", views.book_delete, name="book_delete"), # type: ignore[arg-type]

    path("books/<int:pk>/borrow/", views.borrow_book, name="borrow_book"),

    path("borrowings/", views.borrowing_list, name="borrowing_list"),
    path("borrowings/<int:pk>/return/", views.return_book, name="return_book"),
]
