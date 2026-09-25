FROM python:3.11
WORKDIR /application
COPY . /application
# in docker image, we are creating an "application" folder,
# and copying everthing from our main file "application" into there

RUN apt update -y

RUN apt-get update && pip install -r requirements.txt
CMD ["python3", "application.py"]