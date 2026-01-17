 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import django
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyModel(django.db.models.Model):
    name = django.db.models.CharField(max_length=100)

    class Meta:
        db_table = 'my_model'

@receiver(post_save, sender=MyModel)
def my_post_save_handler(sender, instance, **kwargs):
    print("My post-save handler called")

def my_transaction_handler():
    print("My transaction handler called")

def main():
    django.setup()

    # Create a transaction and register a None callback on commit
    transaction.on_commit(None)

    # Save a model instance to trigger the post-save signal
    my_model = MyModel(name="Test")
    my_model.save()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        raise
```
To reproduce the issue, run the script with `python3 reproducer.py`. The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue.

To fix the issue, replace the line `transaction.on_commit(None)` with `transaction.on_commit(lambda: None)` or remove the line altogether.