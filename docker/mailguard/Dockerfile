FROM python:3.8

ENV DockerHOME=/home/app/webapp  

RUN mkdir -p $DockerHOME  

WORKDIR $DockerHOME  


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

RUN pip install --upgrade pip
RUN pip install -r requirements.txt  

EXPOSE 8000  

CMD python src/manage.py runserver