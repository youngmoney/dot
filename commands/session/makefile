TEST_NAMES=$(patsubst test/%_test.py,test.%_test,$(wildcard test/*_test.py))

default: test

%_test.py:
	python -m unittest $@

test:
	python -m unittest discover -p '*_test.py'
