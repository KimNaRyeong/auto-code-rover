 Here is a standalone Python script that reproduces the issue:
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
    srcdir = '.'
    builddir = '_build'
    try:
        sphinx_build.build_main([srcdir, builddir, 'html', '-b', 'html', '-d', 'build/doctrees'])
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
