install:
	pip install . ${ARGS}

install-dev:
	pip install -e '.[develop]'

test:
	py.test --rootdir=tests
	@echo
	@make -ks check-flake8-results

test-detail:
	py.test -v --rootdir=tests

check-flake8:
	find -type f -name '*.py' | flake8

check-flake8-results:
	@echo '--- flake8 check ---'
	@find -type f -name '*.py' | flake8; \
	if [ $$? = 0 ]; then \
		echo -e '-> \e[32mOK\e[m'; \
	else \
		echo -e '-> \e[31mNG\e[m'; \
		echo; \
		exit 1; \
	fi
