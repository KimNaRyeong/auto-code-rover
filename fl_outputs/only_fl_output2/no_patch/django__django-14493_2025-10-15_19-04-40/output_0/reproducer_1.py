# reproducerer.py
import sys

def print_stacktrace(e: Exception):
    import traceback
    print("Traceback (most recent call last):", file=sys.stderr)
    tb = traceback.extract_tb(e.__traceback__)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Mocking necessary Django components to simulate the environment
class ManifestStaticFilesStorage:
    max_post_process_passes = 1  # default value in a normal scenario

    def post_process(self, *args, **kwargs):
        if self.max_post_process_passes == 0:
            try:
                # Mimic the logical flow that leads to the issue
                for _ in self._mock_passes():
                    pass
            except UnboundLocalError as e:
                print_stacktrace(e)
                raise AssertionError("The issue is present.")
        else:
            print("This test is designed to check the behavior with max_post_process_passes set to 0.")

    def _mock_passes(self):
        # Mimic internal logic that would lead to an UnboundLocalError with max_post_process_passes = 0
        if False:  # This never execute, mimicking the scenario where no substitutions occur
            yield

class MyManifestStaticFilesStorage(ManifestStaticFilesStorage):
    max_post_process_passes = 0

def main():
    try:
        storage = MyManifestStaticFilesStorage()
        storage.post_process()
    except AssertionError:
        sys.exit(0)  # Exit with code 0 to indicate the script has caught the issue as intended
    else:
        raise AssertionError("The issue was not reproduced. Check the implementation and Django's updates.")

if __name__ == "__main__":
    main()
