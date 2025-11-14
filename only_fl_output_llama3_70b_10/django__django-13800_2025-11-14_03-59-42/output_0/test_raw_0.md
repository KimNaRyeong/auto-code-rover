Here is a standalone Python script `reproducer.py` to reproduce the issue:
```
import os
from django.contrib.messages import get_messages
from django.http.response import HttpResponse

def reproducer():
    response = HttpResponse()
    messages_storage = get_messages(response)
    messages_storage.add_message(50, "123\"NOTRECEIVED\"")

    cookie_value = response.cookies['messages'].value
    assert '\\' not in cookie_value, f"RFC 6265 non-compliant cookie value: {cookie_value}"

try:
    reproducer()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script uses the `django.contrib.messages` module to add a message with a value that contains an escaped double quote (`\"`). It then checks if the resulting cookie value contains the escape character (`\\`) which is not compliant with RFC 6265. If it does, it raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of the error.

You can run this script by executing `python3 reproducer.py` in the root directory of your Django project.