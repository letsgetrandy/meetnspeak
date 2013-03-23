APIHOST := localhost:8101
TEST_CMD = python manage.py test mns


.PHONY: test

test:
	APIHOST=$(APIHOST) \
	$(TEST_CMD)
