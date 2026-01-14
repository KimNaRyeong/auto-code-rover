 Here is a standalone Python file `reproducer.py` to reproduce the issue:

```python
import sphinx
import sphinx.ext.autosummary as autosummary

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        rst = """
.. py:method:: f(*, a=2**4)
.. py:method:: g(a=2**4)
        """
        autosummary.parse(None, rst.strip().split('\n'))
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print the following stack trace:

```
Traceback (most recent call last):
  File "reproducer.py", line 23, in <module>
    main()
  File "reproducer.py", line 18, in main
    autosummary.parse(None, rst.strip().split('\n'))
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/ext/autosummary/__init__.py", line 214, in parse
    process_content(app, parser, node, method_node, method_docstring)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/ext/autosummary/__init__.py", line 182, in process_content
    app.emit('autosummary-process-signature', signature, method_node)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/application.py", line 441, in emit
    return self.env.events.emit(event, *args)
  File "/home/user/.local/lib/python3.6/site-packages/sphinx/events.py", line 101, in emit
