"""
Employee data library.  Organize employees into hierarchy and render
details into a useful ascii format for printing.
"""

import json
from textwrap import indent, dedent
from collections import defaultdict

import jsonschema


# JSON Schema for input data structure
schema = {
    "type": "array",
    "items": {
        "type" : "object",
        "required": ["first_name", "id", "manager", "salary"],
        "additionalProperties": False,
        "properties" : {
            "first_name" : {"type" : "string"},
            "id" : {"type" : "number"},
            "manager" : {"type" : ["number", "null"]},
            "salary" : {"type" : "number"},
        }
    }
}


def read_employee_list(filename):
    """
    Read employee-list JSON into python.
    """
    with open(filename) as handle:
        return json.load(handle)


def validate_employee_list(employees):
    """
    Surface level validation of input data.  An empty response is returned when
    the employee list is valid.

    NOTE - Does not check for things like duplicate keys, that manager mentioned
    actually exists in roster, or that there are not any cyclic relationships.
    """
    # Note: no particular reason to use this draft version.  It does what I need, so
    # I saw no need to change it.
    validator = jsonschema.Draft7Validator(schema)

    # Sort for consistent output
    return sorted(e.message for e in validator.iter_errors(employees))


def build_hierarchies(employee_list):
    """
    Build recursive hierarchy structures representing the management trees.
    """
    managers = defaultdict(list)
    for employee in employee_list:
        managers[employee['manager']].append({
            'id': employee['id'],
            'first_name': employee['first_name'],
        })

    # Nest managers within managers
    for employees in managers.values():
        for employee in employees:
            empid = employee['id']
            if empid in managers:
                employee['employees'] = managers[empid]

    # Assuming the tree is well formed, all employees should be captured
    # by returning all top-level managers
    return managers[None]


def render_employees_summary(employees):
    """
    Render complete summary of employee list.
    This includes the hierarchies and sum total of employee salaries.
    """
    # Render employee hierarchies.  Also, strip off any excess indentation or
    # trailing whitespace
    hierarchies = build_hierarchies(employees)
    rendered_hierarchies = dedent(render_employees(hierarchies)).strip()

    # Sum all employee salaries
    total_salary = sum(x['salary'] for x in employees)

    return f"{rendered_hierarchies}\n\nTotal salary: {total_salary}"


def render_employees(hierarchies):
    """
    Render sorted list of employees as printable ASCII tree.
    """
    # Sort employee-list each each level of the hierarchy
    hierarchies = sorted(hierarchies, key=lambda h: h['first_name'])

    # Indent to create "ascii tree" look
    return indent('\n'.join(render_employee(e) for e in hierarchies), '    ')


def render_employee(employee):
    """
    Render employee as printable ASCII tree.
    """
    result = f"- {employee['first_name']}"

    # Additional details for managers
    if 'employees' in employee:
        employees = render_employees(employee['employees'])
        result += f"\n  Employees:\n{employees}"

    return result
