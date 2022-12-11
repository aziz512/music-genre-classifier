FROM python:3.10.8

ENV PYTHONUNBUFFERED=1
ENV NUMBA_CACHE_DIR=/tmp/numba_cache

COPY . .
COPY requirements.txt .
RUN mkdir ./web/temp_files
RUN chmod 777 ./web/temp_files

RUN pip install --upgrade pip \
  && pip install --upgrade pipenv\
  && apt-get clean \
  && apt-get update \
  && apt install -y build-essential \
  && apt-get install -y libsndfile1 \
  && apt-get install -y ffmpeg \
  && pip install --upgrade -r requirements.txt


USER 1001

EXPOSE 8080
WORKDIR ./web


CMD ["python", "app.py", "8080"]