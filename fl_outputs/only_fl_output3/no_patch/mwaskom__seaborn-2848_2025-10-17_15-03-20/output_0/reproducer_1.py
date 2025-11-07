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

def test_seaborn_pairgrid_hue_in_map():
    try:
        import seaborn as sns
        # Checking seaborn's version
        assert sns.__version__ == '0.11.1', "This script expects seaborn version 0.11.1"
        import matplotlib.pyplot as plt  # Ensure matplotlib is available
        iris = sns.load_dataset("iris")
        g = sns.PairGrid(iris, y_vars=["sepal_length", "sepal_width"], x_vars=["petal_length", "petal_width"])
        g.map(sns.scatterplot, hue=iris["species"])
        g.map(sns.regplot, scatter=False)
        print("The issue has been fixed.")
    except AssertionError as ae:
        raise AssertionError(ae)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is still present.")

if __name__ == "__main__":
    test_seaborn_pairgrid_hue_in_map()
