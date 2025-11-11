Here is the reproducer script:

```python
import django
from django.db.models.signals import post_save
from django.db import transaction

def my_signal_receiver(sender, instance, **kwargs):
    try:
        transaction.on_commit(None)  # This line should raise an error
    except Exception as e:
        print_stacktrace(e)
        assert False, "Error expected"

django.setup()
post_save.connect(my_signal_receiver)

try:
    post_save.send(None)
except AssertionError:
    exit(0)
```

To run the script, execute `python3 reproducer.py` in your terminal. The script will raise an `AssertionError` when the issue is present and print a stack trace of the error.