.PHONY: test fmt

all: fmt test

fmt:
	python -m black .

test:
	python test.py

service:
	python main.py
