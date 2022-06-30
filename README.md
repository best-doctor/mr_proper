# mr. Proper

[![Build Status](https://travis-ci.org/best-doctor/mr_proper.svg?branch=master)](https://travis-ci.org/best-doctor/mr_proper)
[![PyPI version](https://badge.fury.io/py/mr-proper.svg)](https://badge.fury.io/py/mr-proper)
[![Maintainability](https://api.codeclimate.com/v1/badges/4b2234d95d5c4944e2e6/maintainability)](https://codeclimate.com/github/best-doctor/mr_proper/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/4b2234d95d5c4944e2e6/test_coverage)](https://codeclimate.com/github/best-doctor/mr_proper/test_coverage)

Static Python code analyzer, that tries to check if functions in code are
[pure](https://en.wikipedia.org/wiki/Pure_function) or not and why.

![Have fun with mr Clean](https://raw.githubusercontent.com/best-doctor/mr_proper/master/docs_img/mr_clean_sponge.jpg)

*DISCLAIMER*: this library is very experimental and has a lot of edge cases.
Functions that mr. Proper marks as pure can be not pure, but they are
usually cleaner than other functions.

## Installation

```bash
pip install mr_proper
```

## What mr. Proper check

1. that function has no blacklisted calls (like `print`)
   and blacklisted attributes access (like `smth.count`);
1. that function not uses global objects (only local vars and function arguments);
1. that function has al least one return;
1. that function not mutates it's arguments;
1. that function has no local imports;
1. that function has no arguments of forbidden types (like ORM objects);
1. that function not uses `self`, `class` or `super`;
1. that function has calls of only pure functions.

This list is not enough to say that function is pure and some points
are quite controversial, but it's a nice start.

## Example

Console usage:

```python
    # test.py
    def add_one(n: int) -> int:
        return n + 1

    def print_amount_of_users(users_qs: QuerySet) -> None:
        print(f'Current amount of users is {users_qs.count()}')
```

```bash
$ mr_propper test.py
add_one is pure!
print_amount_of_users is not pure because of:
    it uses forbidden argument types (QuerySet)
    it calls not pure functions (print)
    it has no return
```

Usage inside Python code sample:

```jupyterpython
>>> import ast
>>> from mr_propper.utils import is_function_pure
>>> funcdef = ast.parse('''
    def add_one(n: int) -> int:
        return n + 1
''').body[0]
>>> is_function_pure(funcdef)
True
>>> is_function_pure(funcdef, with_errors=True)
(True, [])
```

## Parameters

CLI interface:

- `filepath`: path to .py file to check (directories are not supported for now);
- `--recursive`: require inner calls to be pure for function pureness.

## Code prerequisites

1. Python 3.7+;
1. Functions are fully type-annotated;
1. No dynamic calls (like `getattr(sender, 'send_' + message_type)(message)`).

## Contributing

We would love you to contribute to our project. It's simple:

1. Create an issue with bug you found or proposal you have.
   Wait for approve from maintainer.
1. Create a pull request. Make sure all checks are green.
1. Fix review comments if any.
1. Be awesome.

Here are useful tips:

- You can run all checks and tests with `make check`.
  Please do it before TravisCI does.
- We use [BestDoctor python styleguide](https://github.com/best-doctor/guides/blob/master/guides/en/python_styleguide.md).
- We respect [Django CoC](https://www.djangoproject.com/conduct/).
  Make soft, not bullshit.
