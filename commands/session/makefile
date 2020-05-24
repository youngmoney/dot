TEST_NAMES=$(patsubst test/%_test.py,test.%_test,$(wildcard test/*_test.py))

default: test

%_test.py:
	python3 -m unittest $@

test:
	python3 -m unittest discover -p '*_test.py'
