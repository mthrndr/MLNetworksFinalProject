dev_env:
	pip install -r requirements.txt

.PHONY: tests
tests:
	flake8
	pytest --verbose --cov-report term-missing --tb=short --cov=.

github: tests
	git commit -a
	git push origin main
