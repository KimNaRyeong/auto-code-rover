import django
from django.db import models
from django.forms.models import ModelForm
from django.core.exceptions import AssertionError

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    django.setup()
    
    class Book(models.Model):
        title = models.CharField(max_length=200)
        author = models.ForeignKey('Author', on_delete=models.CASCADE, limit_choices_to=models.Q(title='Test'))

    class Author(models.Model):
        name = models.CharField(max_length=100)

    class BookForm(ModelForm):
        class Meta:
            model = Book
            fields = ['title', 'author']

    book_form = BookForm()
    
    try:
        print(book_form.as_table())
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)

if __name__ == "__main__":
    main()
