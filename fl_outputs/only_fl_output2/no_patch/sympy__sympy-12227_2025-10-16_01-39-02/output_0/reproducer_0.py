# reproducer.py
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', line_number, ": ", code_context, file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    from sympy import Float

    # Attempt to create a Float with binary precision instead of decimal
    try:
        binary_prec = 54
        val = 1.0
        f = Float(val, prec=binary_prec)

        # Here we check if the binary precision is correctly set
        # ideally, `f._prec` should equal `binary_prec` when fixed
        if f._prec != binary_prec:
            raise AssertionError(f"Expected binary precision to be {binary_prec}, got {f._prec} instead")
        else:
            print("Issue fixed, binary precision is correctly set.")

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # On exception, exit with a non-zero status code to indicate failure

if __name__ == "__main__":
    main()
    # If the issue is present, this line will not be reached, hence no need for sys.exit(0)
    # Since Python scripts exit with 0 by default if they run to completion without errors.
