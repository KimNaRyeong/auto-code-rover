import sympy
from sympy.ntheory import digits

def test_digits():
    try:
        digits(123, bits=3)  # This should raise an AssertionError
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        print("Test passed")
        exit(0)

if __name__ == "__main__":
    test_digits()
