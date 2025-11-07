def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    from sympy.physics.units import Quantity, voltage, current, ohm, convert_to

    vs = Quantity('vs')
    vs.set_dimension(voltage)
    vs_i = Quantity('vs_i')
    vs_i.set_dimension(current)

    try:
        result = convert_to(vs / vs_i, ohm)
        # Check if the scale_factor calculation issue exists by explicitly comparing against the erroneous result:
        assert str(result) != 'ohm/1000', "Incorrectly received 'ohm/1000'; Expected 'ohm'"
    except AssertionError as e:
        print_stacktrace(e)
        raise e  # Reraise the exception to indicate failure explicitly

if __name__ == "__main__":
    try:
        main()
        print("Issue resolved or not present. Exiting with code 0.")
    except Exception as e:
        exit(1)  # Exit with non-zero code to indicate failure/issue presence
