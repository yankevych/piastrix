FROM python:3.8.5

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY / /

WORKDIR /

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade -r requirements.txt

EXPOSE 5000
COPY . .
CMD ["flask", "run"]




