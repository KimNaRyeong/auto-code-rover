import sympy as sp

def main():
    x = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    result = sp.exp(x)
    simplified_result = sp.simplify(result)

    if not isinstance(simplified_result, sp.Matrix):
        raise AssertionError("Simplification failed to recognize sin expressed as exponentials")

    print_stacktrace(AssertionError())

if __name__ == "__main__":
    main()
