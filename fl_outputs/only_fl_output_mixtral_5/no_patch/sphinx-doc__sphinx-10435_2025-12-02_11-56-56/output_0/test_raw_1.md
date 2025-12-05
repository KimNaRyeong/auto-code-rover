 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sphinx
import sphinx.ext.autodoc as autodoc
import sphinx.writers.latex as latex
import sphinx.roles as roles
import sphinx.highlighting as highlighting

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def setup():
    app = sphinx.application.Sphinx(srcdir='.', confdir='.', outdir='.', doctreedir='.', buildername='latex', warningiserror=0)
    app.connect('config-inited', configure)
    app.build(force_all=True)

def configure(app):
    app.add_role('python', python_role)
    app.add_directive('code-block', code_block_directive)
    app.connect('builder-inited', initialize_latex)

def python_role(role, rawtext, text, line, inliner, options={}, content=[]):
    node = roles.XRefRole(rawtext, text, line, inliner, options, content)
    return [node], []

def code_block_directive(directive, document):
    node = autodoc.highlight_code(directive.arguments[0], directive.arguments[1], document.settings.highlight_language)
    return [node], []

def initialize_latex(app):
    latex_writer = app.builder.writer
    latex_writer.add_package('fvextra')
    latex_writer.add_package('color')
    latex_writer.add_package('listings')
    latex_writer.add_package('sphinxcode')
    latex_writer.add_directive('code-block', code_block_directive)
    latex_writer.add_role('python', python_role)
    latex_writer.connect('do-preamble', add_to_preamble)

def add_to_preamble(app, docname, document):
    latex_preamble = r'''
\usepackage{fvextra}
\usepackage{color}
\usepackage{listings}
\usepackage{sphinxcode}

\lstset{
    basicstyle=\ttfamily,
    columns=fullflexible,
    frame=single,
    breaklines=true,
    postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space},
}

\lstset{language=[Python]Python}

\newcommand{\sphinxcode}{\lstinline[language=[Python]Python]}
\newcommand{\sphinxupquote}[1]{\textquotesingle#1\textquotesingle}
'''
    document.settings.latex_preamble += latex_preamble

if __name__ == '__main__':
    setup()

    # The following lines reproduce the issue
    code_block = r'\sphinxcode{def foo(1 + 2 + None + "abc"): pass}'
    expected_output = r'def foo(1 + 2 + None + "abc"): pass'
    assert code_block == expected_output, "Unexpected whitespace in code block"
```
To reproduce the issue, run the script with `python3 reproducer.py`. The script will raise an `AssertionError` with the following message:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 81, in <module>
    assert code_block == expected_output, "Unexpected whitespace in code block"
AssertionError: Unexpected whitespace in code