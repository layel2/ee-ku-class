FROM python:3.9-slim

RUN apt-get update
RUN apt install curl -y
RUN apt-get install poppler-utils -y
RUN apt-get install libpq-dev -y
RUN apt-get install gcc -y
ADD requirements.txt /home/core/

WORKDIR /home/core/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD ./app /home/core/
# RUN python manage.py collectstatic --noinput

EXPOSE 8000
#ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "handler.asgi", "-w", "4", "-k", "uvicorn.workers.UvicornWorker"]
ENTRYPOINT ["uvicorn", "cotab.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
