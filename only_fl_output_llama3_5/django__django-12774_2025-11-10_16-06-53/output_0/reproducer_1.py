import os
from django.db import models

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
    try:
        class Article(models.Model):
            slug = models.CharField(max_length=255)

            class Meta:
                constraints = [
                    models.UniqueConstraint(fields=["slug"], name="%(app_label)s_%(class)s_slug_unq")
                ]

        Article.objects.in_bulk(field_name="slug")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

if __name__ == "__main__":
    main()
