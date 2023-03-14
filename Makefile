.PHONY: test commit service

all:  test commit service

test:
	python test.py

commit: 
	git add .
	git commit -m "commit"

service:
	python main.py
