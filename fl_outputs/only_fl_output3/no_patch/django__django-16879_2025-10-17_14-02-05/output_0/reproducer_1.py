import os
import sys
import django
from django.conf import settings
from django.db import models, connections, DEFAULT_DB_ALIAS
from django.core.management import call_command
from django.db.models import Subquery, OuterRef, F, Sum, Case, When, FloatField, Count
from django.db.models.functions import Round

# Minimal Django configuration
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=('__main__',),
    USE_TZ=True,
    TIME_ZONE='UTC',
)

django.setup()


class User(models.Model):
    name = models.CharField(max_length=255)


class OtherModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.IntegerField()


class Book(models.Model):
    authors = models.ManyToManyField(User, related_name="books")
    name = models.CharField(max_length=255)


class Author(User):
    pass


def create_tables():
    with connections[DEFAULT_DB_ALIAS].schema_editor() as schema_editor:
        schema_editor.create_model(User)
        schema_editor.create_model(OtherModel)
        schema_editor.create_model(Book)
        schema_editor.create_model(Author)
        call_command('migrate', run_syncdb=True)


def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else 'Unknown'
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f'    {line_number}: {code_context}', file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def test_referenced_group_by_aggregation_over_annotation():
    # Assume the tables have been created; populate them with test data
    user1 = User.objects.create(name="User 1")
    OtherModel.objects.create(user=user1, total=5)
    author1 = Author.objects.create(name="Author 1")
    book1 = Book.objects.create(name="aBook")
    book1.authors.add(author1)
    book2 = Book.objects.create(name="anotherBook")
    book2.authors.add(author1)

    try:
        total_books_qs = (
            Book.objects.filter(authors__pk=OuterRef("pk")).annotate(
                total=Count("pk")).values("total")
        )
        annotated_authors = Author.objects.annotate(
            total_books=Subquery(total_books_qs.annotate(total_books=F("total")).values("total_books")),
            total_books_a=Subquery(total_books_qs.filter(name__istartswith="a").annotate(
                total_books_a=F("total")).values("total_books_a")),
        ).aggregate(
            sum_total_books=Sum("total_books"),
            sum_total_books_a=Sum("total_books_a"),
            a_over_total_rate=Case(
                When(
                    sum_total_books=0,
                    then=0,
                ),
                default=Round((Sum("total_books_a") / Sum("total_books")) * 100, 2),
                output_field=FloatField(),
            ),
        )
        assert annotated_authors["sum_total_books"] > 0, "Aggregation failed to sum total books"
        assert annotated_authors["a_over_total_rate"] >= 0, "Conversion rate calculation failed"

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Test failed due to an unexpected error.")


if __name__ == '__main__':
    create_tables()
    try:
        test_referenced_group_by_aggregation_over_annotation()
        print("Test completed successfully.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
