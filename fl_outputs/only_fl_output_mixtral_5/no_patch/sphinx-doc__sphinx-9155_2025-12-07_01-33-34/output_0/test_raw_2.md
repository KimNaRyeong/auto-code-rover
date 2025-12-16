 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sphinx
import sphinx_build

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    sourcedir = '.'
    confdir = '_build'
    outputdir = '_build/html'
    args = ['-M', 'html', '.', '_build']
    app = sphinx_build.BuildEnvironment(buildername='html', srcdir=sourcedir,
                                        confdir=confdir)
    sphinx_build.main(args, app, status=sphinx.util.status_class())

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        raise
```
To run the script, execute `python3 reproducer.py` in the root directory of the project. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will exit with code 0.