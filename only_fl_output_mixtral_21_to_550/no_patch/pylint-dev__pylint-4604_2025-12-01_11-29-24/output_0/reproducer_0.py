import sys
import traceback
import pylint

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

pylintrc = """
[TYPECHECK]
ignore-comments=yes
"""

args = [
    "pylint",
    "--disable=all",
    "--enable=unused-import",
    "--load-plugins=pylint.extensions.typing",
    "--rcfile=<(echo '%s')" % pylintrc,
    "reproducer.py"
]

try:
    pylint.run_pylint(args)
except Exception as e:
    print_stacktrace(e)
    assert False, "pylint should not emit unused-import warning"
