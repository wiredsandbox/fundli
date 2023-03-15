.PHONY: test commit service

all:  test commit service

test:
	python test.py

commit: 
	git add .
	git commit

service:
	python main.py

deploy:
	git push heroku main
