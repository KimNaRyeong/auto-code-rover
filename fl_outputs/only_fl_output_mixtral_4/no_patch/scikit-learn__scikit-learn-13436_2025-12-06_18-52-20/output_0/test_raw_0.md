 Here's a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sklearn.compose import ColumnTransformer, Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

numeric_features = ['age', 'fare']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

categorical_features = ['embarked', 'sex', 'pclass']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)])

clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', LogisticRegression(solver='lbfgs'))])

if len(str(clf)) > 1000:
    raise AssertionError("Pretty print representation of the pipeline is too long.")

expected_repr = """\
Pipeline(memory=None,
         steps=[('preprocessor',
                 ColumnTransformer(n_jobs=None, remainder='drop',
                                   sparse_threshold=0.3,
                                   transformer_weights=None,
                                   transformers=[('num',
                                                  Pipeline(memory=None,
                                                           steps=[('imputer',
                                                                   SimpleImputer(strategy='median')),
                                                                  ('scaler',
                                                                   StandardScaler())]),
                                                  ['age', 'fare']),
                                                  ('cat',
                                                   Pipeline(memory=None,
                                                            steps=[('imputer',
                                                                    SimpleImputer(strategy='constant',
                                                                                 fill_value='missing')),
                                                                   ('onehot',
                                                                    OneHotEncoder(handle_unknown='ignore'))]),
                                                  ['embarked', 'sex', 'pclass'])]))],
         verbose=False)"""

if str(clf) != expected_repr:
    raise AssertionError(f"Pretty print representation of the pipeline is incorrect.\nExpected:\n{expected_repr}\nActual:\n{str(clf)}")
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace, as the current `repr` of the `clf` object is too long and does not match the expected output. This reproduces the issue described in the given GitHub issue.