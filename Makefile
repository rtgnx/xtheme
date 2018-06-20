image=rtgnx/xtheme

.PHONY: build

image: Dockerfile
	docker build -t $(image) .

test: image
	docker run --rm -it  -v `pwd`/:/xtheme $(image)

build: setup.py
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf .eggs/ *.egg-info build/* dist/*
