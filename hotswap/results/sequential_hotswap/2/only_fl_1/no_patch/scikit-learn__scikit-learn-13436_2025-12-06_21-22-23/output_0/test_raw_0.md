 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
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

if clf.__repr__() != ("Pipeline(memory=None,\n"
                      "         steps=[('preprocessor',\n"
                      "                 ColumnTransformer(n_jobs=None,\n"
                      "                                   remainder='drop',\n"
                      "                                   sparse_threshold=0.3,\n"
                      "                                   transformer_weights=None,\n"
                      "                                   transformers=[('num',\n"
                      "                                                  Pipeline(memory=None,\n"
                      "                                                           steps=[('imputer',\n"
                      "                                                                   SimpleImputer(strategy='median',\n"
                      "                                                                                missing_values=nan,\n"
                      "                                                                                copy=True)],\n"
                      "                                                           verbose=0),\n"
                      "                                                   ('scaler',\n"
                      "                                                    StandardScaler(copy=True,\n"
                      "                                                                    with_mean=True,\n"
                      "                                                                    with_std=True))]),\n"
                      "                                                 ('cat',\n"
                      "                                                  Pipeline(memory=None,\n"
                