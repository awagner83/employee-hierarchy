"""
Test employee-data library.
"""

import pytest

from employees import (read_employee_list, validate_employee_list,
        build_hierarchies, render_employees, render_employees_summary)


@pytest.fixture
def employee_list():
    """Happy-path employee list input"""
    return [
        {"first_name": "Dave", "id": 1, "manager": 2, "salary": 100000},
        {"first_name": "Jeff", "id": 2, "manager": None, "salary": 110000},
        {"first_name": "Andy", "id": 3, "manager": 1, "salary": 90000},
        {"first_name": "Jason", "id": 4, "manager": 1, "salary": 80000},
        {"first_name": "Dan", "id": 5, "manager": 1, "salary": 70000},
        {"first_name": "Rick", "id": 6, "manager": 1, "salary": 60000},
        {"first_name": "Suzanne", "id": 9, "manager": 1, "salary": 80000},
    ]


@pytest.fixture
def bad_employee_list():
    """Employee-list input that should fail validation."""
    return [
        {"first_name": "Dave", "manager": 2, "salary": 100000},
        {"first_name": None, "id": 2, "manager": None, "salary": 110000},
        {"first_name": 5, "id": 3, "manager": 1, "salary": 90000},
        {"first_name": "Jason", "id": 4, "salary": 80000},
        {"first_name": "Dan", "id": 5, "manager": 1, "salary": "one million"},
        {"first_name": "Suzanne", "id": 9, "manager": 1, "salary": 80000, "age": 34},
    ]


@pytest.fixture
def employee_hierarchies():
    """Happy-path employee hierarchy structure."""
    return [
        {
            'id': 2,
            'first_name': 'Jeff',
            'employees': [
                {
                    'id': 1,
                    'first_name': 'Dave',
                    'employees': [
                        {'id': 3, 'first_name': 'Andy'},
                        {'id': 4, 'first_name': 'Jason'},
                        {'id': 5, 'first_name': 'Dan'},
                        {'id': 6, 'first_name': 'Rick'},
                        {'id': 9, 'first_name': 'Suzanne'}
                    ]
                }
            ]
        }
    ]



def test_read_employee_list(employee_list):
    """Test loading employee list."""
    actual = read_employee_list("test/fixtures/input.json")
    expected = employee_list

    assert actual == expected


def test_validate_employee_list(employee_list):
    """Test validating employee list."""
    assert validate_employee_list(employee_list) == []


def test_validate_employee_list_bad(bad_employee_list):
    """Ensure validation of bad input data results in the correct errors."""
    assert validate_employee_list(bad_employee_list) == [
        "'id' is a required property",
        "'manager' is a required property",
        "'one million' is not of type 'number'",
        "5 is not of type 'string'",
        "Additional properties are not allowed ('age' was unexpected)",
        "None is not of type 'string'"
    ]


def test_build_hierarchies(employee_list, employee_hierarchies):
    """Ensure happy-path data produces happy-path hierarchies."""
    assert build_hierarchies(employee_list) == employee_hierarchies


def test_render_employees(employee_hierarchies):
    """Test rendering hierarchies."""
    actual = render_employees(employee_hierarchies).strip()
    expected = str(open('test/fixtures/output_hierarchy').read()).strip()

    assert actual == expected


def test_render_employees_summary(employee_list):
    """Test rendering entire employee summary."""
    actual = render_employees_summary(employee_list).strip()
    expected = str(open('test/fixtures/output').read()).strip()

    assert actual == expected
