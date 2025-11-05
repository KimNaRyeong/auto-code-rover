import sys
from argparse import ArgumentParser, SUPPRESS

def main():
    parser = ArgumentParser(description='Pylint Reproducer')
    parser.add_argument('-v', '--verbose', help='Set verbosity level')

    args, _ = parser.parse_known_args()

    if not hasattr(args, 'verbose') or not args.verbose:
        print_stacktrace(AssertionError('Argument expected for short verbose option'))
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
