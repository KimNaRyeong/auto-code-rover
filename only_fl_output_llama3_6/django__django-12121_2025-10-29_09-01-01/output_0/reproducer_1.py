def to_url(value):
    if value < 10:
        return 'export/foo/<foo:obj>'
    else:
        return ''

def main():
    try:
        url = to_url(5)
        assert not bool(url), "Expected empty string"
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
