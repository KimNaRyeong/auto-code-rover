 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import sys
import traceback
from django.core.management import execute_from_command_line
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from my_first_app.models import City 