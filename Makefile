check:
	make -j2 types style

types:
	mypy --strict .

style:
	flake8 --use-varnames-strict-mode .
