check:
	make -j2 types style

types:
	mypy --strict --implicit-optional .

style:
	flake8 --use-varnames-strict-mode .
