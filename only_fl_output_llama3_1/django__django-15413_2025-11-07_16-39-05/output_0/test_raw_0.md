Here is the reproducer script:

```python
import os
import sys
from django.core.handlers.base import BaseHandler
from django.utils.log import logger
from django.conf import settings

def main():
    # Set up Django environment
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    from django.conf import settings
    settings.configure()

    # Create a test request and response
    from django.http import HttpResponse
    from django.test.client import RequestFactory
    factory = RequestFactory()
    request = factory.get('/')
    response = HttpResponse('Test')

    # Adapt the middleware
    BaseHandler().adapt_method_mode(True, lambda: None)

    # Check if the log message is present
    with self.assertLogs('django.request', 'DEBUG') as cm:
        pass

    if not any(record.getMessage() == "Synchronous middleware ... adapted." for record in cm.records):
        print_stacktrace(AssertionError("Expected log message not found"))
        sys.exit(1)
    else:
        print("Issue reproduced")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

This script sets up a Django environment, creates a test request and response, adapts the middleware using `BaseHandler().adapt_method_mode()`, checks if the log message is present, and prints a stack trace if the issue is not reproduced.