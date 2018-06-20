FROM python:alpine3.7

RUN apk update && apk add gcc py-configobj py-pip python-dev musl-dev libffi-dev
RUN mkdir /xtheme $HOME/.config
WORKDIR /xtheme

CMD ["python", "setup.py", "test"]
