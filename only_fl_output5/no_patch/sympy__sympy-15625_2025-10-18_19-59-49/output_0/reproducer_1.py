import subprocess
import sys
import tempfile
import os

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

def simulate_latex_error():
    latex_content = r'''
    \documentclass{article}
    \usepackage{amsmath}
    \begin{document}
    $$\begin{equation*}1\end{equation*}$$
    \end{document}
    '''

    with tempfile.TemporaryDirectory() as tmpdir:
        tex_file_path = os.path.join(tmpdir, "test.tex")
        with open(tex_file_path, "w") as tex_file:
            tex_file.write(latex_content)
        
        # Attempt to compile the LaTeX file to PDF
        process = subprocess.run(["pdflatex", "-halt-on-error", tex_file_path],
                                 cwd=tmpdir,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 text=True)
        
        # Check for specific LaTeX error signature in the output
        if "Bad math environment delimiter" in process.stdout:
            raise AssertionError("Detected LaTeX error 'Bad math environment delimiter'")

def main():
    try:
        simulate_latex_error()
        print("No issue detected.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
