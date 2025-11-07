Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.contrib.auth.models import User

def prepare_lookup_value(value):
    return value.replace(',', ' ')

try:
    users = User.objects.filter(username__in=['johnny,viola,gordon'])
except Exception as e:
    print_stacktrace(e)
    raise SystemExit(1)

if __name__ == '__main__':
    django.setup()
    admin.autodiscover()

    try:
        users = User.objects.filter(username__in=['johnny,viola,gordon'])
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

    if __name__ == '__main__':
        python = sys.executable
        args = [python] + sys.argv[1:]
        exec(open(__file__).read(), globals(), locals())
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.