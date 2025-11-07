import sympy
from sympy.ntheory import digits

def test_digits():
    result = digits(123, bits=5)  # This should raise an AssertionError if the issue is present
    print_stacktrace(AssertionError("Issue not reproduced"))

try:
    test_digits()
except Exception as e:
    print_stacktrace(e)
    exit(1)
