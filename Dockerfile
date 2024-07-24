FROM python:3.11-slim-buster

COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt update && apt install -y libpq-dev gcc default-libmysqlclient-dev pkg-config 

# install python dependencies
RUN pip install --progress-bar off --upgrade pip --no-cache-dir -r requirements.txt


# running migrations
# RUN python main.py
CMD ["python","main.py"]
