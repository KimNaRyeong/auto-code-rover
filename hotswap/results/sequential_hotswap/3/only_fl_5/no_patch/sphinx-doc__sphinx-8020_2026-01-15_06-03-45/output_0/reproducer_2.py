import subprocess
import os
import sys
import tempfile

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def create_sphinx_project(directory):
    conf_py = os.path.join(directory, "source", "conf.py")
    os.makedirs(os.path.dirname(conf_py))
    with open(conf_py, "w") as f:
        f.write("""
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinx_qt_documentation',
    'sphinxcontrib_trio'
]
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
""")

    index_rst = os.path.join(directory, "source", "index.rst")
    with open(index_rst, "w") as f:
        f.write("""
.. automodule:: reproducer
   :members:
   :undoc-members:
   :show-inheritance:
""")

    module_py = os.path.join(directory, "reproducer.py")
    with open(module_py, "w") as f:
        f.write("""
import typing
from typing import Callable, Awaitable

def decorator(func):
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapped

@decorator
def host(func: Callable[..., Awaitable[None]], timeout: float = 3, *args, **kwargs):
    pass
""")

def run_sphinx_build(directory):
    subprocess.run(["sphinx-build", "-b", "html", os.path.join(directory, "source"), os.path.join(directory, "build")], check=True, capture_output=True)

def check_for_warning():
    with tempfile.TemporaryDirectory() as tmpdir:
        create_sphinx_project(tmpdir)
        try:
            run_sphinx_build(tmpdir)
        except subprocess.CalledProcessError as err:
            output = err.stderr.decode()
            if "WARNING: py:class reference target not found: Callable[[...], Awaitable[None]]" in output:
                print("Issue detected with Sphinx build.")
                print_stacktrace(Exception("Sphinx build emitted the known warning."))
                return
            else:
                print(output)
                raise AssertionError("Sphinx build failed, but not with the expected warning.")

        print("No issue detected, Sphinx build succeeded without the warning.")
        sys.exit(0)

try:
    check_for_warning()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
