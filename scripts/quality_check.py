import subprocess
from helper import show_output


def run_formatter():
    process = subprocess.Popen(['black', '../src/mailguard'],
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
    show_output(process)


def run_import_sort():
    process = subprocess.Popen(['isort', '../src/mailguard'],
                               stdout=subprocess.PIPE,
                               universal_newlines=True)

    show_output(process)


def main():
    run_formatter()
    run_import_sort()


if __name__ == '__main__':
    main()
