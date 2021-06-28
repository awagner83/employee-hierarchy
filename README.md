# Employee Report

## Usage

    python main.py input.json

### Examples

    python main.py test/fixtures/input.json
    python main.py test/fixtures/bad_input.json

## Running Tests

    pytest

## Features

- Organizes employees by manager and outputs a sum of all salaries.
- Surface-level validation of input.  This ensures that fields are of the right
  type, and all required fields are supplied.
- Sorts output alphabetically at each level in the hierarchy.

## Known issues / assumptions

- Validation does not check for duplication in ids.
- Validation does not check that manager-ids mentioned actually exist.
- Validation does not check for cyclic relationships.  Input must be a DAG.
- Oraganizations with extremely deep org charts may cause the
  max-recursion-depth to be exceeded.

