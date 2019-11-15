check:
	make -j3 test types style

test:
	python -m pytest

types:
	mypy --strict --implicit-optional .

style:
	flake8 --use-varnames-strict-mode .
