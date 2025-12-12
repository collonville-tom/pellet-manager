FROM python:3.11.4-slim-buster


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip install Django psycopg2-binary django-environ django-debug-toolbar

# copy project
RUN mkdir -p /usr/src/pellet_mgmt_proj
COPY ./pellet_mgmt_proj /usr/src/pellet_mgmt_proj/pellet_mgmt_proj
COPY ./pellet_mgmt_app /usr/src/pellet_mgmt_proj/pellet_mgmt_app
COPY ./manage.py /usr/src/pellet_mgmt_proj/manage.py 
COPY ./startContaineur.sh /usr/src/pellet_mgmt_proj/startContaineur.sh

RUN chmod +x /usr/src/pellet_mgmt_proj/startContaineur.sh

# set work directory
WORKDIR /usr/src/pellet_mgmt_proj