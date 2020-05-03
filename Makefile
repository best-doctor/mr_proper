check:
	make -j2 test types style requirements

test:
	python -m pytest

types:
	mypy --strict --implicit-optional .

style:
	flake8 --use-varnames-strict-mode .
	mdl README.md

requirements:
	safety check -r requirements.txt
