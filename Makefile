PORT := 8000
DEBUG := True
APIHOST := localhost:8101
ENV = PORT=$(PORT) DJANGO_DEBUG=$(DEBUG) APIHOST=$(APIHOST)
VENV = venv/bin/python
SCRIPTS = $(shell pwd)/mns/static/scripts


.PHONY: test run nose jasmine_tests

run:
	$(ENV) $(VENV) manage.py runserver

test: nose jasmine

nose:
	$(ENV) $(VENV) manage.py test mns

jasmine:
	phantomjs $(SCRIPTS)/lib/test_runner.js $(SCRIPTS)/unit_tests.html
