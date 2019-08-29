build:
	pip install -r requirements.txt
run:
	flask run
test:
	nosetests tests -v --with-id
retest:
	nosetests tests -v --failed
coverage:
	nosetests tests -v --with-coverage --cover-erase --cover-package=api --cover-branches
coverage-html:
	nosetests tests -v --with-coverage --cover-erase --cover-package=api --cover-branches --cover-html && open cover/index.html
clean:
	find . -name '__pycache__' -type d | xargs rm -r && rm -rf .coverage .noseids cover