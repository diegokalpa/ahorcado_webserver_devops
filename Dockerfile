FROM python:3.8-alpine
WORKDIR /app
COPY requirements.txt requirements.txt 
COPY venv/archivos/data.txt venv/
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_APP=venv/"ahorcado.py"

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]