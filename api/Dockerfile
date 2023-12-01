FROM python:3.9

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip3 install --no-cache-dir -r  requirements.txt


CMD exec uvicorn app.server.app:app --host 0.0.0.0 --port ${PORT} --workers 1