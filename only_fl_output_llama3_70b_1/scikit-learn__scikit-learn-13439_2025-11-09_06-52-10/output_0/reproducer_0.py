import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    from sklearn import svm
    from sklearn.datasets import samples_generator
    from sklearn.feature_selection import SelectKBest, f_regression
    from sklearn.pipeline import Pipeline

    X, y = samples_generator.make_classification(
        n_informative=5, n_redundant=0, random_state=42)

    anova_filter = SelectKBest(f_regression, k=5)
    clf = svm.SVC(kernel='linear')
    pipe = Pipeline([('anova', anova_filter), ('svc', clf)])

    len(pipe)  # This should raise a TypeError

except Exception as e:
    print_stacktrace(e)
    assert False, "Pipeline should implement __len__"
