FROM python:3.8
COPY . /jwt_proxy
WORKDIR /jwt_proxy
RUN pip install -r ./requirements.txt
CMD ["python", "app.py"]