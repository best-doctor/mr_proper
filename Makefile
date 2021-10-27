test:
	python -m pytest

coverage:
	python -m pytest --cov=mr_proper --cov-report=xml

types:
	mypy .

style:
	flake8 .

readme:
	mdl README.md

requirements:
	safety check -r requirements.txt

check:
	make style
	make types
	make test
	make requirements
