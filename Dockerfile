FROM python:alpine3.7
COPY . /youtube_haiku
WORKDIR /youtube_haiku
RUN pip install -r requirements.txt
EXPOSE 5001
ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "wsgi:app"]