import inspect

def function_with_dict_param(param: dict = None) -> None:
    """
    :param dict(str, str) param: (optional)
    """
    pass


if __name__ == "__main__":
    try:
        # The issue is that the rendered docs show "dict(str,)" instead of "dict(str, str)"
        sig = inspect.signature(function_with_dict_param)
        annotation = sig.parameters["param"].annotation
        assert annotation == dict[str, str]
    except AssertionError as e:
        print_stacktrace(e)
        raise e
