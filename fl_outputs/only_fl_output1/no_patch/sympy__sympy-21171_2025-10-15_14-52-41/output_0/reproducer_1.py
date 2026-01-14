# reproducer.py
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
    try:
        from sympy import symbols, init_printing
        from sympy.physics.continuum_mechanics import Beam

        # Initialize pretty printing
        init_printing(use_latex='png')

        # Define symbols
        E, L, F, B, H = symbols("E L F B H")
        I = B * H**3 / 12  # Moment of Inertia
        
        # Beam setup
        b2 = Beam(L, E, I)
        b2.apply_load(-F, L / 2, -1)
        b2.apply_support(0, "fixed")
        R0, M0 = symbols("R_0 M_0")
        b2.solve_for_reaction_loads(R0, M0)
        
        # This command tries to show shear force visually, potentially causing the issue due to LaTeX parsing.
        s = b2.shear_force()
        
        # Trying to print or represent the shear force could trigger the exception
        from sympy.printing.latex import latex
        _ = latex(s)  # Explicitly using the latex function to simulate the rendering
        
        # If no exception is raised so far, assume the issue is resolved
        print("Issue fixed, no error occurred.")

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.")

if __name__ == "__main__":
    main()
