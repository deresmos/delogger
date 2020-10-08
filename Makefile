.PHONY: FORCE

install: FORCE
	poetry install --no-dev

install-dev: FORCE
	poetry install

upload: FORCE
	python setup.py bdist_wheel
	twine upload dist/*
	rm -rf dist

test: FORCE
	poetry run pytest --rootdir=tests
	@echo
	# @make -ks check-flake8-results

test-detail: FORCE
	poetry run pytest -v --rootdir=tests --durations=5

format: FORCE
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
