Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import os
import sys
from sphinx.builders.gettext import GettextBuilder
from sphinx.util import logging
import subprocess
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    try:
        os.chdir('/path/to/blender_docs')
        make_clean_make_gettext = subprocess.run(['make', 'clean; make gettext'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if make_clean_make_gettext.returncode != 0:
            print_stacktrace(subprocess.CalledProcessError(make_clean_make_gettext.returncode, 'make clean; make gettext'))
            sys.exit(1)

        with open('build/gettext/blender_manual.pot', 'r') as pot_file:
            pot_content = pot_file.read()

        if "Type" in pot_content and len(pot_content.split("#: ../../manual/modeling/hair.rst:0")) > 2:
            raise AssertionError("Issue present")

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script will change into the directory `/path/to/blender_docs`, run `make clean; make gettext` and then read the contents of the generated `.pot` file. If the issue is present (i.e., there are duplicate locations), it will raise an `AssertionError`.