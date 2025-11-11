import django
from django.db import models
from django.forms import ModelForm, ChoiceField
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

    class Author(models.Model):
        book = models.ForeignKey(Book, on_delete=models.CASCADE, limit_choices_to=models.Q(title='Test'))

    class MyForm(ModelForm):
        book = ChoiceField(queryset=Author.objects.all())

    form = MyForm()
    print(form.as_table())

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present")
        exit(0)
