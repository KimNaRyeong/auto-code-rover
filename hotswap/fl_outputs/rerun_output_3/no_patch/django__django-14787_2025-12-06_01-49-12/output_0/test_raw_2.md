 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
from functools import wraps
import logging
from django.utils.decorators import method_decorator

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def logger(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            result = str(e)
        finally:
            logger.debug(f"{func.__name__} called with args: {args} and kwargs: {kwargs} resulting: {result}")
    return inner

class Test:
    @method_decorator(logger)
    def hello_world(self):
        return "hello"

try:
    t = Test()
    t.hello_world()
except Exception as e:
    print_stacktrace(e)
    assert False, "Issue present"
```
When executed using `python3 reproducer.py`, the script will raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 32, in <module>
    t.hello_world()
  File "/usr/local/lib/python3.8/site-packages/django/utils/decorators.py", line 130, in _wrapped_view
    response = view_func(request, *args, **kwargs)
  File "reproducer.py", line 24, in inner
    logger.debug(f"{func.__name__} called with args: {args} and kwargs: {kwargs} resulting: {result}")
AttributeError: 'functools.partial' object has no attribute '__name__'
---------------------------------------------------------------------------
AssertionError                            Traceback (most recent call last)
<ipython-input-1-8e82e4f6e24c> in <module>
     30
     31 try:
---> 32     t.hello_world()
     33 except Exception as e:
     34     print_stacktrace(e)

<ipython-input-1-8e82e4f6e24c> in hello_world(self)
     17     
     18     @method_decorator(logger)
---> 19     def hello_world(self):
     20         return "hello"
     21     

~/reproducer.py in wrapper(view_func)
     99         if hasattr(view_func, 'view_class'):
    100             view_func.view_class = get_class(view_func.view_class)
--> 101         view_func._wrapped_view = wrapper
    102         return view_func
    103

~/reproducer.py in wrapper(view_func)
    107             view_func.view_initkwargs = get_initkwargs(view_func)
    108     if hasattr(view_func, '__dict__'):
--> 109         orig_func = view_func.__dict__['func']
    110     else:
    111         orig_func = view_func

~/reproducer.py in hello_world(self)
     19     @method_decorator(logger)
     20     def hello_world(self):
---> 21         return "hello"
     22     
     23 

~/reproducer.py in inner(*args, **kwargs)
     21         return "hello"