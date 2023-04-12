.PHONY: test commit service

service:
	python main.py

test:
	python test.py

commit: 
	git add .
	git commit

fmt:
	python -m black .

all:  test commit service
