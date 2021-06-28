"""
CLI entry-point for employee hierarchy report.
"""

import argparse

from employees import (read_employee_list, render_employees_summary,
        validate_employee_list)


def main(args):
    """
    Main entry-point for employee pretty-printing script.
    """
    employees = read_employee_list(args.input_file)

    validation_errors = validate_employee_list(employees)

    if validation_errors:
        print("There were errors while validating employee list!")

        for err in validation_errors:
            print(f' - {err}')

        print("Please fix these errors and try again.")

    else:
        print(render_employees_summary(employees))


def get_args():
    """
    Run argument-parser for usage statement run configuration details from the
    user.
    """
    parser = argparse.ArgumentParser(description='Pretty-print employee hierarchy')
    parser.add_argument('input_file', type=str, help='Input JSON file to process')

    return parser.parse_args()


if __name__ == '__main__':
    main(get_args())
