from sympy import *
import sys

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

def main():
    init_printing()
    x = symbols('x')
    A = Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    B = exp(A)
    C = simplify(B)
    D = C.applyfunc(lambda f: trigsimp(f))
    E = D.applyfunc(lambda f: sqrtdenest(f))
    F = E.applyfunc(lambda f: trigsimp(f))
    G = F.applyfunc(lambda f: simplify(f))
    h = G[0, 1]
    i = h.subs(x, 1)
    assert i == sin(1), "AssertionError: Simplification fails to recognize sin expressed as exponentials"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
