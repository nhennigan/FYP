FROM python:3.8-alpine
WORKDIR /code
COPY requirements.txt /code/
#RUN pip install -r requirements.txt

RUN apk update  
#RUN apk add python3-dev 
#RUN pip install Flask-Datepicker
RUN pip install Flask-Mail
RUN pip install -r requirements.txt
#RUN apk add gcc
#RUN pip install flask-googlemaps

#RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
#RUN apk --no-cache --update-cache add gcc gfortran python python-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev
#RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
#RUN pip install numpy==1.14.3
COPY . /code/
ENV FLASK_APP main.py
CMD flask run --host=0.0.0.0
#CMD ["site.py"] 
