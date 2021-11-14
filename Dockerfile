FROM python:3.11-rc-bullseye
ENV PYTHONUNBUFFERED 1
RUN git clone https://github.com/Erfan017/user_managment.git /drf_src
WORKDIR /drf_src
RUN ls .
RUN pip install -r requirements.txt
VOLUME /drf_src
EXPOSE 8080
CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000