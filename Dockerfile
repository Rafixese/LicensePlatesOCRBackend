FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV FLASK_DEBUG 1

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
#CMD python3 app.py

ENV PYTHONPATH /app
