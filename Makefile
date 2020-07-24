DOCKER_IMAGE ?= platform

.PHONY: help

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

# ===================================================================================================

clean:		## Remove python cache files
	find . -name '__pycache__' | xargs rm -rf
	find . -name '*.pyc' -delete

install:	## Install packages in virtualenv
	@./dev/install.sh

lint:		## run linters
	isort .
	./dev/run-black.sh

test:		## Run unit tests
	@pytest --cov --cov-report xml --cov-report html

test-lint:	## run linters check
	flake8
	isort . --check
	./dev/run-black.sh --check

version:	## Display version
	@python3 -c "import agiletoolkit; print(agiletoolkit.__version__)"

codecov:
	codecov -t $(CODECOV_TOKEN)
