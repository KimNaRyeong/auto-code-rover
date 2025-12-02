 Here is a standalone Python script `reproducer.py` that demonstrates the issue:
```python
import sphinx_rtd_theme

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
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
    html_theme_options = {
        'collapse_navigation': False,
        'sticky_navigation': True,
        'navigation_depth': 4,
        'includehidden': True,
        'relbarbg': 'white',
        'display_version': True,
    }
    html_static_path = ['_static']

    html_context = {
        'css_files': [
            '_static/theme_overrides.css',
        ],
    }

    try:
        import docutils.nodes
        import sphinx.application
        import sphinx.writers.html

        class MyHTMLTranslator(sphinx.writers.html.HTMLTranslator):
            def visit_kbd(self, node):
                if len(node) > 0:
                    self.body.append('<kbd class="kbd compound docutils literal notranslate">')
                else:
                    self.body.append('<kbd class="kbd docutils literal notranslate">')

            def depart_kbd(self, node):
                self.body.append('</kbd>')

        app = sphinx.application.Sphinx(
            srcdir='.',
            confdir='.',
            outdir='.',
            doctreedir='.',
            buildername='html',
            warningiserror=0,
            confoverrides={
                'html_theme': 'sphinx_rtd_theme',
                'html_theme_path': html_theme_path,
                'html_theme_options': html_theme_options,
                'html_static_path': html_static_path,
                'html_context': html_context,
            },
        )

        app.setup_extension('sphinx.ext.doctest')
        app.setup_extension('sphinx.ext.autodoc')
        app.setup_extension('sphinx.ext.intersphinx')
        app.setup_extension('sphinx.ext.viewcode')
        app.setup_extension('sphinx.ext.githubpages')

        env = app.env
        app.build(force_all=True, nonet=True)

        with open('_build/html/index.html', 'r') as f:
            content = f.read()

        expected = '''\
<!DOCTYPE html>
<html class="no-js" lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Test Documentation</title>
<link rel="stylesheet" href="_static/theme_overrides.css" type="text/css" />
<link rel="stylesheet" href="_static/sphinx_rtd_theme.css" type="text/css" />
<link rel="stylesheet" href="_static/pygments.css" type="text/css" />
<script id="documentation_options" data-url_root="./" src="_static/documentation_options.js"></script>
<script src="_static/jquery.js"></script>
<script src="_static/underscore.js"></script>
<script src="_static/doctools.js"></script>
<script src="_static/