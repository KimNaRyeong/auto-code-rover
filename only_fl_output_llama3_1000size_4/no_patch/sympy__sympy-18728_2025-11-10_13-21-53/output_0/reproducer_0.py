import sympy as sp
from sympy import symbols, zoo

def main():
    a, b = symbols('a b', positive=True)
    assert not (a**b).is_zero, "Expected Pow.is_zero to return False"
    print_stacktrace(AssertionError)

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
