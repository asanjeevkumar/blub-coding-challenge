export PYTHONPATH=
PYTHON := python3.6
PIP_TOOLS_VERSION := 4.4.*
mkfile_path := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

check: check-coding-standards check-tests

check-coding-standards: check-pycodestyle check-pylint check-isort

check-pycodestyle: venv
	venv/bin/python -m pycodestyle bill_member.py

check-pylint: venv
	venv/bin/python -m pylint bill_member.py

check-isort: venv
	venv/bin/isort --check --diff --skip venv

check-tests: venv
	venv/bin/python -m pytest

install-pip-tools:
	$(PYTHON) -m pip install --user pip==19.* setuptools==46.*
	$(PYTHON) -m pip install --user pip-tools==$(PIP_TOOLS_VERSION)

requirements.txt: | requirements.in
	$(PYTHON) -m piptools compile --no-header --output-file $@
	chmod +r $@

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || $(PYTHON) -m venv venv
	venv/bin/python -m pip install pip==19.* setuptools==46.*
	venv/bin/python -m pip install -r $< --progress-bar off
	touch $@

upgrade:
	$(PYTHON) -m piptools compile --no-header --upgrade
	chmod +r $@

clean:
	find . -name '*.pyc' -type f -delete
	find . -name '__pycache__' -type d -delete
	rm -rf venv

.PHONY: check check-coding-standards check-pylint check-tests \
    clean deps install-pip-tools