import subprocess
from helper import show_output


def run_formatter():
    process = subprocess.Popen(['black', '../mailguard'],
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
    show_output(process)


def run_static_check():
    process = subprocess.Popen(['flake8', '../mailguard'],
                               stdout=subprocess.PIPE,
                               universal_newlines=True)
    show_output(process)


def run_import_sort():
    process = subprocess.Popen(['isort', '../mailguard'],
                               stdout=subprocess.PIPE,
                               universal_newlines=True)

    show_output(process)


def run_security_check():
    process = subprocess.Popen(['bandit', '-r', '../mailguard'],
                               stdout=subprocess.PIPE,
                               universal_newlines=True)

    show_output(process)


def main():
    # TODO: add output checks to raise error when e.g. static checks has warnings
    run_formatter()
    run_static_check()
    run_import_sort()
    run_security_check()


if __name__ == '__main__':
    main()
