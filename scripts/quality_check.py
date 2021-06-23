import subprocess


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


def show_output(process):
    while True:
        output = process.stdout.readline()
        print(output.strip())
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output
            for output in process.stdout.readlines():
                print(output.strip())
            break


def main():
    run_formatter()
    run_static_check()
    run_import_sort()
    run_security_check()


if __name__ == '__main__':
    main()
