.PHONY: tests

dev_env:
	pip install -r requirements.txt

tests:
	flake8
	pytest --verbose --cov-branch --cov-report term-missing --tb=short --cov=main

github: tests
	git commit -a
	git push origin main
