 Here is a standalone Python script `reproducer.py` that uses the provided LaTeX code and demonstrates the issue with the terms not being separated by a newline in the xelatex output:

```python
import subprocess
import re

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# LaTeX code for the listing
latex_code = r"""
\documentclass{article}
\usepackage{duckuments} % for filler text

\begin{document}

\section{Listing}

\begin{description}
\item[{\sffamily\nolinkurl{{file}.cc}}] \blindtext
\item[{\sffamily\nolinkurl{{file}.cp}}] \blindtext
\item[{\sffamily\nolinkurl{{file}.cxx}}] \blindtext
\item[{\sffamily\nolinkurl{{file}.cpp}}] \blindtext
\item[{\sffamily\nolinkurl{{file}.CPP}}] \blindtext
\item[{\sffamily\nolinkurl{{file}.c++}}] \blindtext
\item[{\sffamily\nolinkurl{{file}.C}}] \blindtext
\item[{\sffamily\nolinkurl{{file}.mm}}] \blindtext
\item[{\sffamily\nolinkurl{{file}.M}}] \blindtext
\item[{\sffamily\nolinkurl{{file}.mii}}] \blindtext
\item[{\sffamily\nolinkurl{{file}.hh}}] \blindtext
\item[{\sffamily\nolinkurl{{file}.H}}] \blindtext
\item[{\sffamily\nolinkurl{{file}.hp}}] \blindtext
\item[{\sffamily\nolinkurl{{file}.hxx}}] \blindtext
\item[{\sffamily\nolinkurl{{file}.hpp}}] \blindtext
\item[{\sffamily\nolinkurl{{file}.HPP}}] \blindtext
\item[{\sffamily\nolinkurl{{file}.h++}}] \blindtext
\item[{\sffamily\nolinkurl{{file}.tcc}}] \blindtext
\end{description}

\end{document}
"""

# Write the LaTeX code to a file
with open("reproduction.tex", "w") as f:
    f.write(latex_code)

# Compile the LaTeX code
subprocess.run(["xelatex", "reproduction.tex"])
