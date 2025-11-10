Here is the `reproducer.py` file to reproduce the issue:
```
import json
from django.contrib import admin
from django.db import models

class MyModel(models.Model):
    my_field = models.JSONField()

admin.site.register(MyModel)

def test_unicode_chars_in_jsonfield():
    obj = MyModel(my_field='中国')
    serialized_data = json.dumps(obj.my_field)
    assert serialized_data == '"\u4e2d\u56fd"'  # expected ASCII encoding
    print("Issue is present: Unicode chars are not displayed properly in JSONField")

try:
    test_unicode_chars_in_jsonfield()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed: Unicode chars are displayed properly in JSONField")
exit(0)
```
This script defines a Django model with a `JSONField` and registers it with the admin site. It then creates an instance of the model with Chinese characters in the `JSONField`, serializes the data using `json.dumps`, and asserts that the resulting string is encoded in ASCII. If the assertion fails, the issue is present, and the script prints a stack trace of the error and exits with code 1. If the assertion passes, the script prints a success message and exits with code 0.

To run this script, save it to `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.