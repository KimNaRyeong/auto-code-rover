Here is a standalone reproducer script:

```Python
import sklearn

def main():
    try:
        pipe = Pipeline([('anova', SelectKBest(f_regression, k=5)), ('svc', svm.SVC(kernel='linear'))])
        len(pipe)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not reproduced")

if __name__ == "__main__":
    main()
```

This script will attempt to create a Pipeline with SelectKBest and SVM, then try to get its length. If the issue is present, it should raise an exception which we catch and print the stack trace for.