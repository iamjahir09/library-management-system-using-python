from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].strip().lower()
        user.first_name = self.cleaned_data["first_name"].strip()
        user.last_name = self.cleaned_data["last_name"].strip()
        if commit:
            user.save()
        return user

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "isbn", "category", "description", "publisher", "publication_year", "total_copies", "available_copies", "cover_url"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "publication_year": forms.NumberInput(attrs={"min": 1, "max": 2100}),
            "total_copies": forms.NumberInput(attrs={"min": 1}),
            "available_copies": forms.NumberInput(attrs={"min": 0}),
        }

    def clean(self):
        cleaned = super().clean()
        total = cleaned.get("total_copies")
        available = cleaned.get("available_copies")
        if total is not None and available is not None and available > total:
            self.add_error("available_copies", "Available copies cannot exceed total copies.")
        return cleaned
