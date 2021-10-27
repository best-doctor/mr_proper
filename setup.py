from typing import Optional

from setuptools import setup, find_packages


package_name = 'mr_proper'


def get_version() -> Optional[str]:
    with open('mr_proper/__init__.py', 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('__version__'):
            return line.split('=')[-1].strip().strip("'")


def get_long_description() -> str:
    with open('README.md', encoding='utf8') as f:
        return f.read()


setup(
    name=package_name,
    description='Static Python code analyzer, that tries to check if functions in code are pure or not and why.',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    keywords=['static-analyzer', 'pure-function'],
    version=get_version(),
    author='Ilya Lebedev',
    author_email='melevir@gmail.com',
    install_requires=[
        'click>=7.1.2',
        'setuptools',
        'stdlib-list>=0.5.0',
        'typing-extensions>=3.7.4.3;python_version<"3.8"',
    ],
    entry_points={
        'console_scripts': [
            'mr_proper = mr_proper.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    url='https://github.com/best-doctor/mr_proper',
    license='MIT',
    py_modules=[package_name],
    zip_safe=False,
)
