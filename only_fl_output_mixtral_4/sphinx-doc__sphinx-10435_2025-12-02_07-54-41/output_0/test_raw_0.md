 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sphinx
import sphinx.ext.autodoc as autodoc
import sphinx.ext.napoleon as napoleon
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
    # Initialize Sphinx
    app = sphinx.application.Sphinx(srcdir='.', confdir='.',
                                     outdir='build/latex', doctreedir='build/doctree',
                                     buildername='latex', warningiserror=True)

    # Add necessary extensions
    app.add_extension('sphinx.ext.autodoc')
    app.add_extension('sphinx.ext.napoleon')

    # Initialize roles and highlighting
    roles.setup_roles(app)
    highlighting.init_highlighting(app)

    # Modify the LaTeX writer to add a space at the start and end of inline code
    app.add_config_value('highlight_language', 'python3', False)
    app.add_config_value('pygments_style', 'sphinx', False)
    app.add_config_value('latex_elements', {}, False)
    app.add_config_value('latex_additional_files', [], False)
    app.add_config_value('latex_engine', 'pdflatex', False)
    app.add_config_value('latex_engine_args', [], False)
    app.add_config_value('latex_preamble', '', False)
    app.add_config_value('latex_appendices', '', False)
    app.add_config_value('latex_domain_indices', True, False)
    app.add_config_value('latex_use_parts', False, False)
    app.add_config_value('latex_use_modindex', True, False)
    app.add_config_value('latex_show_pagerefs', True, False)
    app.add_config_value('latex_show_urls', 'inline', False)
    app.add_config_value('latex_bibtex_style', 'plain', False)
    app.add_config_value('latex_bibtex_bibfile', '', False)
    app.add_config_value('latex_elements_required', [], False)
    app.add_config_value('latex_elements_optional', [], False)
    app.add_config_value('latex_docclass', 'article', False)
    app.add_config_value('latex_logo', '', False)
    appx = latex.LaTeXWriter.setup(app)
    appx.add_package('color')
    appx.add_package('fancyvrb')
    appx.add_package('longtable')
    appx.add_package('hyperref')
    appx.add_package('ulem')
    appx.add_package('amsmath')
    appx.add_package('amssymb')
    appx.add_package('amsthm')
    appx.add_package('graphicx')
    appx.add_package('grffile')
    appx.add_package('verbatim')
    appx.add_package('float')
    appx.add_package('wrapfig')
    appx.add_package('soul')
    appx.