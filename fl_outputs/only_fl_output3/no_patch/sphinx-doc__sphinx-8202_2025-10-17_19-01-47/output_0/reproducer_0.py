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

try:
    from typing import ClassVar, Type, TypeVar, Generic
    
    _ValueType = TypeVar('_ValueType')
    
    class MyGeneric(Generic[_ValueType]):
        #: Doc comment example.
        some_type: ClassVar[Type['MyGenericChild']]
    
    class MyGenericChild(MyGeneric[_ValueType]):
        def __init__(self, inner_value: _ValueType) -> None:
            pass
    
    MyGeneric.some_type = MyGenericChild  # Reassigning to potentially trigger the issue.
    
    # Mimicking the documentation behavior by using vars() might catch docstring anomalies 
    # but will not replicate Sphinx environment fully.
    docs = vars(MyGeneric)
    if not 'some_type' in docs:
        raise AssertionError('Doc comment for some_type is missing or malformed.')
    
    # Trying to access __doc__ to ensure it's still intact and can be triggered as an issue.
    if MyGeneric.some_type.__doc__ is None:
        raise AssertionError('__doc__ of some_type is None, expecting doc comment present.')
    
    print("No issues found with doc comments and Generics.")

except AssertionError as e:
    print_stacktrace(e)
    raise e  # Reraising to ensure non-zero exit if AssertionError is encountered.

except Exception as e:
    print_stacktrace(e)
    exit(1)  # Exit with non-zero due to unexpected issue.

exit(0)  # Exiting with code 0 if everything passed as expected.
