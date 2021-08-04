import subprocess
from helper import show_output


def run_tests():
    process = subprocess.Popen(['cd .. && coverage run -m pytest tests'],
                               stdout=subprocess.PIPE,
                               universal_newlines=True,
                               shell=True)
    show_output(process)


def generate_html():
    process = subprocess.Popen(['cd .. && coverage html'],
                               stdout=subprocess.PIPE,
                               universal_newlines=True,
                               shell=True)

    show_output(process)


def main():
    # TODO: move config and runner into tox
    run_tests()
    generate_html()


if __name__ == '__main__':
    main()
