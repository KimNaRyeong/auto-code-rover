import sympy as sp

def mathematica_code(expr):
    return sp.latex(expr)

def main():
    x = sp.symbols('x')
    result = mathematica_code(sp.Max(x, 2))
    expected_result = 'Max[x,2]'
    if result != expected_result:
        raise AssertionError(f"Expected '{expected_result}' but got '{result}'")

if __name__ == "__main__":
    try:
        main()
        print("The issue is fixed.")
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
