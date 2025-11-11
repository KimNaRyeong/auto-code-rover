import django.utils.dateparse

def reproduce_issue():
    try:
        datetime_obj = django.utils.dateparse.parse_datetime("2012-04-23T10:20:30.400 -02")
        assert datetime_obj is not None, "Issue reproduced"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
