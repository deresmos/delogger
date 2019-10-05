.PHONY: FORCE

install: FORCE
	pip install . ${ARGS}

install-dev: FORCE
	pip install -e '.[develop]'

upload: FORCE
	python setup.py bdist_wheel
	twine upload dist/*
	rm -rf dist

test: FORCE
	py.test --rootdir=tests
	@echo
	@make -ks check-flake8-results

test-detail: FORCE
	py.test -v --rootdir=tests

format: FORCE
	black ./

check-flake8: FORCE
	find -type f -name '*.py' | flake8

check-flake8-results: FORCE
	@echo '--- flake8 check ---'
	@flake8; \
	if [ $$? = 0 ]; then \
		echo -e '-> \e[32mOK\e[m'; \
	else \
		echo -e '-> \e[31mNG\e[m'; \
		echo; \
		exit 1; \
	fi
