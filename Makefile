PORT := 8000
DEBUG := True
APIHOST := localhost:8101
APIDIR := ../meetnspeak
ENV = PORT=$(PORT) DJANGO_DEBUG=$(DEBUG) APIHOST=$(APIHOST)
VENV = venv/bin/python
SCRIPTS = $(shell pwd)/mns/static/scripts


run:
	$(ENV) $(VENV) manage.py runserver

test: nose jasmine

nose:
	$(ENV) $(VENV) manage.py test mns

jasmine:
	phantomjs $(SCRIPTS)/lib/test_runner.js $(SCRIPTS)/unit_tests.html

deploy: deployapi
	git push heroku master

deployapi:
	cd $(APIDIR)
	appcfg.py update ~/dev/meetnspeak
	cd -

.PHONY: test run nose jasmine_tests
