.PHONY: FORCE

install: FORCE
	poetry install --no-dev

install-dev: FORCE
	poetry install

upload: build
	@poetry publish -u ${PYPI_USER} -p ${PYPI_PASSWORD}

upload-test: build
	@poetry config repositories.testpypi https://test.pypi.org/legacy/
	@poetry publish -r testpypi -u ${PYPI_USER} -p ${PYPI_PASSWORD}

build: FORCE
	poetry build

test: FORCE
	poetry run pytest tests
	@echo
	# @make -ks check-flake8-results

test-detail: FORCE
	poetry run pytest tests -v --durations=5

test-detail-log: FORCE
	poetry run pytest tests -v --durations=5 -s

test-coverage: FORCE
	poetry run pytest tests -v --cov=delogger --cov-report=term-missing

test-coverage-html: FORCE
	poetry run pytest tests -v --cov=delogger --cov-report=html

format: FORCE
	isort ./
	poetry run black ./

check-flake8: FORCE
	find -type f -name '*.py' | poetry run flake8

check-flake8-results: FORCE
	@echo '--- flake8 check ---'
	@poetry run flake8; \
	if [ $$? = 0 ]; then \
		echo -e '-> \e[32mOK\e[m'; \
	else \
		echo -e '-> \e[31mNG\e[m'; \
		echo; \
		exit 1; \
	fi
