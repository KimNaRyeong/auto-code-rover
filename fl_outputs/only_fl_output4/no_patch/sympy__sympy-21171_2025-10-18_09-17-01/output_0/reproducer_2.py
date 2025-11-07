# reproducer.py

def main():
    try:
        from sympy import symbols
        from sympy.physics.continuum_mechanics.beam import Beam
        
        # Defining symbols
        E, L, F, B, H = symbols('E L F B H')
        I = B*H**3/12  # Moment of Inertia for the beam's cross-sectional area
        
        b2 = Beam(L, E, I)
        b2.apply_load(-F, L/2, -1)
        b2.apply_support(0, 'fixed')
        
        R0, M0 = symbols('R_0 M_0')
        b2.solve_for_reaction_loads(R0, M0)
        
        # This function call is expected to raise the TypeError we want to catch
        b2.shear_force()
        
        # If the TypeError is not raised by this point, assert an error as the expected condition was not met
        assert False, "The test unexpectedly passed, meaning the issue might have been resolved."

    except TypeError as e:
        # Check if the specific error message is in the exception
        if "_print_SingularityFunction() got an unexpected keyword argument 'exp'" in str(e):
            print("The issue has been reproduced successfully.")
            print_stacktrace(e)
            # Exiting with 0 to indicate the error was successfully reproduced based on the provided setup
            exit(0)
        else:
            # If a TypeError occurred but was not the one we're looking for, re-raise it
            raise
    except Exception as e:
        print("An unexpected error occurred, which may not relate to the reported issue.")
        print_stacktrace(e)
        raise

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

if __name__ == "__main__":
    main()
