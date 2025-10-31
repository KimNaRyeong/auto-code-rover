Here is the reproducer script:

```python
import sklearn
from sklearn import datasets, svm, feature_selection
from sklearn.pipeline import Pipeline

def main():
    X, y = datasets.samples_generator.make_classification(n_informative=5, n_redundant=0, random_state=42)

    anova_filter = feature_selection.SelectKBest(feature_selection.f_regression, k=5)
    clf = svm.SVC(kernel='linear')
    pipe = Pipeline([('anova', anova_filter), ('svc', clf)])

    try:
        len(pipe)
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script should be saved in a file named `reproducer.py` and executed with the command `python3 reproducer.py`. If the issue is present, it will print the stack trace of the error.