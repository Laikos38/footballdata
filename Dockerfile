FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y install sudo

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r ./requirements/local.txt

RUN chmod +x ./scripts/entrypoint.sh

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]