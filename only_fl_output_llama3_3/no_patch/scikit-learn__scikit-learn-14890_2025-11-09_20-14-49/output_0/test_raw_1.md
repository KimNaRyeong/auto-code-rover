The issue seems to be related to the installation of scikit-learn. The error message suggests that scikit-learn has not been built correctly.

To reproduce this issue, you can try installing scikit-learn from source and then running the reproducer script. Here is an example of how you can do it:

```python
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.compose import TransformedTargetRegressor, ColumnTransformer, make_column_transformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression

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

def reproduce_issue():
    try:
        X, y = make_regression(n_samples=10000, noise=100, n_features=10, random_state=2019)
        y = np.exp((y + abs(y.min())) / 200)
        w = np.random.randn(len(X))
        cat_list = ['AA', 'BB', 'CC', 'DD']
        cat = np.random.choice(cat_list, len(X), p=[0.3, 0.2, 0.2, 0.3])

        df = pd.DataFrame(X, columns=["col_" + str(i) for i in range(1, 11)])
        df['sample_weight'] = w
        df['my_caterogy'] = cat

        use_col = [col for col in df.columns if col not in ['sample_weight']]

        numerical_features = df[use_col].dtypes == 'float'
        categorical_features = ~numerical_features

        categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])

        preprocess = make_column_transformer((RobustScaler(), numerical_features), (OneHotEncoder(sparse=False), categorical_features))

        rf = RandomForestRegressor(n_estimators=20)

        clf = Pipeline(steps=[('preprocess', preprocess), ('model', rf)])

        clf_trans = TransformedTargetRegressor(regressor=clf, func=np.log1p, inverse_func=np.expm1)

        # Work
        clf_trans.fit(df[use_col], y)

        # Fail
        try:
            clf_trans.fit(df[use_col], y, sample_weight=df['sample_weight'])
        except Exception as e:
            print_stacktrace(e)
            assert False, "Expected ValueError"

    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected ValueError"

if __name__ == "__main__":
    reproduce_issue()
```

You can install scikit-learn from source by running the following command:

```bash
git clone https://github.com/scikit-learn/scikit-learn.git
cd scikit-learn
python setup.py build
python setup.py install
```

Then, you can run the reproducer script using the following command:

```bash
python3 reproducer.py
```

This should reproduce the issue and print a stack trace.