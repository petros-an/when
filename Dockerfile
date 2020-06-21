FROM python:3.7
RUN pip install pipenv
COPY Pipfile* /tmp/
RUN mkdir -p /opt/when/
COPY . /opt/when/
WORKDIR /opt/when
RUN cd /opt/when && pipenv install
