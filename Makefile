.PHONY: test fmt

all: fmt test

fmt:
	python -m black .

test:
	python test.py

