PACKAGE=stubby
.DEFAULT_GOAL := help

.PHONY: clean-build
clean-build: ## Remove build artifacts
	@echo "> $@"
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info

.PHONY: clean-pyc
clean-pyc: ## Remove python file artifacts
	@echo "> $@"
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name '*.py[co]' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

.PHONY: clean
clean: clean-pyc ## clean-pyc

.PHONY: clean-all
clean-all: clean-build clean-pyc ## Remove all file artifacts

.PHONY: uninstall
uninstall: ## Uninstall package
	@echo "> $@"
	@pip3 uninstall -y ${PACKAGE}

.PHONY: uninstall-all
uninstall-all: uninstall ## Uninstall all packages and dependencies
	@echo "> $@"
	@pip3 freeze | xargs pip3 uninstall -y

.PHONY: install-pkg-deps
install-pkg-deps: ## Install package dependencies
	@echo "> $@"
	@pip3 install -r requirements.txt

.PHONY: install-dev-deps
install-dev-deps: ## Install development and test dependencies
	@echo "> $@"
	@pip3 install -r dev-requirements.txt

.PHONY: install
install: uninstall install-pkg-deps ## Install package in site-packages
	@echo "> $@"
	@pip3 install .

.PHONY: editable
editable: uninstall install-pkg-deps ## Install entrypoint(s) for development
	@echo "> $@"
	@pip3 install --editable .

.PHONY: install-deps
install-deps: install-pkg-deps install-dev-deps ## Install all dependencies

.PHONY: lint
lint: clean-pyc ## Run autopep8 and flake8 in-place
	@echo "+ $@"
	@autopep8 --in-place -r .
	@flake8

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'
