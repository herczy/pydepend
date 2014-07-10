.PHONY: all
all: check

.PHONY: check
check: check-python2.7 check-python3.2

.PHONY: check-python2.7
check-python2.7:
	nosetests-2.7 -s pydepend

.PHONY: check-python3.2
check-python3.2:
	nosetests-3.2 -s pydepend
