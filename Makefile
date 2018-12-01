.PHONY: tests

install:
	pipenv install

uninstall:
	pipenv --rm

shell:
	pipenv shell

style:
	pipenv run pycodestyle .

sort:
	pipenv run isort -rc . -s ./lib

tests:
	python3 -m unittest
