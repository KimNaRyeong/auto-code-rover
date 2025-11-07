from sympy import exp, I, pi, simplify, expand_complex
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
    try:
        # Testing exp to simplify based on its periodicity
        # for purely imaginary arguments
        result1 = exp(9*I*pi/4)
        simplified_result1 = simplify(result1)
        
        # The issue is that exp doesn't automatically use its periodicity to reduce its argument
        # So, if the issue exists, the simplified result would not be equal to the expected simplified form
        # And if the issue is fixed, the simplified result should be equal to the expected simplified form
        assert simplified_result1 == exp(I*pi/4), "exp doesn't simplify based on its periodicity"

        # Additional check with subtraction
        a = exp(9*I*pi/4) - exp(I*pi/4)
        simplified_a = simplify(a)
        expanded_complex_a = expand_complex(a)

        # Assert checks to catch the issue where `simplify` and `expand_complex` might not behave as expected
        assert expanded_complex_a == 0, "`expand_complex` does not simplify to 0"

        print("All checks passed successfully. The issue seems to be fixed.")

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with non-zero code to indicate an issue

if __name__ == "__main__":
    main()
    sys.exit(0)  # Exit successfully as the issue is fixed or not detected
