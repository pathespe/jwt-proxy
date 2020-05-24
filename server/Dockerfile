FROM python:3.8
COPY . /server
WORKDIR /server
RUN pip install -r ./server/requirements.txt
CMD ["python", "./server/server.py"]