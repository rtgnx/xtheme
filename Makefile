.PHONY: build

test: setup.py
	python setup.py test

build: setup.py
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf .eggs/ *.egg-info build/* dist/*
