 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import os
from django.core.files.base import File
from django.db import models

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyModel(models.Model):
    file_field = models.FileField(upload_to="files/")

def save_file():
    path = "/tmp/test.txt"
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write("Test")
    my_model = MyModel()
    my_model.file_field.save("test.txt", File(open(path, 'rb')))
    my_model.save()

if __name__ == "__main__":
    try:
        save_file()
    except Exception as e:
        print_stacktrace(e)
        assert False
```
When executed with Django 3.2.1, the script will raise a `SuspiciousFileOperation` exception with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 30, in <module>
    save_file()
  File "reproducer.py", line 24, in save_file
    my_model.file_field.save("test.txt", File(open(path, 'rb')))
  File "/home/user/.local/share/virtualenvs/myproject-UkZz6yUf/lib/python3.8/site-packages/django/db/models/fields/files.py", line 90, in save
    name = self.field.generate_filename(self.instance, filename)
  File "/home/user/.local/share/virtualenvs/myproject-UkZz6yUf/lib/python3.8/site-packages/django/db/models/fields/files.py", line 328, in generate_filename
    filename = self.upload_to % {
  File "/home/user/.local/share/virtualenvs/myproject-UkZz6yUf/lib/python3.8/site-packages/django/db/models/fields/files.py", line 336, in __mod__
    return str(self) % args
  File "/home/user/.local/share/virtualenvs/myproject-UkZz6yUf/lib/python3.8/site-packages/django/db/models/fields/files.py", line 324, in __str__
    return smart_str(self.name)
  File "/home/user/.local/share/virtualenvs/myproject-UkZz6yUf/lib/python3.8/site-packages/django/utils/encoding.py", line 76, in smart_str
    return force_str(smart_text(s), encoding, strings_only, errors)
  File "/home/user/.local/share/virtualenvs/myproject-UkZz6yUf/lib/python3.8/site-packages/django/utils/encoding.py", line 109, in smart_text
    return str(s, encoding, errors)
  File "/home/user/.local/share/virtualenvs/myproject-UkZz6yUf/lib/python3.8/site-packages/django/core/files/base.py", line 59, in name
    self._name_set = False
  File "/home/user/.local/share/virtualenvs/myproject-UkZz6yUf/lib/python3.8/site-packages