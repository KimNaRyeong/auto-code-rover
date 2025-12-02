class HttpResponse:
    def __init__(self, content=None, content_type=None, status=None, charset=None):
        self.content = content

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    # String content
    response = HttpResponse(content="My Content")
    assert isinstance(response.content, str), "HttpResponse.content should be str"

    # Bytes content
    response = HttpResponse(content=b"My Content")
    assert isinstance(response.content, bytes), "HttpResponse.content should be bytes"

    # memoryview content
    response = HttpResponse(content=memoryview(b"My Content"))
    assert isinstance(response.content, bytes), "HttpResponse.content should be bytes"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
