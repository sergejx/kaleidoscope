all: typecheck test

typecheck:
	mypy --ignore-missing-imports -p kaleidoscope

test:
	python -m unittest tests
