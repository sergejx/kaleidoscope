all: typecheck test

typecheck:
	mypy --check-untyped-defs -p kaleidoscope

test:
	python -m unittest tests
