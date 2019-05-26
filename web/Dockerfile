# Good Resource:
# https://blog.realkinetic.com/building-minimal-docker-containers-for-python-applications-37d0272c52f3

FROM python:3.7-alpine
RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev && \
    apk add postgresql-dev
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY . /app
WORKDIR /app
# Run models.py to build tables, also adds some basic data to the database

#RUN python models.py
#CMD ["python", "models.py"]
CMD ["gunicorn", "-w 4", "-b 0.0.0.0:80", "main:app"]
