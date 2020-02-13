# Add any tasks that are not dependent on files to the .PHONY list.
.PHONY: install_without_dev_from_lock

install_without_dev_from_lock:
	pipenv --rm install --ignore-pipfile --python 3.6
	pipenv run pip install .
