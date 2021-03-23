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
deploy:
	gunicorn -w 4 "api.app:create_app('production')"

docker-all: docker-build push

docker-build:
	docker build -t lab_database_api:latest .

push:
	docker tag lab_database_api:latest registry.jvansan.duckdns.org/lab_database_api:latest
	docker push registry.jvansan.duckdns.org/lab_database_api:latest