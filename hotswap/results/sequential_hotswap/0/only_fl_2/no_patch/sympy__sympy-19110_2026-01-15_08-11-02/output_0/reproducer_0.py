# reproducer.py
def main():
    try:
        from sympy import ZeroMatrix
        
        # Creating a ZeroMatrix instance
        Z = ZeroMatrix(2, 3)
        
        # Evaluating the truthiness of the ZeroMatrix instance
        result = bool(Z)
        
        # The issue is that ZeroMatrix should not be falsy.
        # Thus, if `bool(Z)` is False, it contradicts the expectation.
        assert result, "ZeroMatrix instance should not evaluate to False."
    
    except AssertionError as e:
        print_stacktrace(e)
        raise  # Re-raise the AssertionError to signal the failure externally
    
    # If the script reaches this point without exceptions, the issue is fixed.
    print("The issue is fixed.")

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', line_number, file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
