# mr. Propper

Static Python code analyzer, that tries to check if functions in code are
[pure](https://en.wikipedia.org/wiki/Pure_function) or not and why.

*DISCLAIMER*: this library is developer with document driven development,
so some of described functionality may be not true.


## Installation

    pip install mr_propper


## Example
Console usage:

    # test.py
    def add_one(n: int) -> int:
        return n + 1
    
    
    def print_amount_of_users(users_qs: QuerySet) -> None:
        print(f'Current amount of users is {users_qs.count()}')
    
    
    $ mr_propper test.py
    add_one is pure!
    print_amount_of_users is not pure because of:
        it uses forbidden argument types (QuerySet)
        it calls not pure functions (print)
        it has no return

Usage inside Python code sample:

    >>> import ast
    >>> from mr_propper import is_function_pure
    >>> funcdef = ast.parse('''
        def add_one(n: int) -> int:
            return n + 1
    ''').body[0]
    >>> is_function_pure(funcdef)
    True
    >>> is_function_pure(funcdef, with_errors=True)
    (True, [])


## Code prerequisites
1. Python 3.7+;
2. Functions are fully type-annotated;
3. No dynamic calls (line `getattr(sender, 'send_' + message_type)(message)`).


## Contributing

We would love you to contribute to our project. It's simple:

1. Create an issue with bug you found or proposal you have. Wait for approve from maintainer.
2. Create a pull request. Make sure all checks are green.
3. Fix review comments if any.
4. Be awesome.

Here are useful tips:

- You can run all checks and tests with `make check`. Please do it before TravisCI does.
- We use [BestDoctor python styleguide](https://github.com/best-doctor/guides/blob/master/guides/python_styleguide.md). Sorry, styleguide is available only in Russian for now.
- We respect [Django CoC](https://www.djangoproject.com/conduct/). Make soft, not bullshit.
