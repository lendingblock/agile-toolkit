DOCKER_IMAGE ?= platform

.PHONY: help

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

# ===================================================================================================

bundle3.6:		## build python bundle
	@python setup.py bdist_wheel --python-tag py36

bundle3.7:		## build python bundle
	@python setup.py bdist_wheel --python-tag py37

bundle3.8:		## build python bundle
	@python setup.py sdist bdist_wheel --python-tag py38

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
	@python setup.py --version

codecov:
	codecov -t $(CODECOV_TOKEN)

release-github:	## new tag in github
	@python agile.py git release --yes

release-pypi:	## release to pypi and github tag
	@twine upload dist/* --username lsbardel --password $(PYPI_PASSWORD)

test-version:	## validate version
	@python agile.py git validate --yes-no
