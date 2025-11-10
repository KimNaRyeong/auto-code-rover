Here is the reproducer script:

```python
import django
from django.core import serializers
from django.db import IntegrityError
from test.models import TestTag, Test, TestTagMaster

def main():
    try:
        tag_master = TestTagMaster.objects.create(name="master")
        tag = TestTag.objects.create(name="tag", master=tag_master)
        test = Test.objects.create(name="test")
        test.tags.add(tag)
        test.save()
        serialized_data = serializers.serialize("json", [test])
        print(serialized_data)
    except IntegrityError as e:
        print_stacktrace(e)
        raise AssertionError("Serialization of m2m relation fails with custom manager using select_related")

if __name__ == "__main__":
    django.setup()
    main()
```

This script sets up the models, creates a `Test` object with related `TestTag`, and then tries to serialize it. If an `IntegrityError` is raised (which should be the case due to the custom manager), it prints the stack trace and raises an `AssertionError`.