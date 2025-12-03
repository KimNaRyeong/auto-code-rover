 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Client(models.Model):
    name = models.CharField(_('name'), max_length=256)
    name2 = models.CharField(_('unofficial or obsolete name'), max_length=25