Here is the reproducer script:

```python
import django
from django.template import Template, Context
from django.conf import settings
from django.core.management import execute_from_command_line
from django.test.utils import setup_test_environment
from django.test.client import RequestFactory
from django.template.defaultfilters import random as _random

def main():
    try:
        # Set up the Django environment
        setup_test_environment()
        execute_from_command_line(['manage.py', 'shell'])
        
        # Create a request and context
        rf = RequestFactory()
        request = rf.get('/')
        context = Context({'list_var': []})
        
        # Render the template with the random filter
        template = Template('{{ list_var|random }}')
        result = template.render(context)
        
        # Check if the issue is present
        assert not result, "Expected an empty response"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script sets up the Django environment, creates a request and context with an empty list, renders a template with the random filter, and checks if the response is not empty. If the issue is present, it prints the stack trace and exits with code 1.