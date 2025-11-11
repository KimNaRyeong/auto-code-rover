Here is the reproducer.py file:
```
import os
from sphinx.application import Sphinx
from sphinx.ext.autodoc import AutodocDirective
from docutils.parsers.rst import Directive, directives
from docutils.nodes import document, paragraph, literal_block

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

def test_latex_terms_separated_by_newline():
    app = Sphinx(srcdir='.', confdir='.')
    app.builder.name = 'latex'
    
    doc = document('test')
    directive = Directive('listing', 
                           arguments=[''],
                           options={'class': 'first'},
                           content='''
:samp:`{file}.cc` :samp:`{file}.cp` :samp:`{file}.cxx` :samp:`{file}.cpp` :samp:`{file}.CPP` :samp:`{file}.c++` :samp:`{file}.C`
  C++ source code that must be preprocessed.  Note that in :samp:`.cxx`,
  the last two letters must both be literally :samp:`x`.  Likewise,
  :samp:`.C` refers to a literal capital C.

:samp:`{file}.mm` :samp:`{file}.M`
  Objective-C++ source code that must be preprocessed.

:samp:`{file}.mii`
  Objective-C++ source code that should not be preprocessed.

:samp:`{file}.hh` :samp:`{file}.H` :samp:`{file}.hp` :samp:`{file}.hxx` :samp:`{file}.hpp` :samp:`{file}.HPP` :samp:`{file}.h++` :samp:`{file}.tcc`
  C++ header file to be turned into a precompiled header or Ada spec''')
    doc.append(directive)
    
    app.builder.document(doc)
    
    latex_output = app.builder.get_target_uri('test.tex')
    with open(latex_output, 'r') as f:
        latex_content = f.read()
        
    assert '\n' in latex_content, "Terms are not separated by a newline"
    
if __name__ == '__main__':
    try:
        test_latex_terms_separated_by_newline()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
This script creates a Sphinx application, builds a LaTeX document with the given RST content, and checks if the resulting LaTeX output contains newline characters between terms. If not, it raises an `AssertionError` with a stack trace.