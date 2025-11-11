Here is the reproducer script:

```python
import sklearn
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression

def main():
    try:
        clf = make_pipeline(LogisticRegression())
        clf.fit([[0], [0]], [0, 1], logisticregression__sample_weight=[1, 1])
        clf.fit([[0], [0]], [0, 1], sample_weight=[1, 1])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    main()
```

This script attempts to create a pipeline with a logistic regression step and then tries to fit the data using both the correct and incorrect formats for passing `sample_weight`. If an error occurs, it prints the stack trace and raises an assertion error.