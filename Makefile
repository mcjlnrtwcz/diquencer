.PHONY: tests

install:
	pipenv install

install_dev:
	pipenv install -d

uninstall:
	pipenv --rm

shell:
	pipenv shell

format:
	pipenv run black .

sort:
	pipenv run isort -rc .

lint:
	pipenv run flake8 .

mypy:
	pipenv run mypy diquencer --config-file tox.ini
