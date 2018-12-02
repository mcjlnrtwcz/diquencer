.PHONY: tests

install:
	pipenv install

install_dev:
	pipenv install -d

uninstall:
	pipenv --rm

shell:
	pipenv shell

style:
	pipenv run pycodestyle .

sort:
	pipenv run isort -rc .

tests:
	pipenv run python3.6 -m unittest
