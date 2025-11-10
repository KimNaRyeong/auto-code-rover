Here is the reproducer script:

```python
import sklearn.pipeline as pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.exceptions import NotFittedError

def main():
    try:
        clf = pipeline.make_pipeline(LogisticRegression())
        clf.fit([[0], [0]], [0, 1], logisticregression__sample_weight=[1, 1])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    main()
```

This script will attempt to create a pipeline with a LogisticRegression estimator and then fit the pipeline using sample weights. If the issue is present (i.e., the error message is not friendly enough), it will print the stack trace and raise an AssertionError.