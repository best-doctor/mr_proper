from setuptools import setup, find_packages


package_name = 'mr_proper'


def get_long_description() -> str:
    with open('README.md', encoding='utf8') as f:
        return f.read()


setup(
    name=package_name,
    description='Package to find typos in russian text.',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    keywords='typos',
    version='0.0.1',
    author='Ilya Lebedev',
    author_email='melevir@gmail.com',
    install_requires=[
        'setuptools',
        'stdlib-list>=0.5.0',
        'mypy-extensions==0.4.1',
    ],
    entry_points={
        'console_scripts': [
            'mr_proper = mr_proper.main:main',
        ],
    },
    url='https://github.com/best-doctor/mr_proper',
    license='MIT',
    py_modules=[package_name],
    zip_safe=False,
)
