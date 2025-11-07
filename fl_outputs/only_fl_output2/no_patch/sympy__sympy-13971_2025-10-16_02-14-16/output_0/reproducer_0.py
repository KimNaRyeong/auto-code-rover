import sympy as sp

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

def check_seq_formula_display():
    k, m, n = sp.symbols('k m n', integer=True)
    seq = sp.SeqFormula(n**2, (n, 0, sp.oo))
    
    # Simulating the expected string representation
    # Note: This doesn't fully replicate Jupyter's rendering,
    # but it's aimed at detecting the described issue.
    seq_str = sp.sstr(seq)
    
    # Check if the sequence string representation contains incorrect escaping
    if "\\left\\" in seq_str or "\\right\\" in seq_str:
        raise AssertionError("Incorrect bracket escaping found in SeqFormula representation.")
    
    # The expected format does not contain backslash-escaped brackets
    expected_format = '[0, 1, 4, 9, ...]'
    assert expected_format in seq_str, "SeqFormula representation doesn't match the expected format."

try:
    check_seq_formula_display()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)  # Exits with non-zero to indicate failure/issue presence
else:
    print("No issue detected with SeqFormula representation.")
    exit(0)  # Exits with zero to indicate success/no issue detected
