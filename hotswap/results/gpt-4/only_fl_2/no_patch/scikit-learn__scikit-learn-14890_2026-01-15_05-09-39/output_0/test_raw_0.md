```python
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

def test_transformed_target_regressor_with_sample_weight():
    import pandas as pd
    import numpy as np
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import RobustScaler, OneHotEncoder
    from sklearn.compose import TransformedTargetRegressor, make_column_transformer
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.datasets import make_regression
    
    # Create dataset
    X, y = make_regression(n_samples=10000, noise=100, n_features=10, random_state=2019)
    y = np.exp((y + abs(y.min())) / 200)
    w = np.random.randn(len(X))
    cat_list = ['AA', 'BB', 'CC', 'DD']
    cat = np.random.choice(cat_list, len(X), p=[0.3, 0.2, 0.2, 0.3])
    
    df = pd.DataFrame(X, columns=["col_" + str(i) for i in range(1, 11)])
    df['sample_weight'] = w
    df['my_caterogy'] = cat

    use_col = [col for col in df.columns if col not in ['sample_weight']]

    numerical_features = (df[use_col].dtypes == 'float').values
    categorical_features = ~numerical_features

    preprocess = make_column_transformer(
                                        (RobustScaler(), numerical_features),
                                        (OneHotEncoder(sparse=False), categorical_features)
    )
    
    rf = RandomForestRegressor(n_estimators=20)
    
    clf = Pipeline(steps=[
                          ('preprocess', preprocess),
                          ('model', rf)
    ])
    
    clf_trans = TransformedTargetRegressor(regressor=clf,
                                            func=np.log1p,
                                            inverse_func=np.expm1)
    
    try:
        # Work
        clf_trans.fit(df[use_col], y)
        # Fail
        clf_trans.fit(df[use_col], y, sample_weight=df['sample_weight'])
        print("No AssertionError, the issue seems to be fixed.")
    except Exception as e:
        print_stacktrace(e)
        assert isinstance(e, ValueError), "Expected a ValueError, got a different exception."

if __name__ == "__main__":
    try:
        test_transformed_target_regressor_with_sample_weight()
    except AssertionError as e:
        print_stacktrace(e)
        raise e
```
This script reproduces the described issue in the question. It creates a pandas DataFrame with a mix of numerical and categorical data, then tries to fit a `TransformedTargetRegressor` with sample weights through a pipeline, expecting it to raise a `ValueError` when the issue is present, and catch other exceptions that indicate different problems. The script uses a specific function to print stack traces of any raised exceptions, providing clarity on where and why the exception occurred.