```python
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

def test_nbconvert_latex_issue():
    import nbformat
    from nbconvert import PDFExporter
    from traitlets.config import Config

    # Create a notebook
    nb = nbformat.v4.new_notebook()
    nb.cells.append(nbformat.v4.new_code_cell("""
import sympy as sp
sp.init_printing()
1
    """))

    # Configure PDFExporter to not execute the cells
    c = Config()
    c.PDFExporter.execute = False

    # Export notebook to LaTeX, then PDF (simulation)
    pdf_exporter = PDFExporter(config=c)
    body, _ = pdf_exporter.from_notebook_node(nb)

    # Check for the incorrect LaTeX wrapping
    incorrect_wrapping = "$$\begin{equation*}"
    if incorrect_wrapping in body:
        raise AssertionError("Incorrect LaTeX wrapping detected."

    print("Issue not present. Test passed.")

if __name__ == "__main__":
    try:
        test_nbconvert_latex_issue()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    exit(0)
```

This script attempts to simulate the situation described in the issue. It creates a simple Jupyter Notebook in memory with code that would trigger the LaTeX formatting issue, uses `nbconvert` to export this notebook as a LaTeX document (which is a step towards creating a PDF), then checks if the incorrect LaTeX wrapping is present in the output LaTeX code.

**Note**: You need `nbconvert` and `nbformat` installed in your Python environment for this script to work. If you're working with Jupyter notebooks, you probably already have these. Otherwise, you can install them using pip (`pip install nbconvert nbformat`). Also, realize that converting notebooks to PDF would typically require a LaTeX distribution installed on your machine; however, this script stops at checking the generated LaTeX code for errors, not the final PDF compilation step, hence bypassing the need for a LaTeX installation for this specific test.