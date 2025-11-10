import sympy
from sympy import symbols

def main():
    a = symbols('a', real=True)
    t = symbols('t', real=True, negative=False)

    bug = a * (-t + (-t + 1) * (2 * t - 1)) / (2 * t - 1)

    try:
        print(bug.subs(a, 1).apart(t))
    except AssertionError as e:
        print_stacktrace(e)
        raise

    if bug.apart(t) != '-a*t':
        print_stacktrace(AssertionError("Wrong result with apart"))
        raise

if __name__ == "__main__":
    sympy.__version__ = '1.0'
    main()
