import os
from docutils import nodes
from docutils.parsers.rst import Directive, directives

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

def setup(app):
    app.add_directive('glossary', GlossaryDirective)

class GlossaryDirective(Directive):
    def run(self):
        glossary_node = nodes.definition()
        self.state.nested_parse(self.content, 0, glossary_node)
        return [glossary_node]

if __name__ == '__main__':
    try:
        with open('reproducer.rst', 'w') as f:
            f.write('''
.. glossary::
   :sorted:

   boson
      Particle with integer spin.

   *fermion*
      Particle with half-integer spin.

   tauon
   myon
   electron
      Examples for fermions.
''')
        os.system('xelatex -output-directory=_build reproducer.rst')
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    assert False, "Expected LaTeX output to not contain a newline"

