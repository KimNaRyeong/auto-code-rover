import logging
import os

# Set up logging with the default format
logging.basicConfig(level=logging.DEBUG, format="%(filename)-25s %(lineno)4d %(levelname)-8s %(message)s")

def main():
    # Create a logger
    logger = logging.getLogger(__name__)

    # Log some messages to demonstrate the issue
    logger.debug("SELECT \"app_url\".\"id\", \"app_url\".\"created\", \"app_url\".\"url\" FROM \"app_url\" WHERE \"app_url\".\"id\" = 2; args=(2,)")
    logger.debug("Calling on_field_start with no data")

    # Check if the issue is present
    log_output = ""
    with open("logging.output", "w") as f:
        logging.basicConfig(level=logging.DEBUG, format="%(filename)-25s %(lineno)4d %(levelname)-8s %(message)s", stream=f)
        logger.debug("SELECT \"app_url\".\"id\", \"app_url\".\"created\", \"app_url\".\"url\" FROM \"app_url\" WHERE \"app_url\".\"id\" = 2; args=(2,)")
        logger.debug("Calling on_field_start with no data")
    with open("logging.output", "r") as f:
        log_output = f.read()

    # Check if the module name is present in the log output
    if "django.db.backends" not in log_output and "multipart.multipart" not in log_output:
        raise AssertionError("Module names are not present in the log output")

    print("Issue is fixed!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
