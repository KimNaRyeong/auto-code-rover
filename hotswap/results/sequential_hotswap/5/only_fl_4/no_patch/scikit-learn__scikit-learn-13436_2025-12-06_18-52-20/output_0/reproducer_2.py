import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class ColumnTransformer:
    def __init__(self, transformers):
        self.transformers = transformers

    def __repr__(self):
        result = []
        for name, transformer, features in self.transformers:
            result.append(f"    ({name}, {transformer}, {features})")
        return f"ColumnTransformer({result})"

class Pipeline:
    def __init__(self, steps):
        self.steps = steps

    def __repr__(self):
        result = []
        for name, transformer in self.steps:
            result.append(f"    {name}: {transformer}")
        return f"Pipeline([{', '.join(result)}])"

if __name__ == "__main__":
    numeric_features = ['age', 'fare']
    numeric_transformer = Pipeline(steps=[
        ('imputer', 'SimpleImputer(strategy=\'median\')'),
        ('scaler', 'StandardScaler()')])

    categorical_features = ['embarked', 'sex', 'pclass']
    categorical_transformer = Pipeline(steps=[
        ('imputer', 'SimpleImputer(strategy=\'constant\', fill_value=\'missing\')'),
        ('onehot', 'OneHotEncoder(handle_unknown=\'ignore\')')])

    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])

    clf = Pipeline(steps=[('preprocessor', preprocessor),
                          ('classifier', 'LogisticRegression(solver=\'lbfgs\')')])

    if len(str(clf)) > 1000:
        raise AssertionError("Pretty print representation of the pipeline is too long.")

    expected_repr = """\
Pipeline(steps=[('preprocessor',
                 ColumnTransformer(transformers=[('num',
                                                  Pipeline(steps=[('imputer',
                                                                  'SimpleImputer(strategy=\'median\')'),
                                                                 ('scaler',
                                                                  'StandardScaler()')]),
                                                  ['age', 'fare']),
                                                  ('cat',
                                                   Pipeline(steps=[('imputer',
                                                                   'SimpleImputer(strategy=\'constant\', fill_value=\'missing\')'),
                                                                  ('onehot',
                                                                   'OneHotEncoder(handle_unknown=\'ignore\')')]),
                                                  ['embarked', 'sex', 'pclass'])]))],
         verbose=False)"""

    if str(clf) != expected_repr:
        raise AssertionError(f"Pretty print representation of the pipeline is incorrect.\nExpected:\n{expected_repr}\nActual:\n{str(clf)}")
