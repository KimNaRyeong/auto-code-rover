Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.db import models

def main():
    try:
        class MyModel(models.Model):
            pub_date = models.DateTimeField("date published")

        admin.site.register(MyModel)

        my_model = MyModel()
        my_model.pub_date = '2022-01-01'
        my_model.save()

        my_model.pub_date = '2022-02-01'
        my_model.save()

        history = my_model.history
        if not all([msg.startswith('Changed date published.') for msg in history]):
            raise AssertionError("Expected verbose name in model history")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script creates a simple Django app, defines a model with a datetime field, and then saves two versions of the model. It checks if the history messages contain the verbose name "date published" instead of just "pub_date". If not, it raises an `AssertionError` and prints the stack trace using the provided function.