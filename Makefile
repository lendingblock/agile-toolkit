DOCKER_IMAGE ?= platform

.PHONY: help

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

# ===================================================================================================

clean:		## Remove python cache files
	find . -name '__pycache__' | xargs rm -rf
	find . -name '*.pyc' -delete

test:		## Run flake8 and unit tests
	flake8
	pytest --cov

version:	## Display version
	python3 -c "import agilelib; print(agiletoolkit.__version__)"

codecov:
	codecov --token $(CODECOV_TOKEN)
