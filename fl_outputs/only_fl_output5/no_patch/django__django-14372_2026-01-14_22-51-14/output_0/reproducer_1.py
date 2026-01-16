import os
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def setup_django_environment():
    from django.conf import settings
    if not settings.configured:
        settings.configure(
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                '__main__',  # for TestModel
            ],
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': 'db.sqlite3',
                }
            },
            USE_TZ=True,
        )
    import django
    django.setup()

def define_models():
    from django.db import models
    class TestModel(models.Model):
        file = models.FileField(upload_to='uploads/')
    return TestModel

def main():
    setup_django_environment()
    TestModel = define_models()

    # Create a temporary file to simulate file upload
    file_path = 'tmp_test_file.txt'
    with open(file_path, 'w') as f:
        f.write('Temporary file content.')

    try:
        test_model_instance = TestModel()
        with open(file_path, 'rb') as file_obj:
            test_model_instance.file.save('test_uploaded_file.txt', file_obj, save=True)

        # If the script gets to this point without raising an exception, assume the issue is fixed.
        print("The issue is fixed.")
        test_model_instance.file.delete()  # Clean up uploaded file
        os.remove(file_path)  # Clean up temporary file
        exit(0)

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from e

if __name__ == "__main__":
    main()
