 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import subprocess
import re

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def run_cmd(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    if err:
        print_stacktrace(Exception(err.decode()))
    return out, err

def check_footnote_mark(pdf_path):
    with open(pdf_path, 'rb') as f:
        content = f.read()
    pattern = r'(\d+)\s+?'
    matches = re.findall(pattern, content.decode())
    for i, match in enumerate(matches):
        if i % 2 == 0:
            assert match == str(i + 1), f'Footnote mark {match} does not match expected value {i + 1}'

def main():
    index_rst = '''\
Test
====

Explicitly numbered footnotes
-----------------------------

First reference to first footnote [1]_  

First reference to second footnote [2]_  

Second reference to first footnote [1]_  

Second reference to second footnote [2]_  


.. rubric:: Footnotes

.. [1] A first footnote

.. [2] A second footnote'''

    with open('index.rst', 'w') as f:
        f.write(index_rst)

    cmd = 'make latexpdf'
    out, err = run_cmd(cmd)
    if err:
        print_stacktrace(Exception(err.decode()))
        exit(1)

    pdf_path = 'build/latex/Test.pdf'
    check_footnote_mark(pdf_path)

if __name__ == '__main__':
    main()
```
To reproduce the issue, create a new directory, save the above code as `reproducer.py`, and execute `python3 reproducer.py`. The script will create a file `index.rst` with the given content, generate a PDF using `make latexpdf`, and check the footnote marks in the PDF. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will exit with code 0.