from django.db import models
from django.contrib import admin
from django.urls import path
from django.test.utils import setup_test_environment

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
        from models import Post, User
        admin.site.register(Post, PostAdmin)
        post = Post(title="Test", authors=[User(email="test@example.com")])
        post.save()
        post.delete()
    except Exception as e:
        print_stacktrace(e)
        assert False, "Error occurred"

if __name__ == "__main__":
    main()
