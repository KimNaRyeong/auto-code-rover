Here is a standalone python file `reproducer.py` that reproduces the issue:

```py
import sklearn.pipeline as pipeline
from sklearn.linear_model import LogisticRegression

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

This script should be placed in the root directory of the project and executed by `python3 reproducer.py`. The script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.