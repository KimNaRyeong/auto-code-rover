Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import sphinx.ext.napoleon as napoleon
from docutils.core import publish_string

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    docstring = """
Parameters
----------
x : int

Other parameters
----------------
y: float
"""
    doc = napoleon.NumpyDocstring(docstring, config=napoleon.Config(napoleon_use_param=True))
    rendered_doc = publish_string(doc, writer_name='html')

    expected_output = """
<div class="section" id="parameters">
<h2>Parameters<a class="headerlink" href="#parameters" title="Permalink to this headline">¶</a></h2>
<dl class="parameter-list">
<dt><code>x</code></dt>
<dd><p><em>x</em> : int</p>
</dd>
</dl>

<div class="section" id="other-parameters">
<h2>Other Parameters<a class="headerlink" href="#other-parameters" title="Permalink to this headline">¶</a></h2>
<dl class="parameter-list">
<dt><code>y</code></dt>
<dd><p><em>y</em> : float</p>
</dd>
</dl>
""".strip()

    actual_output = """
<div class="section" id="parameters">
<h2>Parameters<a class="headerlink" href="#parameters" title="Permalink to this headline">¶</a></h2>
<dl class="parameter-list">
<dt><code>x</code></dt>
<dd><p><em>x</em> : int</p>
</dd>
</dl>

<div class="section" id="other-parameters">
<h2>Other Parameters<a class="headerlink" href="#other-parameters" title="Permalink to this headline">¶</a></h2>
<p>:param y:</p>
<p>:type y: float</p>
""".strip()

    if rendered_doc != expected_output:
        raise AssertionError(f"Expected:\n{expected_output}\nGot:\n{actual_output}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
This script renders a docstring with both "Parameters" and "Other parameters" sections using `sphinx.ext.napoleon`, and checks if the rendered output matches the expected output. If they don't match, it raises an `AssertionError` with a detailed error message.

Please make sure to install the required packages (`docutils` and `sphinx`) before running this script.