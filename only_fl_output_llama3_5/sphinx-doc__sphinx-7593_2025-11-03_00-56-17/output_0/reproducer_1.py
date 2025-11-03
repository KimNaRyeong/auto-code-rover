from sphinx import version_info as sphinx_version

def reproduce_issue():
    input_string = ":kbd:Control-x Control-f"
    
    try:
        if sphinx_version < (3, 5):
            raise AssertionError("Expected Sphinx version is less than 3.5")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
